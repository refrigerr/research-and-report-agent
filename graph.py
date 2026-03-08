from langgraph.graph import StateGraph, END
from config import MAX_REVISIONS
from state import AgentState
from agents.input_agent import input_node
from agents.planner_agent import planner_node
from agents.query_writer_agent import query_writer_node
from agents.researcher_agent import researcher_node
from agents.writer_agent import writer_node
from agents.critic_agent import critic_node


def should_revise(state: AgentState) -> str:
    """After Critic: loop back to Writer if failed and under revision limit."""
    critique = state["critique"]
    revision_count = state.get("revision_count", 0)

    if not critique.passed and revision_count < MAX_REVISIONS:
        print(f"Sending back to Writer (revision {revision_count + 1}/{MAX_REVISIONS})\n")
        return "revise"

    if not critique.passed:
        print(f"Max revisions reached — delivering best available report.\n")

    return "deliver"


def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("input", input_node)
    graph.add_node("planner", planner_node)
    graph.add_node("query_writer", query_writer_node)
    graph.add_node("researcher", researcher_node)
    graph.add_node("writer", writer_node)
    graph.add_node("critic", critic_node)

    graph.set_entry_point("input")
    graph.add_edge("input", "planner")
    graph.add_edge("planner", "query_writer")
    graph.add_edge("query_writer", "researcher")
    graph.add_edge("researcher", "writer")
    graph.add_edge("writer", "critic")

    graph.add_conditional_edges(
        "critic",
        should_revise,
        {
            "revise": "writer",
            "deliver": END
        }
    )

    return graph.compile()