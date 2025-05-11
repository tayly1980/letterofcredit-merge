# ui/file_uploader.py

import streamlit as st
import fitz  # PyMuPDF
from logic.openai_generator import detect_message_type
from logic.openai_merger import merge_messages_with_audit

def extract_text_from_pdf(uploaded_file):
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    return "".join(page.get_text() for page in doc)

def render():
    st.title("📤 Upload Your SWIFT Messages")
    st.markdown("Please upload your SWIFT messages in this order:")
    st.markdown("1. MT700 – Letter of Credit (required)")
    st.markdown("2. MT707 – Amendment(s) (optional)")
    st.markdown("3. MT799 – Correction(s) (optional)")
    st.markdown("Supported formats: `.txt`, `.pdf`")

    uploaded_files = st.file_uploader(
        "Upload one or more files (in correct order)", 
        type=["txt", "pdf"], 
        accept_multiple_files=True
    )

    if uploaded_files:
        detected = []
        for file in uploaded_files:
            if file.type == "application/pdf":
                content = extract_text_from_pdf(file)
            else:
                content = file.read().decode("utf-8")

            msg_type = detect_message_type(content)

            detected.append({
                "filename": file.name,
                "content": content,
                "type": msg_type
            })

        st.markdown("### 🧾 Message Previews & Classification")
        for i, msg in enumerate(detected):
            with st.expander(f"{i+1}. {msg['type']} – {msg['filename']}"):
                st.code(msg["content"][:2000], language="markdown")

        st.markdown("---")
        if st.button("✅ Proceed to Merge"):
            st.session_state.uploaded_messages = detected
            st.session_state.generated_messages = "\n\n".join(
                f"**{msg['type']} – {msg['filename']}**\n\n{msg['content']}"
                for msg in detected
            )

            # 🔁 Call OpenAI to perform merge and audit
            message_chain = st.session_state.generated_messages
            merged = merge_messages_with_audit(message_chain)
            st.session_state.final_merge_output = merged

            # ✅ Move to final output view
            st.session_state.step = "final_output"
            st.rerun()