
# Agentic AI Foundations
This repository serves as a foundational exploration into Agentic AI, focusing on Large Language Models (LLMs) and their application in building intelligent agents. It provides a structured environment to learn, experiment, and develop with various Agentic AI patterns and tools.

### What is Agentic AI? ###
Agentic AI refers to the design and implementation of AI systems that can reason, plan, act, and learn autonomously within complex environments. These systems often leverage LLMs to perform tasks, make decisions, and interact with the world, moving beyond simple prompt-response interactions to more sophisticated, goal-oriented behaviors.

### Getting Started ###
To get this repository up and running, follow these steps:

#### Prerequisites ####
*   **Python 3.9+**: Ensure you have a compatible version of Python installed.
*   **uv**: A fast Python package installer and resolver. Install it via pip:
    ```bash
    pip install uv
    ```

#### Setup and Installation ####
1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/SatyaAmitha/llm_agentic_ai.git
    cd llm_agentic_ai
    ```
2.  **Create and Activate a Virtual Environment**:
    Using `uv` (recommended):
    ```bash
    uv venv
    # Windows (PowerShell / CMD):
    .venv\Scripts\activate
    # macOS / Linux:
    # source .venv/bin/activate
    ```
    Or with standard Python:
    ```bash
    python -m venv .venv
    .venv\Scripts\activate          # Windows
    # source .venv/bin/activate     # macOS / Linux
    ```
3.  **Install Dependencies**:
    ```bash
    uv sync
    # or: pip install -r requirements.txt
    ```
4.  **Create `.env`** in the project root (see below). Never commit this file.

#### Environment Variables ####
Create a `.env` file in the **project root** (never commit it). Labs and apps read LLM settings from here.

**Default local LLM (Ollama)** — used by `1_foundations` and `2_Openai` notebooks:
```
LOCAL_LLM_BASE_URL=http://localhost:11434/v1
LOCAL_LLM_API_KEY=ollama
LOCAL_LLM_MODEL=llama3.2:latest
```

Optional keys (only if a lab needs them):
```
GOOGLE_API_KEY=...
SENDGRID_API_KEY=...
PUSHOVER_USER=...
PUSHOVER_TOKEN=...
OPENAI_API_KEY=...
```

Each notebook has one **LLM SETUP** cell that loads these values; later cells reuse `openai` / `model_name` (or `local_model`). Change the model in `.env` or that setup cell only.

#### Local LLM (Ollama via Docker) ####
```bash
cd ollama
docker compose up -d
docker compose exec ollama ollama pull llama3.2
```
See `ollama/README.md` and `ollama/docker-compose.yml`.
#### Jupyter Notebook Setup ####
To ensure your Jupyter notebooks use the correct virtual environment, install an IPython kernel linked to your new environment:
1.  **Install IPython Kernel**:
    ```bash
    pip install ipykernel
    python -m ipykernel install --user --name=llm_agentic_ai --display-name="Python (llm_agentic_ai)"
    ```
2.  **Open Jupyter Lab/Notebook**:
    ```bash
    jupyter lab  # or jupyter notebook
    ```
3.  **Select the Kernel**: In your Jupyter environment, open any notebook from the `1_foundations` directory and select the `Python (llm_agentic_ai)` kernel from the kernel dropdown menu.

### Project Organization and Execution ###
- `1_foundations` — core Agentic AI labs + Gradio `app.py` (default: Ollama from `.env`)
- `2_Openai` — OpenAI Agents SDK labs + `deep_research/`
- `ollama/` — Docker Compose for the local Ollama server

To execute the notebooks:
1.  Start Ollama (`cd ollama && docker compose up -d`) and confirm `.env` has `LOCAL_LLM_*`.
2.  Open notebooks in order (`1_lab.ipynb`, `2_lab.ipynb`, …).
3.  Select the `Python (llm_agentic_ai)` kernel.
4.  Run the **LLM SETUP** cell first, then the rest.
