from pathlib import Path
from typing import List

import numpy as np
import pandas as pd


def generate_sample_input_file(output_path: Path) -> None:
    """
    Generates a sample CSV file with experiment parameters and saves it to the specified path.
    """
    num_rows = 30  # aka trials

    base_system_prompt = ("You are a rational agent participating in an economic decision-making experiment. "
                          "Provide clear, direct responses that explain your reasoning. "
                          "Focus only on the decision at hand.")

    base_prompt_proposer = ("You are the proposer in an ultimatum game. "
                            "The total pot is ${pot}. "
                            "You must propose a split of the pot between you and the receiver. "
                            "State your offer to the receiver and justify your reasoning.")

    base_prompt_receiver = ("You are the receiver in an ultimatum game. "
                            "The total pot is ${pot}. "
                            "The proposer has offered you ${offer}. "
                            "If you accept, you will receive ${offer} and the proposer will receive ${remainder}. "
                            "If you reject, both of you will receive nothing. "
                            "Decide whether to accept or reject the offer and justify your reasoning.")



    # Define supported models
    cpu_models: List[str] = [
        "phi3:latest",
        # "phi:latest",        # Microsoft's smallest model
        # "phi-2:latest",      # Improved version, still lightweight
        # "neural-chat:7b",    # Good balance of size/performance
        # "stablelm-zephyr:3b",# Very lightweight
        # "llama2:7b",         # Base model, reasonable on CPU
        # "orca-mini:3b"       # Smaller version of Orca
    ]
    gpu_models: List[str] = [
        "mixtral:8x7b",      # State-of-the-art performance
        "llama2:70b",        # Large, well-researched model
        "falcon:40b",        # Strong performer
        "openchat:7b",       # Great for dialogues
        "vicuna:13b",        # Strong reasoning
        "codellama:34b",     # Excellent for analytical tasks
        "qwen:72b",          # Latest large model
        "claude-2:latest"    # If available through Ollama
    ]
    models: List[str] = [] + cpu_models  # + gpu_models

    # Define DataFrame columns (matching OpenWebUI parameter names where possible)
    columns: List[str] = [
        # --- Experimental Setup Metadata ---
        "experiment-id",     # str, experiment grouping
        "trial-id",          # str, unique trial identifier
        "game",              # str, task/game type
        "role",              # str, {'proposer', 'receiver'}
        "pot",               # float, total resources in the game
        "offer",             # float, proposed split value
        "model",             # str, model name

        # --- Prompts and Instructions ---
        "system-prompt",     # str, researcher-provided or default
        "base-prompt",       # str, researcher-provided or default
        "final-prompt",      # str, constructed prompt substitued with pot/offer.

        # --- Creative / Behavioral Parameters for Ollama ---
        "temperature",       # float, [0.0-2.0], randomness/creativity
        "top_p",             # float, [0.0-1.0], nucleus sampling
        "top_k",             # int, [1+], top-k token filtering
        "min_p",             # float, [0.0-1.0], minimum probability
        "repeat_penalty",    # float, [1.0-2.0], discourages repetition
        "frequency_penalty", # float, [0.0-2.0], discourages frequent tokens
        "presence_penalty",  # float, [0.0-2.0], encourages novelty
        "tfs_z",             # float, tail-free sampling parameter
        "mirostat",          # int, {0,1,2}, adaptive sampling mode
        "mirostat_eta",      # float, learning rate for mirostat
        "mirostat_tau",      # float, target surprise for mirostat

        # --- Technical / System Parameters ---
        "seed",              # int, reproducibility seed (or not-applicable)
        "repeat_last_n",     # int, tokens considered for repeat_penalty
        "reasoning_effort",  # float or str, not widely supported
        "logit_bias",        # str or dict, bias token probabilities.
        "num_ctx",           # int, context window size
        "stop_sequence",     # str or list, stopping condition
        "use_mmap",          # bool, memory map flag, not useful
        "use_mlock",         # bool, lock model into RAM, not useful
        "num_keep",          # int, tokens to keep from start of context, not useful
        "num_predict",       # int, number of tokens to predict
        # "max_tokens",        # int, max tokens to generate - overlaps w/ num_predict.
    ]

    # Fill with defaults / placeholders
    table: pd.DataFrame = pd.DataFrame({
        "experiment-id": ["EXP00"] * num_rows,
        "trial-id": [f"trial_{i+1}" for i in range(num_rows)],
        "game": ["ultimatum"] * num_rows,
        "role": np.random.choice(["proposer", "receiver"], size=num_rows),
        "pot": [100] * num_rows,
        "offer": [50.0] * num_rows,
        "model": np.random.choice(models, size=num_rows),

        "system-prompt": [base_system_prompt] * num_rows,
        "base-prompt": [""] * num_rows,
        "final-prompt": [""] * num_rows,

        "temperature": [0.8] * num_rows,
        "top_p": [0.9] * num_rows,
        "top_k": [40] * num_rows,
        "min_p": [0.0] * num_rows,
        "repeat_penalty": [1.1] * num_rows,
        "frequency_penalty": [0.0] * num_rows,
        "presence_penalty": [0.0] * num_rows,
        "tfs_z": [1.0] * num_rows,
        "mirostat": [0] * num_rows,
        "mirostat_eta": [0.1] * num_rows,
        "mirostat_tau": [5.0] * num_rows,

        "seed": [42] * num_rows,  # Arbitrary, I like it from Hitchhiker’s Guide
        "repeat_last_n": [64] * num_rows,
        "reasoning_effort": [""] * num_rows,  # left blank
        "logit_bias": [""] * num_rows,        # left blank
        "num_ctx": [2048] * num_rows,
        "stop_sequence": [""] * num_rows,     # left blank
        "use_mmap": [True] * num_rows,
        "use_mlock": [False] * num_rows,
        "num_keep": [0] * num_rows,
        "num_predict": [512] * num_rows,
        # "max_tokens": [512] * num_rows,
    }, columns=columns)

    # Assign base prompts based on role after DataFrame creation
    table["base-prompt"] = table["role"].apply(
        lambda x: base_prompt_proposer if x == "proposer" else base_prompt_receiver
    )

    table.to_csv(output_path, index=False)
    print(f"Sample input file saved to: {output_path}")