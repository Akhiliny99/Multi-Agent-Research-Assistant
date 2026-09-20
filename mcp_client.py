
import asyncio
import os
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

_THIS_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_SERVER_SCRIPT = os.path.join(_THIS_DIR, "mcp_server", "search_server.py")

SERVER_PARAMS = StdioServerParameters(
    command="python",
    args=[_SERVER_SCRIPT],
)


async def call_mcp_tool(tool_name: str, arguments: dict) -> str:
    async with stdio_client(SERVER_PARAMS) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool(tool_name, arguments=arguments)
            text_parts = [c.text for c in result.content if hasattr(c, "text")]
            return "\n".join(text_parts)


def call_mcp_tool_sync(tool_name: str, arguments: dict) -> str:
    """Synchronous wrapper -- safe to call from a normal LangGraph node."""
    return asyncio.run(call_mcp_tool(tool_name, arguments))


if __name__ == "__main__":
    # quick manual test
    out = call_mcp_tool_sync("web_search", {"query": "LangGraph multi-agent systems", "max_results": 3})
    print(out)
