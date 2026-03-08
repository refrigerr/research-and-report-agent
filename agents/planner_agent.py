from config import llm
from schemas import ResearchPlan
from state import AgentState

_llm = llm.with_structured_output(ResearchPlan)

PLANNER_PROMPT = """You are a senior research strategist. Your job is to create a 
thorough, structured research plan for a given topic.

Given the topic below, produce a step-by-step research plan that a team of AI agents 
will follow. Each step should be focused and actionable. Aim for 4-6 steps.

Topic: {topic}

Think about:
- What background context is needed first?
- What are the key sub-questions to answer?
- What data, examples, or case studies would strengthen the report?

IMPORTANT: Every step must be about RESEARCH ONLY — finding, gathering, and analyzing 
information. Do NOT include any step about writing, drafting, summarizing, or synthesizing 
the final report. Steps like "Synthesize Findings", "Draft Report", or "Write Summary" 
are strictly forbidden. A separate Writer agent will handle that at the end of the pipeline.
"""

def planner_node(state: AgentState) -> AgentState:
    """Planner agent: takes a topic and returns a structured research plan."""
    topic = state["topic"]
    
    prompt = PLANNER_PROMPT.format(topic=topic)
    
    print(f"\nPlanner is creating a research plan for: '{topic}'\n")
    
    plan: ResearchPlan = _llm.invoke(prompt)
    
    return {"plan": plan}