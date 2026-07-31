from typing import TypedDict, List, Optional


class AgentState(TypedDict):
    """
    Shared state object that flows through every node in the LangGraph.
    Each agent reads from and writes to this dict.
    """
    topic: str
    plan: Optional[str]
    research_notes: List[str]
    draft: Optional[str]
    critique: Optional[str]
    final_report: Optional[str]
    iteration: int
    max_iterations: int
