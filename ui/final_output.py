# ui/final_output.py

import streamlit as st

def render():
    st.markdown("## 📄 Final MT700 + 🕵️ Audit Trail")

    if 'final_merge_output' not in st.session_state:
        st.error("❌ No final merged message available.")
        return

    # Original message chain
    if 'uploaded_messages' in st.session_state:
        original_chain = "\n\n".join(
            f"{msg['type']} – {msg['filename']}\n\n{msg['content']}"
            for msg in st.session_state.uploaded_messages
        )
    elif 'generated_messages' in st.session_state:
        original_chain = st.session_state.generated_messages
    else:
        original_chain = "N/A"

    # Split MT700 and audit
    full_output = st.session_state.final_merge_output
    split_marker = "| Field"
    if split_marker in full_output:
        mt700_part, audit_part = full_output.split(split_marker, 1)
        audit_part = split_marker + audit_part
    else:
        mt700_part = full_output
        audit_part = "*No audit trail available.*"

    # Preview sections
    with st.expander("📦 Original Message Chain"):
        st.code(original_chain[:5000], language=None)

    st.markdown("### 📬 Final Merged MT700 Message")
    st.code(mt700_part.strip(), language=None)

    st.markdown("### 📊 Audit Trail")
    st.markdown(audit_part.strip(), unsafe_allow_html=False)

    # Start over
    if st.button("🔁 Start Over"):
        st.session_state.clear()
        st.session_state.step = "home"
        st.rerun()  # ✅ Instant reset to Home
