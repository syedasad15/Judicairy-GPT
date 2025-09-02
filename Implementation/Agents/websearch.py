import requests
from bs4 import BeautifulSoup
from utils.gpt_client import call_gpt4  # using same call_gpt4 (actually gpt-3.5-turbo in your client)

DUCKDUCKGO_SEARCH_URL = "https://duckduckgo.com/html/?q="

def search_web(query, max_results=5):
    """Perform a web search using DuckDuckGo and return list of (title, link, snippet)."""
    url = DUCKDUCKGO_SEARCH_URL + requests.utils.quote(query)
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(res.text, "html.parser")

    results = []
    for r in soup.select(".result")[:max_results]:
        title_tag = r.select_one(".result__a")
        snippet_tag = r.select_one(".result__snippet")
        if not title_tag:
            continue
        title = title_tag.get_text(" ", strip=True)
        link = title_tag["href"]
        snippet = snippet_tag.get_text(" ", strip=True) if snippet_tag else ""
        results.append((title, link, snippet))
    return results


def fetch_page_text(url, max_chars=3000):
    """Fetch text content from a webpage (trimmed to limit)."""
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")

        # Get visible text
        for script in soup(["script", "style", "noscript"]):
            script.extract()
        text = " ".join(soup.get_text().split())
        return text[:max_chars]
    except Exception:
        return ""


def websearch_with_citations(query):
    """Perform search, fetch top results, and summarize with GPT including citations."""
    search_results = search_web(query)

    # Build context with numbered references
    sources_text = ""
    for i, (title, link, snippet) in enumerate(search_results, start=1):
        sources_text += f"[{i}] {title}\nURL: {link}\nSnippet: {snippet}\n\n"

    # Optionally fetch first 2 pages full text for deeper context
    extended_context = ""
    for i, (_, link, _) in enumerate(search_results[:2], start=1):
        page_text = fetch_page_text(link)
        if page_text:
            extended_context += f"\n\n[FullText from {i}] {page_text}"

    prompt = f"""
You are a legal research assistant with web access.

User asked:
"{query}"

I searched the web and found the following results:

{sources_text}

Additional page content:
{extended_context}

Now write a helpful, formal summary in the context of Pakistani law when relevant. 
- Integrate info clearly.
- Use numbered citations like [1], [2] where appropriate.
- Only cite if info comes from the sources above.
- If uncertain, say so.
"""

    return call_gpt4(prompt)
