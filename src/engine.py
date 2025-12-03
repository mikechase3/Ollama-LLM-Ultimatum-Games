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
import ollama
import warnings


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
    # Offer to preview and/or save the intermediary DataFrame before Step 4 (Ollama trials)
    maybe_preview_and_save_intermediate_df(df)
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


    # Helper: build Ollama options safely from a data row
    def _build_options(row: Dict[str, Any]) -> Dict[str, Any]:
        # Map known columns to Ollama options; include only if present and not null
        def present(key: str) -> bool:
            return (key in row) and (row[key] is not None) and (not (isinstance(row[key], float) and np.isnan(row[key]))) and (row[key] != "")

        opts: Dict[str, Any] = {}
        mapping = [
            ("seed", "seed"),
            ("temperature", "temperature"),
            ("top_p", "top_p"),
            ("top_k", "top_k"),
            ("repeat_penalty", "repeat_penalty"),
            ("presence_penalty", "presence_penalty"),
            ("frequency_penalty", "frequency_penalty"),
            ("mirostat", "mirostat"),
            ("mirostat_tau", "mirostat_tau"),
            ("mirostat_eta", "mirostat_eta"),
            ("num_ctx", "num_ctx"),
            ("num_predict", "num_predict"),
            ("num_keep", "num_keep"),
            ("tfs_z", "tfs_z"),
            ("min_p", "min_p"),
            ("repeat_last_n", "repeat_last_n"),
        ]
        for col, opt_key in mapping:
            if present(col):
                opts[opt_key] = row[col]

        # Stop sequences: support string or list
        if present("stop_sequence"):
            stop_val = row["stop_sequence"]
            if isinstance(stop_val, str):
                # Allow pipe-separated list, else single stop
                parts = [s for s in [p.strip() for p in stop_val.split("|")] if s]
                opts["stop"] = parts if len(parts) > 1 else parts
            elif isinstance(stop_val, (list, tuple)):
                opts["stop"] = list(stop_val)

        # Booleans that Ollama accepts
        for b in ["use_mmap", "use_mlock"]:
            if present(b):
                opts[b] = bool(row[b])

        return opts

    # Iterate over trials and call Ollama
    results: List[Dict[str, Any]] = []
    trials: List[Dict[str, Any]] = trials_with_prompts_df.to_dict(orient="records")

    for idx, row in enumerate(trials, start=1):
        base_out: Dict[str, Any] = dict(row)  # start with original inputs
        try:
            model = row.get("model")
            prompt = row.get("final-prompt")
            system_prompt = row.get("system-prompt", "")
            options = _build_options(row)

            if not model or not prompt:
                raise ValueError("Missing required fields for Ollama call: 'model' and/or 'final-prompt'.")

            response = ollama.generate(
                model=model,
                prompt=prompt,
                system=system_prompt or None,
                options=options if options else None,
                stream=False,
            )

            # Merge key response fields
            base_out.update({
                "llm_status": "ok",
                "llm_model": response.get("model"),
                "llm_created_at": response.get("created_at"),
                "llm_response": response.get("response"),
                "llm_done": response.get("done"),
                "llm_done_reason": response.get("done_reason"),
                "llm_eval_count": response.get("eval_count"),
                "llm_eval_duration_ns": response.get("eval_duration"),
                "llm_prompt_eval_count": response.get("prompt_eval_count"),
                "llm_prompt_eval_duration_ns": response.get("prompt_eval_duration"),
                "llm_total_duration_ns": response.get("total_duration"),
            })

            # Some versions include token/metadata under "info"; if present, flatten a few
            info = response.get("info") if isinstance(response, dict) else None
            if isinstance(info, dict):
                for k, v in info.items():
                    base_out[f"llm_info_{k}"] = v

        except Exception as e:
            base_out.update({
                "llm_status": "error",
                "llm_error": str(e),
            })

        results.append(base_out)

    return pd.DataFrame(results)


def debug_run_single_trial(trial: Dict[str, Any]) -> Dict[str, Any]:
    """ Runs a single trial for debugging purposes"""
    # Define the parameters
    params = {
        "model": "phi:latest",
        "prompt": "Hello, world!",
        "images": [],
        "format": "",
        "options": {
            "seed": 123,
            "temperature": 0.7,
            "top_p": 0.9,
            "top_k": 40,
            "num_predict": 128,
            "repeat_penalty": 1.1,
            "presence_penalty": 0.0,
            "frequency_penalty": 0.0,
            "stop": [],
            "mirostat": 0,
            "mirostat_tau": 5.0,
            "mirostat_eta": 0.1,
            "num_ctx": 2048,
            "num_batch": 1,
            "num_keep": 0,
            "num_gpu": 0,
            "main_gpu": 0,
            "low_vram": False,
            "f16_kv": True,
            "logits_all": False,
            "vocab_only": False,
            "use_mmap": True,
            "use_mlock": False,
            "embedding_only": False,
            "rope_frequency_base": 10000.0,
            "rope_frequency_scale": 1.0,
            "num_thread": 8,
        },
        "system": "",  # System prompt instructions
        "template": "",  # Wrapper for formatting the final prompt. I'm doing it manually?
        "context": [],  # auxiliary inputs? Not used here.
        "stream": False,
        "raw": False,  # if true, returns token arrays, logits, metadata.
        "keep_alive": 0,  # keep the http/tcp connection open.
    }

    # Generate with Ollama
    response = ollama.generate(**params)  # modified from chat -> generate

    # Show the full results dict
    print(response)
    return response


# --- 5. Saving Results ---

def save_results(results_df: pd.DataFrame, output_path: Path) -> None:
    """
    Saves the final results DataFrame to a specified CSV or Excel file.

    Args:
        results_df (pd.DataFrame): The DataFrame containing the experiment results.
        output_path (Path): The file path where the results should be saved.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if results_df is None or results_df.empty:
        warnings.warn("save_results called with empty results DataFrame; creating empty file.")
    results_df.to_csv(output_path, index=False)
    print(f"Results saved to: {output_path}")


# --- Utility: Optional preview and save of intermediary DataFrame (Step 3) ---
def maybe_preview_and_save_intermediate_df(df: pd.DataFrame, default_filename: str = "Intermediate-Prompts.csv") -> None:
    """
    Provides interactive console prompts to:
    - Preview the intermediary DataFrame (head with all columns)
    - Preview a compact view with just pot, offer, and final-prompt
    - Optionally save the full intermediary DataFrame to CSV before Step 4 runs.

    Args:
        df (pd.DataFrame): The intermediary DataFrame (output of Step 3).
        default_filename (str): Default filename for saving the CSV.
    """
    # All prompts should be resilient to non-interactive execution
    def _ask(prompt: str) -> str:
        try:
            return input(prompt).strip().lower()
        except Exception:
            # Non-interactive environment; skip further interaction
            raise

    # Move previous debug prints here as an optional preview
    try:
        show_head = _ask("Do you want to preview the intermediary DataFrame head (all columns)? [y/N]: ")
    except Exception:
        return

    if show_head in ("y", "yes"):
        # Show head with all columns for visibility, without permanently changing global options
        with pd.option_context('display.max_columns', None, 'display.width', 200):
            print("Intermediary DataFrame (head):")
            print(df.head())

    # Offer a compact preview focusing on key columns
    try:
        show_compact = _ask("Do you want to preview a compact view (pot, offer, final-prompt)? [y/N]: ")
    except Exception:
        return

    if show_compact in ("y", "yes"):
        cols = [c for c in ['pot', 'offer', 'final-prompt'] if c in df.columns]
        if cols:
            compact = df.loc[:, cols].head()
            with pd.option_context('display.max_columns', None, 'display.width', 200):
                print("Compact intermediary view (head):")
                print(compact)
        else:
            print("Compact view unavailable: required columns not found.")

    # Finally, offer to save the full intermediary DataFrame
    try:
        save_answer = _ask("Do you want to save the intermediary DataFrame to CSV before running trials? [y/N]: ")
    except Exception:
        return

    if save_answer not in ("y", "yes"):
        return

    # Determine default save path under the project data directory
    project_root = Path(__file__).parent.parent
    data_dir = project_root / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    default_path = data_dir / default_filename

    try:
        try:
            path_str_raw = input(f"Enter a path to save the CSV (press Enter to use default: {default_path}): ")
            path_str = path_str_raw.strip()
        except Exception:
            path_str = ""

        save_path = Path(path_str) if path_str else default_path
        # Ensure parent directory exists
        save_path.parent.mkdir(parents=True, exist_ok=True)

        df.to_csv(save_path, index=False)
        print(f"Intermediary DataFrame saved to: {save_path}")
    except Exception as e:
        print(f"Warning: Failed to save intermediary DataFrame to '{save_path}': {e}")
