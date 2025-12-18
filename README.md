# Ollama-LLM-Ultimatum-Games
[//]: # (Better title: LLM Game Theory Sandbox? TODO: change project title.)

## OpenWebUI Login
me@mchase.me / `password`

## Architecture
See docs/architecture.md for the full ASCII diagram of the stack.

## Project Overview
* Provide a self-contained Docker environment for conducting LLM behavioral experiments.
  * Ultimatum Game
  * With LLMs
* Must be easily run/transferable to secure, air-gapped systems.

Researchers can define experimental trials in an Excel file, run them against locally hosted LLMs in Ollama,
and receive `pd.DataFrame` (or Excel/CSV) with the results for analysis.

A Streamlit web app provides a friendly interface to visualize results and manage the workflow.

## Usage Guide
Quick starts were moved into dedicated docs:
- docs/ubuntu-native.md — run app on Ubuntu natively (.venv) with Docker for infra
- docs/containers.md — run entire stack in containers (dashboard + infra)

### Why native dev instead of Docker for the app?
PyCharm had issues connecting to Docker as a remote interpreter on this machine (upstream bug). Until that’s fixed, you can either:
- run the dashboard in Docker and continue editing locally via bind mounts, or
- run everything natively in a `.venv` while Docker only provides infra.

See docs/ubuntu-native.md and docs/containers.md for details, including example PyCharm run configurations.

## Development Notes
I want to define the pipeline here later so I remember what and how I did it.

Air‑gapped tip: On an online machine, pre-download packages for offline install

```
pip download -r requirements.txt -d ./packages
```

