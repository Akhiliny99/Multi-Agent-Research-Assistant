from typing import TypedDict, List, Optional


class AgentState(TypedDict):
    
    topic: str
    plan: Optional[str]
    research_notes: List[str]
    draft: Optional[str]
    critique: Optional[str]
    final_report: Optional[str]
    iteration: int
    max_iterations: int
