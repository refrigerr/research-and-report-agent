from typing import TypedDict
from schemas import (
    ResearchPlan,
    StepQueries,
    StepResearch,
    Report,
    Critique,
)

class AgentState(TypedDict):
    user_message: str                    # Raw input from the user
    topic: str                           # Cleaned research topic extracted by input_node
    plan: ResearchPlan                   # Structured plan produced by planner_node
    search_queries: list[StepQueries]    # Queries produced by query_writer_node
    research_results: list[StepResearch] # Raw gathered data produced by researcher_node
    report: Report                       # Final report produced by writer_node
    critique: Critique                    # Latest critique from critic_node
    revision_count: int 