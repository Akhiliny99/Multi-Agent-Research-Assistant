from langchain_groq import ChatGroq
from agents.state import AgentState
from config import GROQ_API_KEY, GROQ_MODEL

llm = ChatGroq(model=GROQ_MODEL, api_key=GROQ_API_KEY, temperature=0)


def critic_node(state: AgentState) -> AgentState:
    """
    Reviews the draft. If it's good, prefixes the critique with "APPROVED".
    Otherwise gives concrete revision feedback, which the graph's conditional
    edge will route back to the researcher node.
    """
    prompt = (
        "You are a strict editor. Review the draft report below for the given topic. "
        "If it is accurate, complete, and well-structured, respond with exactly "
        "'APPROVED' followed by nothing else. Otherwise respond with "
        "'REVISE:' followed by 2-3 concrete, specific points to fix.\n\n"
        f"Topic: {state['topic']}\n\n"
        f"Draft:\n{state.get('draft', '')}"
    )
    response = llm.invoke(prompt)
    critique = response.content.strip()
    state["critique"] = critique
    state["iteration"] = state.get("iteration", 0) + 1

    if critique.upper().startswith("APPROVED"):
        state["final_report"] = state.get("draft")

    return state
