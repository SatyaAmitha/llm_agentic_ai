from pydantic import BaseModel, Field
from agents import Agent, OpenAIChatCompletionsModel
import os
from llm_client import client

INSTRUCTIONS = (
    "You are a senior researcher tasked with writing a cohesive report for a research query. "
    "You will be provided with the original query, and some initial research done by a research assistant.\n"
    "You should first come up with an outline for the report that describes the structure and "
    "flow of the report. Then, generate the report and return that as your final output.\n"
    "The final output should be in markdown format, and it should be lengthy and detailed. Aim "
    "for 5-10 pages of content, at least 1000 words."
)


class ReportData(BaseModel):
    short_summary: str = Field(description="A short 2-3 sentence summary of the findings.")

    markdown_report: str = Field(description="The final report")

    follow_up_questions: list[str] = Field(description="Suggested topics to research further")


local_client = client
local_model = OpenAIChatCompletionsModel(
    model=os.getenv("LLM_MODEL") or os.getenv("LOCAL_LLM_MODEL", "llama3.2:latest"),
    openai_client=local_client,
)

writer_agent = Agent(
    name="WriterAgent",
    instructions=INSTRUCTIONS,
    model=local_model,
    output_type=ReportData,
)