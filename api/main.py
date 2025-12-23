from fastapi import FastAPI
from fastapi.concurrency import run_in_threadpool
from pydantic import BaseModel
import traceback
from src.rag import get_rag

app = FastAPI()
pipeline = None  # variável global para o pipeline


class Question(BaseModel):
    question: str


@app.on_event("startup")
def startup_event():
    global pipeline
    print("Inicializando pipeline RAG...")
    pipeline = get_rag()
    print("Pipeline RAG inicializado.")


async def execute_pipeline(method, *args, **kwargs):
    """Executa qualquer método do pipeline em thread separada e trata erros."""
    try:
        return await run_in_threadpool(method, *args, **kwargs)
    except Exception:
        print(f"\n=== ERRO AO EXECUTAR {method.__name__} ===")
        traceback.print_exc()
        print("========================================\n")
        return {"detail": f"Erro interno ao executar {method.__name__}."}


@app.post("/ask")
async def ask(question: Question):
    if not question.question.strip():
        return {"answer": "Pergunta vazia."}

    response = await execute_pipeline(pipeline.answer, question.question)
    if isinstance(response, dict) and "detail" in response:
        return response

    return {"answer": response}


@app.post("/retrieve")
async def retrieve(question: Question):
    if not question.question.strip():
        return {"documents": []}

    docs = await execute_pipeline(pipeline.retrieve, question.question)
    if isinstance(docs, dict) and "detail" in docs:
        return docs

    return {"documents": docs}


@app.get("/health")
async def health():
    # Retorna status do pipeline e componentes carregados
    return {
        "status": "ok",
        "vectorstore_loaded": getattr(pipeline, "vectorstore_loaded", True),
        "llm_loaded": getattr(pipeline, "llm_loaded", True)
    }


@app.get("/stats")
async def stats():
    # Retorna estatísticas do pipeline
    if pipeline is None:
        return {"detail": "Pipeline não inicializado"}

    return {
        "total_documents": getattr(pipeline, "total_documents", 82),
        "embedding_model": getattr(pipeline, "embedding_model_name", "sentence-transformers/all-MiniLM-L6-v2"),
        "llm_model": getattr(pipeline, "llm_model_name", "Qwen/Qwen2.5-0.5B-Instruct"),
        "chunk_size": getattr(pipeline, "chunk_size", 1200),
        "chunk_overlap": getattr(pipeline, "chunk_overlap", 150)
    }


