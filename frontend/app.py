import os
from typing import Any

import requests
import streamlit as st


st.set_page_config(
    page_title="Enterprise AI Assistant",
    page_icon="spark",
    layout="wide",
    initial_sidebar_state="expanded",
)


st.markdown(
    """
    <style>
    :root {
        color-scheme: dark;
    }
    html, body, [class*="css"], [data-testid="stMarkdownContainer"] {
        color: #f4f6fb !important;
    }
    [data-testid="stAppViewContainer"] {
        background: #0b1020;
    }
    [data-testid="stHeader"] {
        background: #0b1020;
    }
    [data-testid="stSidebar"] {
        background: #11172a;
        border-right: 1px solid #252d47;
    }
    [data-testid="stSidebar"] > div {
        padding-top: 1.75rem;
    }
    .block-container {
        max-width: 1180px;
        padding-top: 1.4rem;
        padding-bottom: 2rem;
        color: #f4f6fb;
    }
    #MainMenu, footer {
        visibility: hidden;
    }
    .brand {
        display: flex;
        align-items: center;
        gap: 10px;
        margin: 0 0 1.6rem 4px;
        color: #ffffff;
        font-size: 19px;
        font-weight: 750;
    }
    .brand-mark {
        width: 38px;
        height: 38px;
        display: grid;
        place-items: center;
        border-radius: 11px;
        color: white;
        background: linear-gradient(135deg, #7c69ff, #a88cff);
        box-shadow: 0 8px 18px rgba(124, 105, 255, 0.30);
        font-size: 18px;
    }
    .section-label {
        color: #aeb6ce;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 0.12em;
        margin: 0 0 8px 6px;
    }
    .app-card {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 8px;
        padding: 11px 12px;
        border: 1px solid #29324e;
        border-radius: 12px;
        background: #171d31;
        color: #edf0f8;
        font-size: 14px;
        font-weight: 650;
    }
    .app-card.active {
        border-color: #7162df;
        background: #252449;
        color: #ffffff;
    }
    .app-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #9a8cff;
    }
    .chat-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        min-height: 74px;
        margin-bottom: 12px;
        padding: 12px 18px;
        border: 1px solid #29324e;
        border-radius: 16px;
        background: #11172a;
        box-shadow: 0 8px 28px rgba(0, 0, 0, 0.18);
    }
    .chat-title {
        color: #ffffff;
        font-size: 18px;
        font-weight: 760;
    }
    .chat-subtitle {
        margin-top: 3px;
        color: #b8bfd3;
        font-size: 12px;
    }
    .status {
        display: inline-flex;
        align-items: center;
        gap: 7px;
        color: #d8dced;
        font-size: 12px;
    }
    .status-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #34b66a;
        box-shadow: 0 0 0 4px #def4e7;
    }
    [data-testid="stChatMessage"] {
        border: 1px solid #29324e;
        border-radius: 16px;
        background: #171d31;
        color: #f7f8fc;
        margin: 8px 0;
        padding: 13px 16px;
    }
    [data-testid="stChatMessage"][data-testid*="assistant"] {
        background: #13192b;
    }
    [data-testid="stChatMessage"] p,
    [data-testid="stChatMessage"] span,
    [data-testid="stChatMessage"] li,
    [data-testid="stChatMessage"] strong {
        color: #f7f8fc !important;
    }
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] {
        color: #f7f8fc;
    }
    [data-testid="stCaptionContainer"] {
        color: #aeb6ce !important;
    }
    [data-testid="stChatInput"] {
        border: 0;
    }
    [data-testid="stChatInput"] textarea {
        min-height: 56px;
        color: #ffffff !important;
        caret-color: #ffffff;
    }
    [data-testid="stChatInput"] > div {
        border: 1px solid #3a4566;
        border-radius: 16px;
        background: #171d31;
        box-shadow: 0 8px 28px rgba(0, 0, 0, 0.20);
    }
    [data-testid="stChatInput"] textarea::placeholder {
        color: #9ba4bc !important;
        opacity: 1;
    }
    div.stButton > button {
        width: 100%;
        border-radius: 11px;
        border: 1px solid #8172ef;
        background: #7161df;
        color: white;
        font-weight: 700;
        height: 44px;
        box-shadow: 0 8px 16px rgba(113, 97, 223, 0.20);
    }
    div.stButton > button:hover {
        border-color: #9a8cff;
        background: #6252cf;
        color: white;
    }
    [data-testid="stFileUploader"] section {
        border: 1px dashed #4c5777;
        border-radius: 12px;
        background: #171d31;
        color: #f4f6fb;
    }
    [data-testid="stFileUploader"] small,
    [data-testid="stFileUploader"] span,
    [data-testid="stFileUploader"] button {
        color: #f4f6fb !important;
    }
    [data-testid="stAlert"] {
        color: #ffffff;
        border-radius: 12px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
API_URL = os.getenv("ENTERPRISE_AI_API_URL", "http://127.0.0.1:8000").rstrip("/")


def check_api() -> bool:
    try:
        return requests.get(f"{API_URL}/api/health", timeout=2).ok
    except requests.RequestException:
        return False


def source_label(source: str) -> str:
    labels = {
        "private_kb": "Private knowledge",
        "web_search": "Web search",
        "direct": "General answer",
        "insufficient_evidence": "Evidence needed",
    }
    return labels.get(source, "Assistant")


if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hello! Ask me about your private company knowledge, or upload a document to add it to the knowledge base.",
            "source": "direct",
        }
    ]


with st.sidebar:
    st.markdown(
        '<div class="brand"><div class="brand-mark">AI</div><span>Enterprise AI</span></div>',
        unsafe_allow_html=True,
    )
    st.markdown('<div class="section-label">APPLICATIONS</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="app-card active"><span class="app-dot"></span><span>Knowledge Assistant</span></div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="app-card"><span class="app-dot"></span><span>Document Library</span></div>',
        unsafe_allow_html=True,
    )

    st.markdown('<div class="section-label" style="margin-top:1.5rem;">ADD KNOWLEDGE</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Upload private company file",
        type=["pdf", "txt", "md", "docx"],
        label_visibility="collapsed",
    )

    ingest_clicked = st.button("Upload & ingest", use_container_width=True)
    if ingest_clicked:
        if uploaded_file is None:
            st.warning("Choose a PDF, TXT, MD, or DOCX file first.")
        else:
            with st.spinner("Uploading and adding document to the knowledge base..."):
                try:
                    response = requests.post(
                        f"{API_URL}/api/ingest",
                        headers={"secret-key": os.getenv("ADMIN_API_KEY", "abhi")},
                        files={"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)},
                        timeout=300,
                    )
                    if response.ok:
                        result: Any = response.json()
                        st.success(result.get("message", "Document ingested successfully."))
                    else:
                        try:
                            detail = response.json().get("detail", response.text)
                        except requests.JSONDecodeError:
                            detail = response.text
                        st.error(f"Ingestion failed: {detail}")
                except requests.RequestException as exc:
                    st.error(f"Could not reach the API at {API_URL}: {exc}")


api_online = check_api()
status_text = "System online" if api_online else "API unavailable"
status_color = "#34b66a" if api_online else "#e05a67"

st.markdown(
    f"""
    <div class="chat-header">
        <div>
            <div class="chat-title">Knowledge Assistant</div>
            <div class="chat-subtitle">Chat with your private company knowledge</div>
        </div>
        <div class="status"><span class="status-dot" style="background:{status_color};box-shadow:0 0 0 4px {'#f7dfe2' if not api_online else '#def4e7'}"></span>{status_text}</div>
    </div>
    """,
    unsafe_allow_html=True,
)


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message["role"] == "assistant" and message.get("source"):
            st.caption(source_label(message["source"]))


prompt = st.chat_input("Ask about your company knowledge...")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Searching the knowledge base..."):
            try:
                response = requests.post(
                    f"{API_URL}/api/chat",
                    json={"question": prompt},
                    timeout=300,
                )
                if response.ok:
                    result = response.json()
                    answer = result.get("answer", "I could not generate an answer.")
                    source = result.get("source", "direct")
                else:
                    try:
                        detail = response.json().get("detail", response.text)
                    except requests.JSONDecodeError:
                        detail = response.text
                    answer = f"The assistant could not complete this request: {detail}"
                    source = "insufficient_evidence"
            except requests.RequestException as exc:
                answer = f"Could not reach the API at {API_URL}. Start the FastAPI server and try again."
                source = "insufficient_evidence"

        st.markdown(answer)
        st.caption(source_label(source))

    st.session_state.messages.append(
        {"role": "assistant", "content": answer, "source": source}
    )
