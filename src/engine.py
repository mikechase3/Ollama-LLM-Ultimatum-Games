"""
Core logic for the LLM experiment runner.

This script contains the main pipeline functions for generating sample data,
loading input trials, building prompts, running Ollama experiments,
and saving the results.
"""

import pandas as pd
from pathlib import Path
import numpy as np
from typing import List, Dict, Any

# --- 1. Data Generation ---
#
# def generate_sample_input_file(output_path: Path) -> None:
#     """
#     Generates a sample CSV file with experiment parameters and saves it to the specified path.
#     """
#     num_rows = 20  # aka trials
#     # num_columns = 33
#
#     # Define supported models
#     models = ["phi3:mini", "phi3:latest", "mixtral:8x7b", "dolphin-llama3:8b"]
#
#     # Define DataFrame columns (matching OpenWebUI parameter names where possible)
#     columns = [
#         # --- Experimental Setup Metadata ---
#         "experiment-id",     # str, experiment grouping
#         "trial-id",          # str, unique trial identifier
#         "game",              # str, task/game type
#         "role",              # str, {'proposer', 'receiver'}
#         "pot",               # float, total resources in the game
#         "offer",             # float, proposed split value
#         "model",             # str, model name
#
#         # --- Prompts and Instructions ---
#         "base-prompt",       # str, researcher-provided or default
#         "modified-prompt",   # str, todo: edited version of base-prompt
#
#         # --- Creative / Behavioral Parameters ---
#         "temperature",       # float, [0.0-2.0], randomness/creativity
#         "top_p",             # float, [0.0-1.0], nucleus sampling
#         "top_k",             # int, [1+], top-k token filtering
#         "min_p",             # float, [0.0-1.0], minimum probability
#         "repeat_penalty",    # float, [1.0-2.0], discourages repetition
#         "frequency_penalty", # float, [0.0-2.0], discourages frequent tokens
#         "presence_penalty",  # float, [0.0-2.0], encourages novelty
#         "tfs_z",             # float, tail-free sampling parameter
#         "mirostat",          # int, {0,1,2}, adaptive sampling mode
#         "mirostat_eta",      # float, learning rate for mirostat
#         "mirostat_tau",      # float, target surprise for mirostat
#
#         # --- Technical / System Parameters ---
#         "seed",              # int, reproducibility seed (or not-applicable)
#         "repeat_last_n",     # int, tokens considered for repeat_penalty
#         "reasoning_effort",  # float or str, not widely supported
#         "logit_bias",        # str or dict, bias token probabilities
#         "num_ctx",           # int, context window size
#         "max_tokens",        # int, max tokens to generate
#         "stop_sequence",     # str or list, stopping condition
#         "use_mmap",          # bool, memory map flag
#         "use_mlock",         # bool, lock model into RAM
#         "num_keep",          # int, tokens to keep from start of context
#         "num_predict",       # int, number of tokens to predict
#     ]
#
#     # Fill with defaults / placeholders
#     table = pd.DataFrame({
#         "experiment-id": ["EXP00"] * num_rows,
#         "trial-id": [f"trial_{i+1}" for i in range(num_rows)],
#         "game": ["ultimatum"] * num_rows,
#         "role": np.random.choice(["proposer", "receiver"], size=num_rows),
#         "pot": [100] * num_rows,
#         "offer": [50.0] * num_rows,
#         "model": np.random.choice(models, size=num_rows),
#
#         "base-prompt": ["Placeholder for researcher-provided question."] * num_rows,
#         "modified-prompt": ["todo"] * num_rows,
#
#         "temperature": [0.8] * num_rows,
#         "top_p": [0.9] * num_rows,
#         "top_k": [40] * num_rows,
#         "min_p": [0.0] * num_rows,
#         "repeat_penalty": [1.1] * num_rows,
#         "frequency_penalty": [0.0] * num_rows,
#         "presence_penalty": [0.0] * num_rows,
#         "tfs_z": [1.0] * num_rows,
#         "mirostat": [0] * num_rows,
#         "mirostat_eta": [0.1] * num_rows,
#         "mirostat_tau": [5.0] * num_rows,
#
#         "seed": [42] * num_rows,  # Arbitrary, I like it from Hitchhiker’s Guide
#         "repeat_last_n": [64] * num_rows,
#         "reasoning_effort": [""] * num_rows,  # left blank
#         "logit_bias": [""] * num_rows,        # left blank
#         "num_ctx": [2048] * num_rows,
#         "max_tokens": [512] * num_rows,
#         "stop_sequence": [""] * num_rows,     # left blank
#         "use_mmap": [True] * num_rows,
#         "use_mlock": [False] * num_rows,
#         "num_keep": [0] * num_rows,
#         "num_predict": [128] * num_rows,
#     }, columns=columns)
#
#     table.to_csv(output_path, index=False)
#     print(f"Sample input file saved to: {output_path}")

# --- 2. Data Loading ---

def load_input_data(input_path: Path) -> pd.DataFrame:
    """
    Loads the experimental trials from a specified CSV or Excel file.

    Args:
        input_path (Path): The path to the input file.

    Returns:
        pd.DataFrame: A DataFrame containing the experimental trials.
    """
    # This will contain logic to read the CSV/Excel and validate it.
    print(f"Placeholder: Will load data from '{input_path}'")
    # Return an empty DataFrame for now to allow the pipeline to run.
    return pd.DataFrame()

# --- 3. Prompt Engineering ---

def build_prompts_df(input_df: pd.DataFrame) -> pd.DataFrame:
    """
    Takes the input DataFrame and adds a new column with the fully constructed
    prompt for each trial, based on the 'role', 'pot', and other variables.

    Args:
        input_df (pd.DataFrame): The DataFrame loaded from the input file.

    Returns:
        pd.DataFrame: The DataFrame with an added 'final_prompt' column.
    """
    # This will contain the logic for the PromptBuilder class we discussed.
    print("Placeholder: Will build final prompts for each trial.")
    input_df['final_prompt'] = "This is a placeholder prompt."
    return input_df

# --- 4. Experiment Execution ---

def run_ollama_trials(trials_with_prompts_df: pd.DataFrame) -> pd.DataFrame:
    """
    Iterates through each trial, sends a request to the Ollama API with the
    specified parameters, and captures the full response.

    Args:
        trials_with_prompts_df (pd.DataFrame): The DataFrame containing the
                                               final prompts and all parameters.

    Returns:
        pd.DataFrame: A new DataFrame containing the results of all trials,
                      including all inputs and all output metadata.
    """
    # This is the core engine that will call the Ollama API.
    print("Placeholder: Will run all trials against the Ollama API.")
    # Return an empty DataFrame for now.
    return pd.DataFrame()

# --- 5. Saving Results ---

def save_results(results_df: pd.DataFrame, output_path: Path) -> None:
    """
    Saves the final results DataFrame to a specified CSV or Excel file.

    Args:
        results_df (pd.DataFrame): The DataFrame containing the experiment results.
        output_path (Path): The file path where the results should be saved.
    """
    # This will contain the logic to save the results.
    print(f"Placeholder: Will save results to '{output_path}'")
    pass
