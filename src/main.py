"""
Main entry point for running the LLM experiment pipeline.

This script orchestrates the entire process:
1. Define the file paths for input and output.
2. Ensures a sample input file exists.
3. Loads the data.
4. Builds the prompts.
5. Runs the Ollama trials.
6. Save the results.
"""

import subprocess
from pathlib import Path
import engine
import input_table_gen


# --- 1. Define Constants and File Paths ---
# Use pathlib to handle paths robustly. This makes the script work
# regardless of where you run it from.


PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
INPUT_FILE_PATH = DATA_DIR / "Experiment-SAMPLE-IN.csv"
OUTPUT_FILE_PATH = DATA_DIR / "Experiment-SAMPLE-OUT.csv"


# --- 2. Main Pipeline Function ---
def run_pipeline():
    """Executes the full experiment pipeline."""
    print("--- Starting LLM Experiment Pipeline ---")

    # Step 1: Generate a sample input file if one doesn't exist
    print(f"Input file not found. Generating sample at '{INPUT_FILE_PATH}'")
    input_table_gen.generate_sample_input_file(INPUT_FILE_PATH)


    # Step 2: Load the input data
    print(f"\nLoading data from: {INPUT_FILE_PATH}")
    input_df = engine.load_input_data(INPUT_FILE_PATH)

    # Step 3: Build prompts for each trial
    print("\nBuilding prompts...")
    trials_with_prompts_df = engine.build_prompts_df(input_df)

    # Step 4: Run the trials against the Ollama API
    print("\nRunning Ollama trials...")
    # results_df = engine.run_ollama_trials(trials_with_prompts_df)
    print(engine.debug_run_single_trial(trials_with_prompts_df.iloc[0]))  # Debug output for first trial

    # Step 5: Save the final results
    print(f"\nSaving results to: {OUTPUT_FILE_PATH}")
    engine.save_results(results_df, OUTPUT_FILE_PATH)

    print("\n--- Pipeline Finished ---")


# --- 3. Script Execution ---
if __name__ == "__main__":
    run_pipeline()