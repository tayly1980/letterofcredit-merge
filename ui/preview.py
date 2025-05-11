# ui/preview.py

import streamlit as st
from logic.prompt_builder import build_generation_prompt
from logic.openai_generator import generate_synthetic_messages

def render():
    st.title("Preview Your SWIFT Message Sequence")

    if 'message_sequence' not in st.session_state:
        st.error("No sequence found. Please start from the beginning.")
        if st.button("🔙 Go to Home"):
            st.session_state.step = "home"
            st.rerun()
        return

    sequence = st.session_state.message_sequence
    st.markdown("### Message Sequence:")
    for i, msg_type in enumerate(sequence):
        st.markdown(f"**{i+1}. {msg_type}**")

    st.markdown("---")

    # Generate synthetic messages with OpenAI
    if st.button("🧠 Use OpenAI to Generate Messages"):
        st.info("Generating messages... please wait.")
        prompt = build_generation_prompt(sequence)
        response = generate_synthetic_messages(prompt)

        if response.startswith("❌"):
            st.error(response)
        else:
            st.session_state.generated_messages = response
            st.success("Messages generated successfully!")
            st.rerun()  # ✅ Ensures generated messages appear immediately

    # Show generated messages if available
    if 'generated_messages' in st.session_state:
        st.markdown("### Generated Messages")
        st.code(st.session_state.generated_messages, language=None)

        if st.button("🧩 Proceed to Merge Final MT700"):
            st.session_state.step = "final_mt700"
            st.rerun()

    if st.button("🔁 Go Back to Sequence Builder"):
        st.session_state.step = "sequence_builder"
        st.rerun()
