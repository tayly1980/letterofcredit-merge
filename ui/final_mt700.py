# ui/final_mt700.py

import streamlit as st
from logic.openai_merger import merge_messages_with_audit

def render():
    st.markdown("## 🔄 Merge Synthetic Messages into Final MT700")

    # Load message chain from upload or synthetic generation
    message_chain = None
    if 'uploaded_messages' in st.session_state:
        message_chain = "\n\n".join(
            f"{msg['type']} – {msg['filename']}\n\n{msg['content']}"
            for msg in st.session_state.uploaded_messages
        )
    elif 'generated_messages' in st.session_state:
        message_chain = st.session_state.generated_messages

    if not message_chain:
        st.warning("No message chain found. Please upload or generate messages first.")
        return

    # Preview the full message chain
    with st.expander("🧾 Message Chain Preview", expanded=True):
        st.code(message_chain[:5000], language=None)

    # Merge button
    if st.button("🧩 Merge Messages to Final MT700"):
        with st.spinner("Merging... please wait ⏳"):
            result = merge_messages_with_audit(message_chain)
            st.session_state.final_merge_output = result
            st.session_state.step = "final_output"
            st.rerun()  # ✅ ensures you land on final output screen instantly
