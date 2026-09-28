# Deep Research System

The Deep Research system is a multi-agent architecture designed to perform comprehensive research on any given topic, summarizing findings, and optionally sending them via email.

## Features

-   **Multi-Agent Architecture**: Leverages specialized AI agents for planning, searching, writing, and email generation.
-   **Gradio Web Interface**: Provides an intuitive web UI for users to submit research queries.
-   **Asynchronous Processing**: Executes web searches in parallel for efficient data gathering.
-   **Modular Design**: Each agent (Planner, Search, Writer, Email) has a distinct responsibility, promoting maintainability and scalability.
-   **Error Handling**: Gracefully handles failed searches and other operational issues.
-   **Real-time Updates**: Provides progress updates to the user throughout the research process.
-   **Structured Output**: Utilizes Pydantic models to ensure consistency and structure in data such as search plans and final reports.
-   **Email Delivery**: Formats and sends the final research report via email using the SendGrid API.

## Architecture Overview

The system operates through several interconnected layers:

1.  **User Interface Layer**:
    *   **Gradio Web Interface** (`deep_research.py`): The entry point for users to input research queries.

2.  **Orchestration Layer**:
    *   **ResearchManager** (`research_manager.py`): The central component that orchestrates and coordinates the entire research workflow, from planning to report delivery.

3.  **Agent Layer**:
    *   **Planner Agent** (`planner_agent.py`): Generates a strategic plan of multiple search queries based on the user's initial research request.
    *   **Search Agent** (`search_agent.py`): Executes the planned web searches and summarizes the results from various sources.
    *   **Writer Agent** (`writer_agent.py`): Synthesizes the summarized search results into a comprehensive and well-structured markdown report.
    *   **Email Agent** (`email_agent.py`): Formats the final report into an email and handles its dispatch.

4.  **External Services**:
    *   **Local LLM** (Ollama by default): Powers all AI agents (planning, summarization, writing, email formatting). Configured via project-root `.env` (`LLM_*` / `LOCAL_LLM_*`).
    *   **Web Search** (Simulated): Currently uses mock data for testing purposes.
    *   **SendGrid API**: Utilized by the Email Agent for reliable email delivery.

## Setup

To set up and run the Deep Research system, follow these steps:

1.  **Clone the Repository**:
    ```bash
    git clone <repository_url>
    cd llm_agentic_ai/2_Openai/deep_research
    ```

2.  **Create a Virtual Environment and Install Dependencies**:
    It is recommended to use `uv` for dependency management. If you don't have `uv`, you can install it via `pip install uv`.
    ```bash
    uv venv
    uv pip install -r requirements.txt
    ```
    Alternatively, using `pip`:
    ```bash
    python -m venv venv
    ./venv/Scripts/activate # On Windows
    source venv/bin/activate # On macOS/Linux
    pip install -r requirements.txt
    ```

## Langfuse Setup (Optional for LLM Tracing)

If you wish to enable LLM tracing with Langfuse, please follow these steps. This will allow you to monitor and debug the LLM calls made by the agents, providing detailed insights into their operations.

### 1. Run Langfuse Locally (using Docker)

Langfuse can be easily set up locally using Docker. If you don't have Docker installed, please follow the instructions on the [official Docker website](https://www.docker.com/get-started).

To start the Langfuse server and database locally, run the following command in your terminal:

```bash
docker run --pull always -p 3000:3000 -p 5000:5000 -it ghcr.io/langfuse/langfuse
```

Once started, you can access the Langfuse UI in your browser at `http://localhost:3000`.

For more details, refer to the [Langfuse GitHub repository](https://github.com/langfuse/langfuse).

### 2. Extract Langfuse Keys

After setting up and running Langfuse locally, you will need to extract the `Secret Key` and `Public Key` to configure your application.

1.  **Access Langfuse UI**: Open your web browser and navigate to `http://localhost:3000`.
2.  **Create a Project**: If it's your first time, you might need to create a new project.
3.  **Go to Settings**: In the Langfuse UI, navigate to the **Settings** section.
4.  **Find API Keys**: Look for an "API Keys" or "Project Settings" tab where your `Secret Key` and `Public Key` will be displayed. Copy these values.

### 3. Configure Environment Variables

Prefer the **project-root** `.env` (same file used by the labs). Example for Ollama + optional Langfuse / email:

```
# Local LLM (Ollama Docker — see ../../ollama/README.md)
LOCAL_LLM_BASE_URL=http://localhost:11434/v1
LOCAL_LLM_API_KEY=ollama
LOCAL_LLM_MODEL=llama3.2:latest

# deep_research also accepts LLM_* (falls back to LOCAL_LLM_* if unset)
LLM_BASE_URL=http://localhost:11434/v1
LLM_API_KEY=ollama
LLM_MODEL=llama3.2:latest

SENDGRID_API_KEY=

LANGFUSE_SECRET_KEY="YOUR_LANGFUSE_SECRET_KEY"
LANGFUSE_PUBLIC_KEY="YOUR_LANGFUSE_PUBLIC_KEY"
LANGFUSE_HOST=http://localhost:3000
```

*   Start Ollama first: `cd ollama && docker compose up -d` then `docker exec ollama ollama pull llama3.2`.
*   Change `LLM_MODEL` / `LOCAL_LLM_MODEL` to switch models; agents read this from `llm_client.py`.
*   Replace `SENDGRID_API_KEY` and Langfuse keys if you use those features.

## How to Run

To start the Deep Research web interface, navigate to the `2_Openai/deep_research/` directory and run the `deep_research.py` file:

```bash
uv run deep_research.py
```
or if using pip:
```bash
python deep_research.py
```

This will launch a Gradio web interface in your browser, where you can input your research queries and view the generated reports.
