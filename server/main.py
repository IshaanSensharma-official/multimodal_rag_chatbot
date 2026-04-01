from fastapi import FastAPI, UploadFile, File, Form, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from modules.load_vectorstore import load_vectorstore, get_vectorstore
from modules.llm import get_llm_chain
from modules.query_handlers import query_chain
from logger import logger

app = FastAPI(title="RagBot 2.0")

# Allow all origins (frontend can communicate freely)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.middleware("http")
async def catch_exception_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as exc:
        logger.exception("UNHANDLED EXCEPTION")
        return JSONResponse(status_code=500, content={"error": str(exc)})


@app.get("/")
async def root():
    return {"message": "RagBot 2.0 is running! Go to /docs for API reference."}


@app.get("/test")
async def test():
    return {"message": "Testing successful..."}


@app.post("/upload_pdfs/")
async def upload_pdfs(files: List[UploadFile] = File(...)):
    """
    Upload one or more PDFs.
    They will be chunked, embedded, and stored in ChromaDB.
    """
    try:
        logger.info(f"Received {len(files)} file(s) for upload")
        load_vectorstore(files)
        logger.info("Documents added to ChromaDB successfully")
        return {"message": f"{len(files)} file(s) processed and vectorstore updated."}
    except Exception as e:
        logger.exception("Error during PDF upload")
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.post("/ask/")
async def ask_question(question: str = Form(...)):
    """
    Ask a question. The server will retrieve relevant chunks
    from ChromaDB and generate an answer using Groq LLaMA3.
    """
    try:
        logger.info(f"User query: {question}")

        vectorstore = get_vectorstore()
        retriever = vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 4}
        )

        chain = get_llm_chain(retriever)
        result = query_chain(chain, question)

        logger.info("Query successful")
        return result

    except Exception as e:
        logger.exception("Error processing question")
        return JSONResponse(status_code=500, content={"error": str(e)})
