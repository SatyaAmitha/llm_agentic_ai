flowchart LR
  U["User"] --> UI["Gradio ChatInterface"] --> CHAT["chat(message, history)"]

  subgraph "Setup"
    ENV["load_dotenv(override=True)"]
    KEYS["ENV: LOCAL_LLM_BASE_URL, LOCAL_LLM_API_KEY, LOCAL_LLM_MODEL, PUSHOVER_USER, PUSHOVER_TOKEN"]
    CLIENT["OpenAI client (Ollama / local LLM from .env)"]
    ENV --> KEYS --> CLIENT
  end

  subgraph "Context Building"
    PDF["Read me/Profile.pdf via PdfReader"]
    TXT["Read me/summary.txt"]
    PROMPT["Compose system_prompt (persona + summary + LinkedIn)"]
    PDF --> PROMPT
    TXT --> PROMPT
  end

  CHAT --> PROMPT

  subgraph "Tools & Schemas"
    SCHEMAS["JSON tool schemas → tools list"]
    T1["record_user_details(email, name?, notes?)"]
    T2["record_unknown_question(question)"]
    T1 -. contributes .-> SCHEMAS
    T2 -. contributes .-> SCHEMAS
  end

  CHAT --> LLM["openai.chat.completions.create(model, messages, tools)"]
  LLM --> DECIDE{"finish_reason == 'tool_calls'?"}

  subgraph "Tool Handling Loop"
    HANDLE["handle_tool_calls(tool_calls)"]
    DISPATCH["Dispatch by function name (globals)"]
    RESULTS["Append tool results to messages"]
    DECIDE -- Yes --> HANDLE --> DISPATCH
    DISPATCH -->|T1 or T2| RESULTS --> LLM
  end

  subgraph "Notifications"
    PUSH["push(message) → POST to Pushover API"]
    T1 --> PUSH
    T2 --> PUSH
  end

  DECIDE -- No --> RESP["Return assistant message"] --> UI
