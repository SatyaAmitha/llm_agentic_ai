from agents import Agent, WebSearchTool, ModelSettings, OpenAIChatCompletionsModel
import os
from agents import function_tool
from llm_client import client

INSTRUCTIONS = (
    "You are a research assistant. Given a search term, you search the web for that term and "
    "produce a concise summary of the results. The summary must 2-3 paragraphs and less than 300 "
    "words. Capture the main points. Write succintly, no need to have complete sentences or good "
    "grammar. This will be consumed by someone synthesizing a report, so its vital you capture the "
    "essence and ignore any fluff. Do not include any additional commentary other than the summary itself."
)

local_client = client
local_model = OpenAIChatCompletionsModel(
    model=os.getenv("LLM_MODEL") or os.getenv("LOCAL_LLM_MODEL", "llama3.2:latest"),
    openai_client=local_client,
)


# Create simulated web search tool
@function_tool
async def simulated_web_search(query: str) -> str:
    """Simulate web search results for testing purposes"""
    mock_results = {
        "Latest AI Agent frameworks in 2025": """
        Based on current trends, the latest AI Agent frameworks in 2025 include:

        1. **OpenAI Agents SDK** - Comprehensive framework with hosted tools and function calling
        2. **LangChain** - Modular approach with extensive integrations and RAG capabilities
        3. **AutoGen** - Microsofts multi-agent conversation framework with group chat
        4. **CrewAI** - Task-based agent orchestration with role-based workflows
        5. **LangGraph** - Stateful, multi-actor applications with complex workflows
        6. **Semantic Kernel** - Microsofts AI orchestration framework
        7. **Flowise** - Low-code platform for building AI agents

        Key trends: Increased focus on tool integration, better memory management,
        improved agent coordination, multimodal capabilities, and cost optimization.
        """,
        "AI development trends": """
        Current AI development trends focus on:
        - Multimodal agents (text, image, audio, video)
        - Better reasoning and planning capabilities
        - Cost optimization and efficiency
        - Improved memory and context management
        - Enhanced tool integration and API connectivity
        - Better human-AI collaboration interfaces
        """,
        "AI agent market": """
        The AI agent market is experiencing rapid growth with:
        - Enterprise adoption for automation and decision support
        - Integration with existing business workflows
        - Focus on domain-specific applications
        - Increased investment in agent infrastructure
        - Growing ecosystem of specialized tools and platforms
        """
    }

    # Return mock results or a generic response
    # ✅ Fixed properly closed f-string
    return mock_results.get(
        query,
        f"Simulated search results for: {query}\n\n"
        "This is a mock response for testing purposes. In a real implementation, "
        "this would contain actual web search results."
    )

search_agent = Agent(
    name="Search agent",
    instructions=INSTRUCTIONS,
    tools=[simulated_web_search],  # Use simulated search instead of WebSearchTool
    model=local_model,
    model_settings=ModelSettings(tool_choice="required"),
)

# search_agent = Agent(
#     name="Search agent",
#     instructions=INSTRUCTIONS,
#     tools=[WebSearchTool(search_context_size="low")],
#     model=local_openai_model,
#     model_settings=ModelSettings(tool_choice="required"),
# )