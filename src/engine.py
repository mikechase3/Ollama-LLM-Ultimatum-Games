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

# --- 1. Data Generation ---> moved to input_table_gen.py ---

# --- 2. Data Loading ---

def load_input_data(input_path: Path) -> pd.DataFrame:
    """
    Loads the experimental trials from a specified CSV or Excel file.

    Args:
        input_path (Path): The path to the input file.

    Returns:
        pd.DataFrame: A DataFrame containing the experimental trials.
    """
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    df = pd.read_csv(input_path)

    # Validate required columns
    required_cols = ['role', 'pot', 'offer', 'base-prompt']
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")
    return df
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
    df = input_df.copy()

    def format_prompt(row):
        if row['role'] == 'proposer':
            return row['base-prompt'].format(pot=row['pot'])
        elif row['role'] == 'receiver':
            remainder = row['pot'] - row['offer']  # Calculate outside format()
            return row['base-prompt'].format(
                pot=row['pot'],
                offer=row['offer'],
                remainder=remainder  # Pass as new parameter
            )
        else:
            raise ValueError(f"Invalid role: {row['role']}")

    df['final-prompt'] = df.apply(format_prompt, axis=1)  # axis 1 for row-wise operations.

    return df

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
