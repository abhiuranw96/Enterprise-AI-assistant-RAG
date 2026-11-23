from pathlib import Path
from fastapi import APIRouter, File, Header, UploadFile
from fastapi.exceptions import HTTPException
from traitlets import default
from src.core.config import get_settings
from pydantic import BaseModel, Field
from src.utils.helper import ask_agent
from src.ingestion.loader import SUPPORTED_FILE_TYPES, load_file
from src.chunking import chunker
from src.vectordb.vector_store import add_documents

settings = get_settings()

# router
router = APIRouter(prefix="/api")

class chatRequest(BaseModel):
    question: str = Field(min_length=2, max_length=3000)
    
@router.get("/health")
async def health_check():
    return {"status": "ok"}

# chat endpoint
@router.post("/chat")
async def chat_endpoint(request: chatRequest):
    response = ask_agent(request.question)
    
    return {
        "answer": response["answer"],
        "source": response["source"],
        "rewritten_query": response.get("current_query", request.question  ),
    }

# Ingestion endpoint for adding documents to the vector store
@router.post("/ingest")
async def ingest_documents(file: UploadFile = File(...), secret_key: str = Header(default="")):
    if secret_key != settings.admin_api_key:
        raise HTTPException(status_code=403, detail="Invalid secret key")
    
    suffix = Path(file.filename).suffix.lower()
    if suffix not in SUPPORTED_FILE_TYPES:
        raise HTTPException(status_code=400, detail=f"Unsupported file type. Supported types are: {SUPPORTED_FILE_TYPES}")
    
    upload_dir = Path(settings.upload_dir)
    upload_dir.mkdir(parents=True, exist_ok=True)
    dest = upload_dir / Path(file.filename).name
    dest.write_bytes(await file.read())
    
    docs = load_file(dest)
    chunks = chunker.chunk_documents(docs)
    
    # add chunks to vector store
    ids = add_documents(chunks)
    
    return {"message": f"Successfully ingested {dest.name} with {len(chunks)} chunks.", "ids": len(ids)}
    
    

    