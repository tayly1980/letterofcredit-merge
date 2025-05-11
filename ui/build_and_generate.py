# ui/build_and_generate.py

import streamlit as st
from logic.prompt_builder import build_generation_prompt
from logic.openai_generator import generate_synthetic_messages
from logic.openai_merger import merge_messages_with_audit

def render():
    st.title("🛠️ Build & Generate SWIFT Messages")

    # Initialize session state
    if 'message_sequence' not in st.session_state:
        st.session_state.message_sequence = ['MT700']
    if 'sequence_confirmed' not in st.session_state:
        st.session_state.sequence_confirmed = False

    # Sequence controls
    col1, col2 = st.columns(2)
    with col1:
        if st.button("➕ Add MT707 (Amendment)"):
            st.session_state.message_sequence.append("MT707")
            st.rerun()
    with col2:
        if st.button("➕ Add MT799 (MSC - Correction)"):
            st.session_state.message_sequence.append("MT799")
            st.rerun()

    # Show current sequence
    st.markdown("### 🧾 Current Sequence")
    for i, msg in enumerate(st.session_state.message_sequence):
        st.markdown(f"{i + 1}. {msg}")

    # Reset sequence
    if st.button("🔁 Reset Sequence"):
        st.session_state.message_sequence = ['MT700']
        st.session_state.sequence_confirmed = False
        st.session_state.pop('generated_messages', None)
        st.session_state.pop('final_merge_output', None)
        st.rerun()

    # Confirm sequence first
    if not st.session_state.sequence_confirmed:
        if st.button("✅ Confirm Sequence"):
            st.session_state.sequence_confirmed = True
            st.rerun()
        return  # Stop here until confirmed

    # Auto-generate after confirmation
    if 'generated_messages' not in st.session_state:
        st.markdown("### 🤖 Generating Synthetic Messages...")
        prompt = build_generation_prompt(st.session_state.message_sequence)
        result = generate_synthetic_messages(prompt)

        if result.startswith("❌"):
            st.error(result)
        else:
            st.session_state.generated_messages = result
            st.success("Messages generated successfully!")
            st.rerun()

    # Show generated results and merge option
    st.markdown("### 📬 Generated Messages")
    st.code(st.session_state.generated_messages, language=None)

    if st.button("🧩 Proceed to Merge Final MT700"):
        with st.spinner("Merging... please wait ⏳"):
            message_chain = st.session_state.generated_messages
            merged = merge_messages_with_audit(message_chain)
            st.session_state.final_merge_output = merged
            st.session_state.step = "final_output"
            st.rerun()

    if st.button("🔁 Go Back and Rebuild Sequence"):
        st.session_state.sequence_confirmed = False
        st.session_state.pop('generated_messages', None)
        st.rerun()
