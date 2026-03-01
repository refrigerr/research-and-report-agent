from config import llm, MAX_REVISIONS
from schemas import Report, StepResearch, Critique
from state import AgentState


_llm = llm.with_structured_output(Report)


WRITER_PROMPT = """You are a professional research writer. Your job is to write a clear, 
well-structured research report based strictly on the provided research data.

Report structure:
- Title: clear and descriptive
- Executive Summary: 1 paragraph, 3-5 sentences, captures the whole story
- Sections: one section per research step, each with 2-3 focused paragraphs
- Conclusion: 1 paragraph, 3-5 sentences, key takeaways only
- Sources: deduplicated list of all URLs referenced

Writing rules:
- Write for an informed reader, not a beginner
- Only use information present in the research data — do not invent facts
- Be direct: no filler phrases like "it is worth noting that" or "in conclusion, we can see"
- Each section must reflect what was actually found for that step

Topic: {topic}
Objective: {objective}
Expected output: {expected_output}

{revision_block}

Research Data:
{research_data}
"""

REVISION_BLOCK = """== REVISION REQUEST ==
A Critic reviewed your previous version and it did not pass. You MUST address every issue below.

Issues:
{issues}

Instructions:
{instructions}
== END REVISION REQUEST ==
"""

def research_to_text(research_results: list[StepResearch]) -> str:
    """Serialize all research results into a readable block for the prompt."""
    lines = []
    for step in research_results:
        lines.append(f"=== Step {step.step_number}: {step.step_title} ===")
        for r in step.results:
            lines.append(f"  Query   : {r.query}")
            lines.append(f"  Title   : {r.title}")
            lines.append(f"  Source  : {r.source}")
            lines.append(f"  Content : {r.content}")
            lines.append("")
    return "\n".join(lines)

def writer_node(state: AgentState) -> AgentState:
    plan = state["plan"]
    research_results = state["research_results"]
    critique: Critique | None = state.get("critique")
    revision_count = state.get("revision_count", 0)

    if critique and not critique.passed:
        revision_count += 1
        print(f"✍️  Writer is revising the report (revision {revision_count}/{MAX_REVISIONS})...\n")
        revision_block = REVISION_BLOCK.format(
            issues="\n".join(f"- {i}" for i in critique.issues),
            instructions=critique.revision_instructions
        )
    else:
        print(f"✍️  Writer is composing the report...\n")
        revision_block = ""

    prompt = WRITER_PROMPT.format(
        topic=plan.topic,
        objective=plan.objective,
        expected_output=plan.expected_output,
        revision_block=revision_block,
        research_data=research_to_text(research_results)
    )

    report: Report = _llm.invoke(prompt)
    return {"report": report, "revision_count": revision_count}