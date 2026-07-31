"""
MCP Server: exposes research tools over the Model Context Protocol (stdio transport).

Run standalone to test:
    python mcp_server/search_server.py

The researcher agent (agents/mcp_client.py) launches this as a subprocess and
talks to it over stdio using the MCP protocol -- this is what satisfies the
"Build MCP tools" requirement, as opposed to just calling a Python function
directly.
"""
from mcp.server.fastmcp import FastMCP
from duckduckgo_search import DDGS
import httpx

mcp = FastMCP("research-tools")


@mcp.tool()
def web_search(query: str, max_results: int = 5) -> str:
    """
    Search the web for a query and return a formatted summary of the top results.

    Args:
        query: the search query
        max_results: how many results to return (default 5)
    """
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
    """
    Fetch a URL and return a truncated plain-text preview of its content.

    Args:
        url: the URL to fetch
        max_chars: max characters of raw content to return
    """
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
