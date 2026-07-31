"""
Run the full multi-agent research pipeline in-process (single Python process,
LangGraph handling orchestration + the revision loop).

Usage:
    python main.py "The impact of retrieval-augmented generation on enterprise search"
"""
import sys
from graph import build_graph
from config import MAX_REVISION_ITERATIONS


def run(topic: str):
    app = build_graph()

    initial_state = {
        "topic": topic,
        "plan": None,
        "research_notes": [],
        "draft": None,
        "critique": None,
        "final_report": None,
        "iteration": 0,
        "max_iterations": MAX_REVISION_ITERATIONS,
    }

    final_state = app.invoke(initial_state)

    print("\n" + "=" * 60)
    print("PLAN")
    print("=" * 60)
    print(final_state.get("plan"))

    print("\n" + "=" * 60)
    print(f"FINAL REPORT (after {final_state['iteration']} iteration(s))")
    print("=" * 60)
    print(final_state.get("final_report") or final_state.get("draft"))

    return final_state


if __name__ == "__main__":
    topic_arg = " ".join(sys.argv[1:]) or "Retrieval-Augmented Generation for enterprise knowledge bases"
    run(topic_arg)
