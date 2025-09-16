import streamlit as st
from datetime import datetime

# --- Page Configuration ---
st.set_page_config(
    page_title="LLM Research Tool",
    page_icon="🔬",
    layout="wide",
)

# --- Page Title ---
st.title("🔬 LLM Shared Intent Research Dashboard")
now = datetime.now()
formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
st.write(f"Dashboard launched on: {formatted_time}")

st.divider()

# --- Placeholder Message ---
st.header("🚧 Core Application - Under Development 🚧")
st.info(
    "The core experimental logic is currently being developed and tested. "
    "This user interface will be connected once the backend is complete."
)
st.warning(
    "To run an experiment, please use the command line entry point for now."
)
