from config import MAX_REVISIONS
from graph import build_graph
from schemas import Report, ResearchPlan, StepQueries, StepResearch

def print_report(report: Report, critique=None):
    width = 60
    print("\n" + "=" * width)
    print(f"  {report.title}")
    print("=" * width)

    print(f"\nEXECUTIVE SUMMARY")
    print(f"{report.executive_summary}\n")

    for section in report.sections:
        print(f"{'─' * width}")
        print(f"  {section.title}")
        print(f"{'─' * width}")
        print(f"{section.body}\n")

    print(f"{'─' * width}")
    print(f"  CONCLUSION")
    print(f"{'─' * width}")
    print(f"{report.conclusion}\n")

    print(f"{'─' * width}")
    print(f"  SOURCES")
    print(f"{'─' * width}")
    for i, url in enumerate(report.sources, 1):
        print(f"  [{i}] {url}")

    if critique:
        s = critique.scores
        print(f"\n{'─' * width}")
        print(f"  FINAL CRITIQUE SCORES")
        print(f"{'─' * width}")
        print(f"  Coverage   : {s.coverage}/10")
        print(f"  Accuracy   : {s.accuracy}/10")
        print(f"  Clarity    : {s.clarity}/10")
        print(f"  Overall    : {critique.overall}/10 — {'Passed' if critique.passed else 'Delivered after max revisions'}")

        if not critique.passed and critique.issues:
            print(f"\n  Remaining issues:")
            for issue in critique.issues:
                print(f"    • {issue}")

    print("=" * width)
    
    
def run(user_message: str):
    app = build_graph()
    result = app.invoke({"user_message": user_message})

    plan: ResearchPlan = result["plan"]
    search_queries: list[StepQueries] = result["search_queries"]
    research_results: list[StepResearch] = result["research_results"]

    print("=" * 60)
    print(f"RESEARCH PLAN: {plan.topic}")
    print("=" * 60)
    print(f"\nObjective:\n   {plan.objective}\n")

    for step in plan.steps:
        print(f"  Step {step.step_number}: {step.title}")
        print(f"  ├─ What to do : {step.description}")
        print(f"  └─ Goal       : {step.goal}\n")

    print(f"Expected Output:\n   {plan.expected_output}")

    print("\n" + "=" * 60)
    print("SEARCH QUERIES")
    print("=" * 60)

    for step_q in search_queries:
        print(f"\n  Step {step_q.step_number}: {step_q.step_title}")
        for i, q in enumerate(step_q.queries, 1):
            prefix = "  └─" if i == len(step_q.queries) else "  ├─"
            print(f"{prefix} [{i}] {q}")

    print("\n" + "=" * 60)
    print("RESEARCH RESULTS")
    print("=" * 60)

    for step_r in research_results:
        print(f"\n  Step {step_r.step_number}: {step_r.step_title}  ({len(step_r.results)} results)")
        for r in step_r.results:
            print(f"\n    Query  : {r.query}")
            print(f"    Title  : {r.title}")
            print(f"    Source : {r.source}")
            print(f"    Content: {r.content[:200]}...")

    print("\n" + "=" * 60)
    print()
    print()
    print()
    print()
    
    revision_count = result.get("revision_count", 0)
    print(f"\n\n{'=' * 60}")
    print(f"REPORT  (revisions made: {revision_count}/{MAX_REVISIONS})")
    critique = result.get("critique")
    print_report(result["report"], critique)

    return result

user_input = "I don't know what RAG is"
run(user_input)