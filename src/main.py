"""
Main entry point for running the LLM experiment pipeline.

This script orchestrates the entire process:
1. Define the file paths for input and output.
2. Ensures a sample input file exists.
3. Loads the data.
4. Builds the prompts.
5. Runs the Ollama trials.
6. Saves the results.
"""

from pathlib import Path
from src import core

# --- 1. Define Constants and File Paths ---
# Use pathlib to handle paths robustly. This makes the script work
# regardless of where you run it from.
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
INPUT_FILE_PATH = DATA_DIR / "input_trials.csv"
OUTPUT_FILE_PATH = DATA_DIR / "output_trials.csv"


# --- 2. Main Pipeline Function ---
def main():
    """Executes the full experiment pipeline."""
    print("--- Starting LLM Experiment Pipeline ---")

    # Step 1: Generate a sample input file if one doesn't exist
    if not INPUT_FILE_PATH.exists():
        print(f"Input file not found. Generating sample at '{INPUT_FILE_PATH}'")
        core.generate_sample_input_file(INPUT_FILE_PATH)

    # Step 2: Load the input data
    print(f"\nLoading data from: {INPUT_FILE_PATH}")
    input_df = core.load_input_data(INPUT_FILE_PATH)

    # Step 3: Build prompts for each trial
    print("\nBuilding prompts...")
    trials_with_prompts_df = core.build_prompts_df(input_df)

    # Step 4: Run the trials against the Ollama API
    print("\nRunning Ollama trials...")
    results_df = core.run_ollama_trials(trials_with_prompts_df)

    # Step 5: Save the final results
    print(f"\nSaving results to: {OUTPUT_FILE_PATH}")
    core.save_results(results_df, OUTPUT_FILE_PATH)

    print("\n--- Pipeline Finished ---")


# --- 3. Script Execution ---
if __name__ == "__main__":
    main()