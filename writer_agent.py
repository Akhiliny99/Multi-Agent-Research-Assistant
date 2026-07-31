from langchain_groq import ChatGroq
from agents.state import AgentState
from config import GROQ_API_KEY, GROQ_MODEL

llm = ChatGroq(model=GROQ_MODEL, api_key=GROQ_API_KEY, temperature=0.3)


def writer_node(state: AgentState) -> AgentState:
    """Synthesizes all accumulated research notes into a coherent draft report."""
    notes = "\n\n".join(state.get("research_notes", []))
    prompt = (
        "Write a well-structured report on the topic below using the research "
        "notes provided. Use clear headings and short paragraphs.\n\n"
        f"Topic: {state['topic']}\n\n"
        f"Research notes:\n{notes}"
    )
    response = llm.invoke(prompt)
    state["draft"] = response.content
    return state
