import os
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate  # ✅ Fixed import
from langchain.chains import RetrievalQA
from langchain_groq import ChatGroq

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")


def get_llm_chain(retriever):
    """
    Build and return a RetrievalQA chain using Groq LLaMA3
    and the provided retriever.
    """
    llm = ChatGroq(
        groq_api_key=GROQ_API_KEY,
        model_name="llama3-70b-8192"
    )

    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template="""
You are **RagBot**, an AI-powered assistant that helps users understand the content of uploaded PDF documents.

Your job is to provide clear, accurate, and helpful responses based **only on the provided context**.

---

🔍 **Context**:
{context}

🙋 **User Question**:
{question}

---

💬 **Answer**:
- Respond in a calm, factual, and helpful tone.
- Use simple language where possible.
- If the context does not contain the answer, say: "I'm sorry, but I couldn't find relevant information in the provided documents."
- Do NOT make up facts outside the context.
"""
    )

    return RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        chain_type_kwargs={"prompt": prompt},
        return_source_documents=True
    )