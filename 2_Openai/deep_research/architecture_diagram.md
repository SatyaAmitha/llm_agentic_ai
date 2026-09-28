# Deep Research System Architecture

## Mermaid Diagram

```mermaid
graph TB
    %% User Interface Layer
    UI[Gradio Web Interface<br/>deep_research.py]

    %% Main Orchestrator
    RM[ResearchManager<br/>research_manager.py]

    %% Agent Layer
    PA[Planner Agent<br/>planner_agent.py]
    SA[Search Agent<br/>search_agent.py]
    WA[Writer Agent<br/>writer_agent.py]
    EA[Email Agent<br/>email_agent.py]

    %% External Services
    LLM[Local LLM<br/>Ollama]
    WS[Web Search<br/>Simulated]
    SG[SendGrid API<br/>Email Service]

    %% Data Models
    WSP[WebSearchPlan<br/>Pydantic Model]
    WSItem[WebSearchItem<br/>Pydantic Model]
    RD[ReportData<br/>Pydantic Model]

    %% Flow Connections
    UI -->|User Query| RM
    RM -->|Plan Searches| PA
    PA -->|WebSearchPlan| RM
    RM -->|Search Items| SA
    SA -->|Search Results| RM
    RM -->|Query + Results| WA
    WA -->|ReportData| RM
    RM -->|Report| EA

    %% Agent to External Service Connections
    PA -->|Generate Plan| LLM
    SA -->|Search Query| WS
    SA -->|Summarize Results| LLM
    WA -->|Write Report| LLM
    EA -->|Format Email| LLM
    EA -->|Send Email| SG

    %% Data Model Connections
    PA -.->|Outputs| WSP
    WSP -.->|Contains| WSItem
    WA -.->|Outputs| RD

    %% Styling
    classDef uiClass fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    classDef agentClass fill:#f3e5f5,stroke:#4a148c,stroke-width:2px
    classDef serviceClass fill:#e8f5e8,stroke:#1b5e20,stroke-width:2px
    classDef modelClass fill:#fff3e0,stroke:#e65100,stroke-width:2px

    class UI uiClass
    class PA,SA,WA,EA agentClass
    class LLM,WS,SG serviceClass
    class WSP,WSItem,RD modelClass
```

## Architecture Overview

The Deep Research system is a multi-agent architecture designed to perform comprehensive research on any given topic. Here's how it works:

### 1. **User Interface Layer**
- **Gradio Web Interface** (`deep_research.py`): Provides a simple web UI for users to input research queries

### 2. **Orchestration Layer**
- **ResearchManager** (`research_manager.py`): Central orchestrator that coordinates the entire research workflow

### 3. **Agent Layer**
- **Planner Agent** (`planner_agent.py`): Creates a strategic search plan with multiple search queries
- **Search Agent** (`search_agent.py`): Executes web searches and summarizes results
- **Writer Agent** (`writer_agent.py`): Synthesizes search results into a comprehensive report
- **Email Agent** (`email_agent.py`): Formats and sends the final report via email

### 4. **External Services**
- **Local LLM** (Ollama by default, via project-root `.env`): Powers all AI agents for planning, searching, writing, and email formatting
- **Web Search** (Simulated): Currently uses mock data for testing
- **SendGrid API**: Handles email delivery

### 5. **Data Models**
- **WebSearchPlan**: Contains the overall search strategy
- **WebSearchItem**: Individual search queries with reasoning
- **ReportData**: Final report with summary and follow-up questions

## Workflow Process

1. **User Input**: User enters a research query via Gradio interface
2. **Planning**: Planner Agent creates 5 strategic search queries
3. **Search Execution**: Search Agent performs parallel searches and summarizes results
4. **Report Generation**: Writer Agent synthesizes findings into a detailed markdown report
5. **Email Delivery**: Email Agent formats and sends the report via SendGrid
6. **Status Updates**: ResearchManager provides real-time progress updates to the user

## Key Features

- **Asynchronous Processing**: Parallel search execution for efficiency
- **Modular Design**: Each agent has a specific responsibility
- **Error Handling**: Graceful handling of failed searches
- **Real-time Updates**: Progress tracking throughout the process
- **Structured Output**: Pydantic models ensure data consistency
