import streamlit as st
import base64

st.set_page_config(page_title="Base64 Encode/Decode with Copy Icon", layout="wide")

# CSS Styling
st.markdown("""
<style>
    body {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    h1 {
        text-align: center;
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
    .btn-encode {
        background-color: #28a745;
        color: white;
        font-weight: bold;
        border-radius: 10px;
        border:none;
        padding: 0.5em 1.5em;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }
    .btn-encode:hover {
        background-color: #1e7e34;
    }
    .btn-download > button {
        background-color: #ff4b5c !important;
        color: white !important;
        font-weight: bold;
        border-radius: 10px !important;
        padding: 0.5em 1.5em !important;
        cursor: pointer;
        transition: background-color 0.3s ease !important;
        width: 100% !important;
        margin-top: 10px !important;
    }
    .btn-download > button:hover {
        background-color: #e03f4a !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("🔐 Base64 Encode / Decode Utility")

mode = st.radio("Select Mode", ["Encode", "Decode"], horizontal=True)

input_text = st.text_area(
    label="Input",
    height=180,
    placeholder="Enter text to encode..." if mode == "Encode" else "Enter Base64 text to decode..."
)

output_text = ""
error = ""

if mode == "Encode":
    if st.button("Encode", key="encode_btn", help="Click to encode", args=None):
        try:
            output_text = base64.b64encode(input_text.encode("utf-8")).decode("utf-8")
            error = ""
        except Exception as e:
            error = f"Encoding error: {e}"
else:
    if st.button("Decode", key="decode_btn", help="Click to decode", args=None):
        try:
            decoded_bytes = base64.b64decode(input_text.encode("utf-8"), validate=True)
            output_text = decoded_bytes.decode("utf-8", errors="replace")
            error = ""
        except Exception as e:
            error = f"Decoding error: {e}"

if error:
    st.error(error)

if output_text:
    st.markdown(
        f"""
        <div class="output-container" style="position:relative;">
            <textarea class="output-textarea" readonly rows="10" style="width:100%;">{output_text}</textarea>
            <svg class="copy-icon" onclick="navigator.clipboard.writeText(`{output_text}`).then(() => alert('Copied to clipboard!'))" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                <path d="M16 1H4a2 2 0 0 0-2 2v14h2V3h12V1zm3 4H8a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h11a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2zm0 16H8V7h11v14z"/>
            </svg>
        </div>
        """, unsafe_allow_html=True)

    st.download_button(
        label="Download Output",
        data=output_text,
        file_name=f"{mode.lower()}_output.txt",
        mime="text/plain",
        key="download_btn"
    )
