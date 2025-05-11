# app.py

import streamlit as st
from ui import (
    home,
    build_and_generate,
    file_uploader,
    final_output
)

# Set app page config
st.set_page_config(page_title="Letter of Credit Swift Merge App", layout="wide")

# Initialize session state
if 'step' not in st.session_state:
    st.session_state.step = "home"

# Page routing logic
if st.session_state.step == "home":
    home.render()

elif st.session_state.step in ["input_selector", "sequence_builder", "preview"]:
    build_and_generate.render()

elif st.session_state.step == "file_uploader":
    file_uploader.render()

elif st.session_state.step == "final_output":
    final_output.render()
