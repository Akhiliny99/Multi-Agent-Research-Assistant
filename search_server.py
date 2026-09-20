
from mcp.server.fastmcp import FastMCP
from duckduckgo_search import DDGS
import httpx

mcp = FastMCP("research-tools")


@mcp.tool()
def web_search(query: str, max_results: int = 5) -> str:
   
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
    except Exception as e:
        return f"Search failed: {e}"

    if not results:
        return "No results found."

    formatted = []
    for r in results:
        formatted.append(
            f"Title: {r.get('title', 'N/A')}\n"
            f"URL: {r.get('href', 'N/A')}\n"
            f"Snippet: {r.get('body', 'N/A')}"
        )
    return "\n\n---\n\n".join(formatted)


@mcp.tool()
def fetch_url_summary(url: str, max_chars: int = 3000) -> str:
  
    try:
        resp = httpx.get(url, timeout=10, follow_redirects=True, headers={
            "User-Agent": "Mozilla/5.0 (research-assistant-bot)"
        })
        resp.raise_for_status()
        return resp.text[:max_chars]
    except Exception as e:
        return f"Error fetching URL: {e}"


if __name__ == "__main__":
    # Runs the MCP server over stdio -- a client (our LangGraph agent) will
    # spawn this process and speak MCP to it.
    mcp.run()
