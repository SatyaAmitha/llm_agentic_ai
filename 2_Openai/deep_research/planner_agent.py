from pydantic import BaseModel, Field
import os
from agents import Agent, OpenAIChatCompletionsModel
from llm_client import client

HOW_MANY_SEARCHES = 5

INSTRUCTIONS = f"You are a helpful research assistant. Given a query, come up with a set of web searches \
to perform to best answer the query. Output {HOW_MANY_SEARCHES} terms to query for."


class WebSearchItem(BaseModel):
    reason: str = Field(description="Your reasoning for why this search is important to the query.")
    query: str = Field(description="The search term to use for the web search.")


class WebSearchPlan(BaseModel):
    searches: list[WebSearchItem] = Field(description="A list of web searches to perform to best answer the query.")


local_client = client
local_model = OpenAIChatCompletionsModel(
    model=os.getenv("LLM_MODEL") or os.getenv("LOCAL_LLM_MODEL", "llama3.2:latest"),
    openai_client=local_client,
)

planner_agent = Agent(
    name="PlannerAgent",
    instructions=INSTRUCTIONS,
    model=local_model,
    output_type=WebSearchPlan,
)