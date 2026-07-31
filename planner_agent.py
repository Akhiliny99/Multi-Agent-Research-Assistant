from langchain_groq import ChatGroq
from agents.state import AgentState
from config import GROQ_API_KEY, GROQ_MODEL

llm = ChatGroq(model=GROQ_MODEL, api_key=GROQ_API_KEY, temperature=0)


def planner_node(state: AgentState) -> AgentState:
    """Breaks the topic down into concrete research questions."""
    prompt = (
        "You are a research planner. Break the topic below into 3-5 concrete, "
        "specific research questions the researcher should investigate. "
        "Return them as a numbered list only, no preamble.\n\n"
        f"Topic: {state['topic']}"
    )
    response = llm.invoke(prompt)
    state["plan"] = response.content
    state["research_notes"] = state.get("research_notes", [])
    state["iteration"] = state.get("iteration", 0)
    return state
