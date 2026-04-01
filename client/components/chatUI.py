import streamlit as st
from utils.api import ask_question


def render_chat():
    """
    Main chat interface component.
    """
    st.subheader("💬 Chat with your Documents")

    # Initialize chat history in session state
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Render existing chat history
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).markdown(msg["content"])

    # Handle new user input
    user_input = st.chat_input("Ask a question about your uploaded documents...")

    if user_input:
        # Show user message immediately
        st.chat_message("user").markdown(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Query the backend
        with st.spinner("Thinking..."):
            try:
                response = ask_question(user_input)

                if response.status_code == 200:
                    data = response.json()
                    answer = data.get("response", "No answer returned.")
                    sources = data.get("sources", [])

                    st.chat_message("assistant").markdown(answer)

                    # Show sources if available
                    if sources:
                        unique_sources = list(set(src for src in sources if src))
                        if unique_sources:
                            st.markdown("📄 **Sources:**")
                            for src in unique_sources:
                                st.markdown(f"- `{src}`")

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer
                    })
                else:
                    st.error(f"❌ Server error: {response.text}")

            except Exception as e:
                st.error(f"❌ Could not reach server: {e}")
