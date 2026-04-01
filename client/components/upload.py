import streamlit as st
from utils.api import upload_pdfs_api


def render_uploader():
    """
    Sidebar component for uploading PDFs to the backend.
    """
    st.sidebar.header("📂 Upload PDFs")
    uploaded_files = st.sidebar.file_uploader(
        "Upload one or more PDFs",
        type="pdf",
        accept_multiple_files=True
    )

    if st.sidebar.button("📤 Upload to Database") and uploaded_files:
        with st.sidebar:
            with st.spinner("Uploading and processing..."):
                try:
                    response = upload_pdfs_api(uploaded_files)
                    if response.status_code == 200:
                        st.success("✅ Uploaded successfully!")
                    else:
                        st.error(f"❌ Error: {response.text}")
                except Exception as e:
                    st.error(f"❌ Could not reach server: {e}")
