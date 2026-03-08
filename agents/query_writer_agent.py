from config import llm
from schemas import QueryWriterOutput, ResearchStep
from state import AgentState
from datetime import date


_llm = llm.with_structured_output(QueryWriterOutput)

QUERY_WRITER_PROMPT = """You are an expert research query writer. You will be given a 
research topic and a structured research plan with multiple steps.

Your job is to write 2-3 precise, targeted web search queries for EACH step.

Rules for writing good queries:
- Be specific — avoid vague terms
- Use keywords a search engine would match well (not full sentences)
- Vary the angle of each query within a step (e.g. one factual, one recent, one comparative)
- Keep queries concise (5-10 words max)
- Reflect the step's goal, not just its title

Today's date is: {date}

Topic: {topic}

Research Steps:
{steps}
"""

def steps_to_text(steps: list[ResearchStep]) -> str:
    """Format plan steps into readable text for the prompt."""
    lines = []
    for step in steps:
        lines.append(f"Step {step.step_number}: {step.title}")
        lines.append(f"  Description: {step.description}")
        lines.append(f"  Goal: {step.goal}")
        lines.append("")
    return "\n".join(lines)

def query_writer_node(state: AgentState) -> AgentState:
    """Query Writer: generates 2-3 search queries per research step."""
    plan = state["plan"]

    print(f"Query Writer is generating search queries for {len(plan.steps)} steps...\n")

    prompt = QUERY_WRITER_PROMPT.format(
        date=date.today(),
        topic=plan.topic,
        steps=steps_to_text(plan.steps)
    )

    result: QueryWriterOutput = _llm.invoke(prompt)

    return {"search_queries": result.steps}