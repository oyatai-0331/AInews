# Priority Sources (優先巡回URLリスト)

List the URLs you want the research step (Claude Code) to crawl **first**,
before falling back to open-ended WebSearch. These are the feeds, blogs, and
listing pages your lab trusts most.

How it is used:

- The research prompt tells Claude Code to `Read` this file at the start of each
  run, then `WebFetch` the URLs below **before** doing general web search.
- Use the fetched pages to discover concrete, recent items (papers / releases /
  posts), then follow and `WebFetch` the specific links you find on them.
- These are *priorities*, not a whitelist. After exhausting them, Claude may
  still `WebSearch` freely for anything relevant and new.
- Still obey the rules in CLAUDE.md: only include items from pages you actually
  opened, and never fabricate titles, authors, dates, or URLs.

Format: one URL per bullet. An optional `—` note after the URL explains what the
page is. Lines that are not bullets (like this paragraph) are ignored.

## URLs

- https://openai.com/news/ — OpenAI news and product announcements
- https://www.anthropic.com/news — Anthropic news and product announcements
- https://blog.google/technology/ai/ — Google AI news
- https://deepmind.google/discover/blog/ — Google DeepMind research and product blog
- https://ai.meta.com/blog/ — Meta AI blog
- https://blogs.microsoft.com/ai/ — Microsoft AI blog
- https://mistral.ai/news/ — Mistral AI news
- https://x.ai/news — xAI news
- https://huggingface.co/blog — Hugging Face blog
- https://huggingface.co/papers — Hugging Face daily papers
- https://github.blog/changelog/ — GitHub product changelog
- https://vercel.com/blog?tag=ai — Vercel AI and platform posts
- https://blog.langchain.com/ — LangChain blog
- https://www.llamaindex.ai/blog — LlamaIndex blog
- https://www.reuters.com/technology/artificial-intelligence/ — Reuters AI coverage
- https://techcrunch.com/category/artificial-intelligence/ — TechCrunch AI coverage
- https://www.theverge.com/ai-artificial-intelligence — The Verge AI coverage
- https://www.technologyreview.com/topic/artificial-intelligence/ — MIT Technology Review AI coverage
- https://arxiv.org/list/cs.CL/recent — arXiv cs.CL (computation & language), newest first
- https://arxiv.org/list/cs.LG/recent — arXiv cs.LG (machine learning), newest first
- https://arxiv.org/list/cs.AI/recent — arXiv cs.AI (artificial intelligence), newest first
- https://arxiv.org/list/cs.IR/recent — arXiv cs.IR (information retrieval), newest first
- https://arxiv.org/list/stat.ML/recent — arXiv stat.ML (machine learning statistics), newest first
- https://aclanthology.org/ — ACL Anthology for NLP papers and proceedings
- https://paperswithcode.com/latest — Papers with Code, latest
- https://www.semanticscholar.org/ — Semantic Scholar search
- https://openreview.net/ — OpenReview (conference submissions & reviews)

<!--
Add your own below. Examples:
- https://example-lab.github.io/blog/ — a group blog you follow
- https://some-conference.org/accepted-papers — this year's accepted list
-->
