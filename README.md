# Ollama-LLM-Ultimatum-Games
[//]: # (Better title: LLM Game Theory Sandbox? TODO: change project title.)

## Architecture
```
+--------------------------------------------------------------------------------+
| HOST MACHINE (Your Computer - localhost)                                       |
|                                                                                |
|  +---------------------------+       +---------------------------------------+ |
|  | src/main.py (Command Line)|       | src/dashboard.py (Streamlit UI)       | |
|  | - Runs experiment script  |       | - Runs via 'streamlit run' command    | |
|  +---------------------------+       +---------------------------------------+ |
|               |                                         |                      |
| (via docker exec)                                       |                      |
|               |                                (Browser access)                |
|               |              +----------------------------------------------+  |
|               |              |                DOCKER NETWORK                |  |
|               |              |                                              |  |
|               |              |  +-----------------------------------------+ |  |
|               |              |  | Python App Container (python-dev)       | |  |
|               +------------->|  |              |                          | |  |
|                              |  | +--------------+                        | |  |
|                              |  | | src/engine.py|                        | |  |
|                              |  | +--------------+                        | |  |
|                              |  |       |                                 | |  |
|                              |  | (API Call via http://ollama:11434)      | |  |
|       localhost:8501 --------+--|----> | (Port 8501)                      | |  |
|                              |  |       v                                 | |  |
|                              |  +-------|---------------------------------+ |  |
|                              |          |                                   |  |
|                              |  +-------|---------------------------------+ |  |
|                              |  | Ollama Service Container (ollama)       | |  |
|       localhost:11434 -------+--|----->| API listens on Port 11434        | |  |
|                              |  | ---- +----------------------------------+ |  |
|                              |          ^                                   |  |
|                              |  +-------|---------------------------------+ |  |
|                              |  | OpenWebUI Container (webui)              | | |
|       localhost:3000 --------+--|----->| UI on Port 8080                   | | |
|                              |  |      | (Manual testing & model mgmt)     | | |
|                              |  |      | (API Call via http://ollama:11434)| | |
|                              |  +-----------------------------------------+ |  |
|                              +----------------------------------------------+  |
|                                                                                |
+--------------------------------------------------------------------------------+
```

## Project Overview
* Provide a self-contained Docker environment for conducting LLM behavioral experiments.
  * Ultimatum Game
  * With LLMs
* Must be easily run/transferable to secure, air-gapped systems.

Researchers can define experimental trials in an Excel file, run them against locally hosted LLMs in Ollama,
and receive `pd.DataFrame` (or Excel/CSV) with the results for analysis.

A Streamlit web app provides a friendly interface to visualize results and manage the workflow.

## Usage Guide
* Prerequisites: Docker Engine/Compose installed and running, or use a local Python virtual environment.

### Run Options

You can run this project in two primary ways, depending on your development setup.

#### Option A: Native on Ubuntu (recommended for local dev)
This starts only the infrastructure services (e.g., Ollama and OpenWebUI) via Docker and runs the app locally in your host Python environment.

1. Start infra with Docker Compose
   - From the project root:
     - `docker compose -f docker-compose-infra.yml up -d`
   - This brings up the Ollama API on `http://localhost:11434` and OpenWebUI on `http://localhost:3000`.

2. Create and activate a virtual environment
   - `python3 -m venv .venv`
   - `source .venv/bin/activate`
   - `pip install -r requirements.txt`

3. Generate the input trials table (one-model dev tables)
   - `python src/main.py`
   - Edit `data/input_trials.xlsx` to set pot, split, model, temperature, etc.

4. Run the Streamlit dashboard locally
   - `streamlit run src/dashboard.py`
   - Open `http://localhost:8501`
   - Click “Run Experiment” to execute.

5. Results
   - Displayed in the Streamlit UI.
   - An Excel file `data/exp##-results.xlsx` will be created with detailed outputs for each trial.

Notes
- The development run configuration generates tables using a single model at a time. Since the current development target is a CPU-only machine, there’s no need to spin up multiple models concurrently. This keeps iteration fast and resource usage low.

#### Option B: All-in-Docker (containerized app + infra)
If you prefer running the entire stack in containers:

1. From the project root, start the default stack:
   - `docker compose up -d`
   - Streamlit UI: `http://localhost:8501`
   - Ollama API: `http://localhost:11434`
   - OpenWebUI: `http://localhost:3000`

2. Alternatively, for a production-leaning stack:
   - `docker compose -f docker-compose-production.yml up -d`
   - `docker compose -f docker-compose-production.yml down` to shutdown.

3. Manage input/output files by editing or copying files inside the mounted volumes as defined in the compose files.

### Compose Files Overview
- `docker-compose-infra.yml`: infra-only for local dev on Ubuntu (Ollama, OpenWebUI). Use with a local `.venv` for the app.
- `docker-compose.yml`: default dev stack (containers for app and infra together).
- `docker-compose-production.yml`: production-leaning configuration with tighter settings.

### Why native dev instead of Docker for the app?
During development, PyCharm had issues talking to the newest Docker Engine API. After trying a `daemon.json` tweak, PyCharm still couldn’t reliably connect/build and use the container as the interpreter. So, for now: f*** it, we’re doing it live — the app runs natively in a `.venv`, while Docker only runs the infra.

If/when PyCharm resolves Docker API compatibility, the full-container dev experience can be restored.

## Development Notes
I want to define the pipeline here later so I remember what and how I did it.

Air‑gapped tip: On an online machine, pre-download packages for offline install

```
pip download -r requirements.txt -d ./packages
```