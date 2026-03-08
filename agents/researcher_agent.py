from state import AgentState
from schemas import StepResearch, SearchResult
from config import tavily


def researcher_node(state: AgentState) -> AgentState:
    """Researcher: runs each query through Tavily and collects results per step."""
    search_queries = state["search_queries"]

    print(f"Researcher is searching the web...\n")

    research_results: list[StepResearch] = []

    for step in search_queries:
        print(f"Step {step.step_number}: {step.step_title}")
        step_results: list[SearchResult] = []

        for query in step.queries:
            print(f"     ↳ Searching: \"{query}\"")

            try:
                response = tavily.search(
                    query=query,
                    max_results=3,          # 3 sources per query
                    search_depth="advanced" # deeper search, better content
                )

                for r in response.get("results", []):
                    step_results.append(SearchResult(
                        query=query,
                        source=r.get("url", ""),
                        title=r.get("title", ""),
                        content=r.get("content", "")
                    ))

            except Exception as e:
                print(f"Search failed for '{query}': {e}")

        research_results.append(StepResearch(
            step_number=step.step_number,
            step_title=step.step_title,
            results=step_results
        ))

        print(f"Collected {len(step_results)} results\n")

    return {"research_results": research_results}