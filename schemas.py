from pydantic import BaseModel, Field

class ResearchTopic(BaseModel):
    topic: str = Field(description="A clean, well-formed research topic extracted from the user message")
    reasoning: str = Field(description="Why you interpreted the user's message this way")

class ResearchStep(BaseModel):
    step_number: int = Field(description="Step number in the research plan")
    title: str = Field(description="Short title for this research step")
    description: str = Field(description="What to research or do in this step")
    goal: str = Field(description="What we expect to learn or produce from this step")

class ResearchPlan(BaseModel):
    topic: str = Field(description="The main research topic")
    objective: str = Field(description="Overall goal of the research")
    steps: list[ResearchStep] = Field(description="Ordered list of research steps")
    expected_output: str = Field(description="What the final report should contain")
    
class StepQueries(BaseModel):
    step_number: int = Field(description="The step this belongs to")
    step_title: str = Field(description="Title of the step")
    queries: list[str] = Field(description="2-3 focused search queries for this step")

class QueryWriterOutput(BaseModel):
    steps: list[StepQueries] = Field(description="Search queries for each research step")
    
class SearchResult(BaseModel):
    query: str      # The query that produced this result
    source: str     # URL of the source
    title: str      # Page title
    content: str    # Relevant content snippet
    
class StepResearch(BaseModel):
    step_number: int
    step_title: str
    results: list[SearchResult]  # All search results gathered for this step
    
class ReportSection(BaseModel):
    title: str = Field(description="Section heading")
    body: str = Field(description="Section content in 2-4 paragraphs")
    
class Report(BaseModel):
    title: str = Field(description="Report title")
    executive_summary: str = Field(description="1 short paragraph overview of the whole report")
    sections: list[ReportSection] = Field(description="Main body sections, one per research step")
    conclusion: str = Field(description="1 short paragraph wrapping up key takeaways")
    sources: list[str] = Field(description="Deduplicated list of source URLs used in the report")
    
class CritiqueScores(BaseModel):
    coverage: int = Field(description="1-10: Does the report cover all research steps thoroughly?")
    accuracy: int = Field(description="1-10: Is the report grounded in the research data, no invented facts?")
    clarity: int = Field(description="1-10: Is the report clear, well-structured, and easy to follow?")
    
class Critique(BaseModel):
    scores: CritiqueScores
    overall: int = Field(description="Overall score 1-10, weighted: coverage 40%, accuracy 40%, clarity 20%")
    passed: bool = Field(description="True if overall >= 7")
    issues: list[str] = Field(description="Specific, actionable issues. Empty if passed=True")
    revision_instructions: str = Field(description="Concrete instructions for the Writer on what to fix. Empty string if passed=True")