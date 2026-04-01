import streamlit as st
from components.upload import render_uploader
from components.chatUI import render_chat
from components.history_download import render_history_download

st.set_page_config(page_title="RagBot 2.0", page_icon="🤖", layout="wide")
st.title("🤖 RagBot 2.0 — Chat with your PDFs")
st.caption("Upload PDFs from the sidebar, then ask questions below.")

render_uploader()
render_chat()
render_history_download()
