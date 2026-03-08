from config import llm
from schemas import Critique, Report
from agents.query_writer_agent import steps_to_text
from agents.writer_agent import research_to_text
from state import AgentState


_llm = llm.with_structured_output(Critique)

CRITIC_PROMPT = """You are a strict research report critic. Evaluate the report below 
against the original research plan and the raw research data it was based on.

Score each dimension from 1 to 10:
- Coverage    (40%): Every research step has a matching section with meaningful content
- Accuracy    (40%): All facts are grounded in the research data, nothing invented
- Clarity     (20%): Well-structured, easy to follow, no ambiguity

Compute overall as the weighted average of the four scores.
Set passed = True if overall >= 7.

If passed is False you MUST provide:
- issues: a specific list of problems (reference section/step names concretely)
- revision_instructions: exact instructions telling the Writer what to change

If passed is True, set issues to an empty list and revision_instructions to "".

Original Research Plan:
{plan}

Research Data (what the Writer had access to):
{research_data}

Report to evaluate:
Title: {title}

Executive Summary:
{executive_summary}

{sections}

Conclusion:
{conclusion}
"""

def report_sections_to_text(report: Report) -> str:
    lines = []
    for s in report.sections:
        lines.append(f"Section: {s.title}")
        lines.append(s.body)
        lines.append("")
    return "\n".join(lines)

def critic_node(state: AgentState) -> AgentState:
    plan = state["plan"]
    report = state["report"]
    research_results = state["research_results"]

    print(f"Critic is reviewing the report...\n")

    prompt = CRITIC_PROMPT.format(
        plan=steps_to_text(plan.steps),
        research_data=research_to_text(research_results),
        title=report.title,
        executive_summary=report.executive_summary,
        sections=report_sections_to_text(report),
        conclusion=report.conclusion
    )

    critique: Critique = _llm.invoke(prompt)

    # Print scores
    s = critique.scores
    print(f"Coverage: {s.coverage}/10 | Accuracy: {s.accuracy}/10 | "
          f"Clarity: {s.clarity}/10")
    print(f"Overall: {critique.overall}/10 — {'Passed' if critique.passed else 'Failed'}")

    if not critique.passed:
        print(f"Issues:")
        for issue in critique.issues:
            print(f"- {issue}")
    print()

    return {"critique": critique}