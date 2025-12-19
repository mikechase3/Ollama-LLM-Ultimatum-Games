Run everything in containers (dashboard + infra)

Services in docker-compose.yml:
- ollama — LLM server (port 11434)
- webui — OpenWebUI (port 3000)
- dashboard — Streamlit app (port 8501)

Quick start:
1. docker compose up -d
2. Open:
   - Streamlit: http://localhost:8501
   - Ollama API: http://localhost:11434
   - OpenWebUI: http://localhost:3000

Edit locally, run in container:
- Your working tree is bind-mounted into the dashboard container, so changes in src/ reflect live.
- You can keep using your local IDE/.venv for tooling while the app is served from Docker.

GPU (optional):
- To enable GPU for Ollama, install NVIDIA Container Toolkit and add the appropriate runtime/devices to the `ollama` service. See docker-compose-production.yml for an example configuration.

Pre-pulling models:
- Easiest: `docker exec -it ollama ollama pull phi3:latest`
- Or bake a helper service similar to the (deprecated) docker-compose-infra.yml example.

Stopping:
- docker compose down