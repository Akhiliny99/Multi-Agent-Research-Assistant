r"""
Builds the LangGraph state machine:

    planner -> researcher -> writer -> critic --(revise)--> researcher (loop)
                                              \--(end)-----> END

This is a genuine graph (with a conditional loop-back edge), not a linear
chain -- which is the distinction interviewers usually probe for when a CV
says "LangGraph experience".
"""
from langgraph.graph import StateGraph, END

from agents.state import AgentState
from agents.planner_agent import planner_node
from agents.researcher_agent import researcher_node
from agents.writer_agent import writer_node
from agents.critic_agent import critic_node


def route_after_critic(state: AgentState) -> str:
    if state["iteration"] >= state["max_iterations"]:
        return "end"
    critique = (state.get("critique") or "").strip().upper()
    if critique.startswith("APPROVED"):
        return "end"
    return "revise"


def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("planner", planner_node)
    graph.add_node("researcher", researcher_node)
    graph.add_node("writer", writer_node)
    graph.add_node("critic", critic_node)

    graph.set_entry_point("planner")
    graph.add_edge("planner", "researcher")
    graph.add_edge("researcher", "writer")
    graph.add_edge("writer", "critic")

    graph.add_conditional_edges(
        "critic",
        route_after_critic,
        {
            "revise": "researcher",
            "end": END,
        },
    )

    return graph.compile()
