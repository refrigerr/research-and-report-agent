from langchain_core.messages import HumanMessage, SystemMessage
from config import llm
from schemas import ResearchTopic
from state import AgentState


_llm = llm.with_structured_output(ResearchTopic)


def input_node(state: AgentState) -> AgentState:
    """Takes raw user message and extracts a clean research topic."""
    user_message = state["user_message"]
    print(f"\nUser asked: '{user_message}'")

    messages = [
        SystemMessage(content=(
            "You are a research assistant. The user will give you a question or message. "
            "Your job is to extract or rephrase it into a clean, specific research topic "
            "suitable for deep research. Be precise — don't broaden too much, don't narrow too much."
        )),
        HumanMessage(content=user_message)
    ]

    result: ResearchTopic = _llm.invoke(messages)
    print(f"Extracted topic: '{result.topic}'")
    print(f"Reasoning: {result.reasoning}\n")

    return {"topic": result.topic}