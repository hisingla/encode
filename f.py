import streamlit as st
import base64

st.set_page_config(page_title="Base64 Encode/Decode with Copy Icon", layout="wide")

st.markdown("""
<style>
    body {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    /* Reduce top margin/padding for the main block */
    .block-container {
        padding-top: 1.4rem !important;
    }
    /* Make title align to the left */
    h1 {
        text-align: left !important;
        margin-bottom: 2rem;
        color: #ffdd57;
    }
    textarea {
        background-color: #2f2f6e;
        border-radius: 8px;
        color: #f0f0f0;
        font-family: monospace;
        font-size: 14px;
        padding-top: 1.8rem;
        resize: vertical;
        position: relative;
        width: 100%;
        height: 180px;
        border: none;
        outline: none;
    }
    .output-container {
        position: relative;
    }
    .copy-icon {
        position: absolute;
        top: 8px;
        right: 8px;
        cursor: pointer;
        fill: #28a745;
        width: 24px;
        height: 24px;
        transition: fill 0.3s ease;
        z-index: 20;
    }
    .copy-icon:hover {
        fill: #1e7e34;
    }
    /* Style primary (encode and decode) buttons yellow */
    button[kind="primary"] {
        background-color: #facc15 !important;
        color: black !important;
        font-weight: 900 !important;
        border-radius: 10px !important;
        border:none !important;
        padding: 0.5em 1.5em !important;
        cursor: pointer !important;
        transition: background-color 0.3s ease !important;
        width: 100%;
    }
    button[kind="primary"]:hover {
        background-color: #b45309 !important;
        color: white !important;
    }
    /* Download button green */
    div.stDownloadButton > button {
        background-color: #16a34a !important;
        color: white !important;
        font-weight: bold !important;
        border-radius: 10px !important;
        padding: 0.5em 1.5em !important;
        cursor: pointer !important;
        transition: background-color 0.3s ease !important;
        width: 100% !important;
        margin-top: 10px !important;
    }
    div.stDownloadButton > button:hover {
        background-color: #15803d !important;
    }
</style>
""", unsafe_allow_html=True)

if "output_text" not in st.session_state:
    st.session_state.output_text = ""

if "error" not in st.session_state:
    st.session_state.error = ""

def clear_output_on_input_change():
    st.session_state.output_text = ""
    st.session_state.error = ""

st.title("🔐 Base64 Encode / Decode Utility")

mode = st.radio("", ["Encode", "Decode"], horizontal=True, on_change=clear_output_on_input_change)

# --- FIX: Clear input_text on mode change ---
if "last_mode" not in st.session_state:
    st.session_state.last_mode = mode
if mode != st.session_state.last_mode:
    st.session_state.input_text = ""
    st.session_state.last_mode = mode
# --- END FIX ---

input_text = st.text_area(
    label="Input",
    height=180,
    placeholder="Enter text to encode..." if mode == "Encode" else "Enter Base64 text to decode...",
    key="input_text"
)

error_msg = ""

cols = st.columns(2)

with cols[0]:
    if mode == "Encode":
        if st.button("Encode", key="encode_btn", type="primary"):
            try:
                st.session_state.output_text = base64.b64encode(st.session_state.input_text.encode("utf-8")).decode("utf-8")
                st.session_state.error = ""
            except Exception as e:
                st.session_state.error = f"Encoding error: {e}"
    else:
        if st.button("Decode", key="decode_btn", type="primary"):
            try:
                decoded_bytes = base64.b64decode(st.session_state.input_text.encode("utf-8"), validate=True)
                st.session_state.output_text = decoded_bytes.decode("utf-8", errors="replace")
                st.session_state.error = ""
            except Exception as e:
                st.session_state.error = f"Decoding error: {e}"

if st.session_state.error:
    st.error(st.session_state.error)

if st.session_state.output_text:
    st.code(st.session_state.output_text, language=None)

    st.download_button(
        label="Download Output",
        data=st.session_state.output_text,
        file_name=f"{mode.lower()}_output.txt",
        mime="text/plain",
        key="download_btn"
    )
