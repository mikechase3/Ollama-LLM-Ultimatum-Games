import streamlit as st
from datetime import datetime
from main import run_pipeline


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

# Add a form for experiment parameters
with st.form("experiment_params"):
    input_file = st.file_uploader("Input File")
    output_name = st.text_input("Output File Name")

    if st.form_submit_button("Run Pipeline"):
        with st.spinner("Running experiment pipeline..."):
            run_pipeline()  # Later modify to accept parameters

# --- Placeholder Message ---
st.header("🚧 Core Application - Under Development 🚧")
st.info(
    "The core experimental logic is currently being developed and tested. "
    "This user interface will be connected once the backend is complete."
)
st.warning(
    "To run an experiment, please use the command line entry point for now."
)
