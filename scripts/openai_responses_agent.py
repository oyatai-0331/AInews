#!/usr/bin/env python3
"""Run one OpenAI Responses API turn with optional web search and JSON output.

This is the OpenAI fallback for `.github/actions/agent`. It intentionally uses
only the Python standard library so GitHub Actions does not need dependency
installation. The script receives the prompt and JSON schema via environment
variables, calls the Responses API, extracts one JSON object from the model's
text output, and exposes it as a `json` GitHub Actions output.
"""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request

from extract_json import extract


API_URL = "https://api.openai.com/v1/responses"
DEFAULT_MODEL = "gpt-5-mini"


def _truthy(value: str | None) -> bool:
    return (value or "").strip().lower() in {"1", "true", "yes", "on"}


def _output_text(response: dict) -> str:
    if isinstance(response.get("output_text"), str):
        return response["output_text"]

    texts: list[str] = []
    for item in response.get("output", []) or []:
        if not isinstance(item, dict):
            continue
        for content in item.get("content", []) or []:
            if not isinstance(content, dict):
                continue
            text = content.get("text")
            if isinstance(text, str):
                texts.append(text)
    return "\n".join(texts).strip()


def _request(payload: dict, api_key: str) -> dict:
    body = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        API_URL,
        data=body,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=600) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"OpenAI API HTTP {exc.code}: {detail}") from exc


def main() -> int:
    api_key = os.environ.get("OPENAI_API_KEY", "").strip()
    prompt = os.environ.get("AGENT_PROMPT", "").strip()
    schema_raw = os.environ.get("JSON_SCHEMA", "").strip()
    model = os.environ.get("OPENAI_MODEL", "").strip() or DEFAULT_MODEL
    web_search = _truthy(os.environ.get("WEB_SEARCH"))

    if not api_key:
        print("::warning title=OpenAI fallback::OPENAI_API_KEY is empty; skipping.", file=sys.stderr)
        return 0
    if not prompt or not schema_raw:
        print("::warning title=OpenAI fallback::prompt or JSON schema is empty; skipping.", file=sys.stderr)
        return 0

    try:
        schema = json.loads(schema_raw)
    except json.JSONDecodeError as exc:
        print(f"::error title=OpenAI fallback::JSON_SCHEMA is invalid: {exc}", file=sys.stderr)
        return 1

    if web_search:
        prompt = (
            f"{prompt}\n\n"
            "Use the OpenAI web_search tool for current claims. Include only items "
            "grounded in sources found through web search or URLs supplied in the "
            "repository context. Do not guess live news, release names, dates, or URLs."
        )

    payload: dict = {
        "model": model,
        "input": prompt,
        "text": {
            "format": {
                "type": "json_schema",
                "name": "structured_output",
                "schema": schema,
                "strict": False,
            }
        },
    }
    if web_search:
        payload["tools"] = [{"type": "web_search"}]
        payload["tool_choice"] = "auto"
        payload["include"] = ["web_search_call.action.sources"]

    try:
        response = _request(payload, api_key)
    except RuntimeError as exc:
        print(f"::error title=OpenAI fallback::{exc}", file=sys.stderr)
        return 1

    raw = _output_text(response)
    try:
        data = extract(raw)
    except (ValueError, json.JSONDecodeError) as exc:
        print(f"::warning title=OpenAI fallback::could not parse JSON response ({exc}); skipping publish.", file=sys.stderr)
        return 0

    compact = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    print(compact)

    out = os.environ.get("GITHUB_OUTPUT", "").strip()
    if out:
        with open(out, "a", encoding="utf-8") as handle:
            handle.write("json<<__AGENT_JSON_EOF__\n")
            handle.write(compact + "\n")
            handle.write("__AGENT_JSON_EOF__\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
