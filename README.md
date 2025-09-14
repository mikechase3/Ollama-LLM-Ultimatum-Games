# Ollama-LLM-Ultimatum-Games
[//]: # (Better title: LLM Game Theory Sandbox? TODO: change project title.)

## Project Overview
* Provide a self-contained Docker (Dockher... I hardly know her) env for conducting LLM behavioral experiments.
  * Ultimatum Game
  * With LLMs.
* Must be easily run/transferrable to secure, air-gapped systems.

Researchers can define experimental trials in an Excel file, run them against locally hosted LLMs in Ollama
and receive pd.DataFrame (or excel/csv) with the results for analysis.

A streamlit web app provides a friendly interface to visualize results & manage the workflow.

## Usage Guide
* **Prerequisites**: Docker Engine/Compose must be installed/running.

### Running The Experiment
1. Prepare the input file
   1. Open the `data/input_trials.xlsx` file
   2. Edit the rows to define experimental conditions (e.g. change pot, split, model, temperature)
   3. Save the file.
1. Launch the env
   1. Open a terminal in the project's root directory
   2. Run `docker compose up -d`
1. Launch web interface
   1. Launch a browser & goto `http://localhost:8501`
   1. Verify streamlit dashboard loaded the `input_trials.xlsx` file.
   1. Click the "run experiment" button to start the process.
1. Get the resultws
   1. Results will be displayed in browser/streamlit
   1. A new file named `data/exp##-results.xlsx` will be created in the project folder.
   1. Contains detailed output for each trial. 

## Development Guide
I want to define the pipeline here later so I remember what & how I did it.

* For Air-Gapped Networks, run `pip download -r requirements.txt -d ./packages` on the online computer's terminal