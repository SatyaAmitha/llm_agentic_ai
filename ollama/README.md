# Ollama (local LLM)

Docker Compose setup for the project's default local model.
Labs and apps read settings from the **project-root** `.env`.

## Quick start

From this folder (`ollama/`):

```bash
# 1. Start Ollama
docker compose up -d

# 2. Pull the default model (first time only)
docker compose exec ollama ollama pull llama3.2

# 3. Check it's running
docker compose ps
docker compose exec ollama ollama list
```

API (OpenAI-compatible): **http://localhost:11434/v1**

## Useful commands

```bash
docker compose up -d          # start
docker compose down           # stop (keeps models)
docker compose down -v        # stop and delete model volume
docker compose logs -f        # follow logs
docker compose exec ollama ollama list
docker compose exec ollama ollama pull <model>
```

## Project `.env` (repo root)

```
LOCAL_LLM_BASE_URL=http://localhost:11434/v1
LOCAL_LLM_API_KEY=ollama
LOCAL_LLM_MODEL=llama3.2:latest
```

Change `LOCAL_LLM_MODEL` to switch models — notebooks use one **LLM SETUP** cell that reads these values.
