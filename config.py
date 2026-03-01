import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv(override=True)

MAX_REVISIONS = 2

llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0,
    api_key=os.environ.get("OPENAI_API_KEY")
)

tavily = TavilyClient(api_key=os.environ.get("TAVILY_API_KEY"))