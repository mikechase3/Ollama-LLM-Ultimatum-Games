Run natively on Ubuntu (recommended for dev)

Prerequisites:
- Docker Engine + Docker Compose
- Python 3.10+ and venv

Steps:
1. Start infra (Ollama + OpenWebUI):
   - docker compose up -d ollama webui
   - Ollama API: http://localhost:11434
   - OpenWebUI: http://localhost:3000

2. Create and activate a virtual environment:
   - python3 -m venv .venv
   - source .venv/bin/activate
   - pip install -r requirements.txt

3. Generate an input table (example):
   - python src/main.py

4. Run the Streamlit dashboard locally:
   - streamlit run src/dashboard.py
   - Open http://localhost:8501

5. PyCharm run configs (optional):
   - See screenshots in docs/images/PycharmMainConfig.png and docs/images/StreamlitShellConfig.png

Notes:
- CPU-only is fine for quick iteration.
- Models live in ./ollama-data and persist between restarts.