import streamlit as st

def render():
    # Title + subtitle
    st.markdown("""
        <style>
            .app-title {
                font-size: 2.3rem;
                font-weight: 800;
                margin-bottom: 0.3rem;
            }
            .app-subtitle {
                font-size: 1.1rem;
                color: #AAAAAA;
                margin-bottom: 2rem;
                max-width: 700px;
            }
            .button-container {
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                padding-top: 30px;
            }
            .button-container button {
                width: 300px;
                height: 3.5em;
                font-size: 1.1rem !important;
                font-weight: 600 !important;
                border-radius: 12px;
                margin: 10px 0;
            }
        </style>
        <div class="app-title">Letter of Credit Swift Merge App</div>
        <div class="app-subtitle">
            🧾 Generate or upload SWIFT messages (MT700, MT707, MT799), merge them, and review a final MT700 with an audit trail.
        </div>
    """, unsafe_allow_html=True)

    # Action buttons
    st.markdown('<div class="button-container">', unsafe_allow_html=True)

    if st.button("🧠  Create Synthetic Messages"):
        st.session_state.step = "sequence_builder"
        st.rerun()

    if st.button("📤  Upload Your SWIFT Messages"):
        st.session_state.step = "file_uploader"
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

        # Disclaimer
    st.markdown("""
        <div style='
            border-left: 6px solid #f39c12;
            background-color: #2d2d2d;
            padding: 1rem;
            margin-top: 3rem;
            font-size: 1rem;
            color: #f0f0f0;
        '>
            ⚠️ <strong>Disclaimer:</strong> This application is intended for <em>testing and proof-of-concept</em> purposes only. <br><br>
            Please do not upload real or sensitive SWIFT messages. When enabled, message generation and merging functions
            may rely on OpenAI’s language models and data may be processed externally.
        </div>
    """, unsafe_allow_html=True)
