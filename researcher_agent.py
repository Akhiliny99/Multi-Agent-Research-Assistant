from langchain_groq import ChatGroq
from agents.state import AgentState
from agents.mcp_client import call_mcp_tool_sync
from config import GROQ_API_KEY, GROQ_MODEL

llm = ChatGroq(model=GROQ_MODEL, api_key=GROQ_API_KEY, temperature=0)


def researcher_node(state: AgentState) -> AgentState:
    """
    Uses the MCP `web_search` tool to gather fresh information, then asks the
    LLM to condense it into research notes. Re-entered on revision loops, so
    it also takes the previous critique into account when present.
    """
    plan = state.get("plan", state["topic"])
    critique = state.get("critique")

    query = state["topic"] if not critique else f"{state['topic']} {critique}"
    search_results = call_mcp_tool_sync("web_search", {"query": query, "max_results": 5})

    prompt = (
        "Using the research plan and web search results below, write concise "
        "research notes as bullet points covering the key facts and figures.\n\n"
        f"Research plan:\n{plan}\n\n"
    )
    if critique:
        prompt += f"Address this feedback from the last review:\n{critique}\n\n"
    prompt += f"Web search results:\n{search_results}"

    response = llm.invoke(prompt)

    notes = state.get("research_notes", [])
    notes.append(response.content)
    state["research_notes"] = notes
    return state
