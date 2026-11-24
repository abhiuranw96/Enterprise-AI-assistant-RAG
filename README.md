# Enterprise AI Assistant

A private knowledge assistant for an organization. Upload company documents to a Pinecone-backed knowledge base, then ask questions through a Streamlit chat interface. The backend uses a LangGraph workflow to route questions, retrieve and grade private evidence, generate answers, and use web search when the private knowledge base is insufficient.

## Features

- Chat interface built with Streamlit.
- FastAPI endpoints for chat, document ingestion, and health checks.
- Document ingestion for PDF, TXT, Markdown, and DOCX files.
- Document chunking, Hugging Face embeddings, and Pinecone vector search.
- Groq-powered answer generation and Tavily web-search fallback.
- Private-KB answers include source context when evidence is available.

## Requirements

- Python 3.10 or later.
- API credentials for Groq, Tavily, and Pinecone.
- A Pinecone index configured for the embedding model's dimension (384 by default).

## Setup

Create and activate a virtual environment from the project root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the project dependencies:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Create a `.env` file in the project root and configure the application:

```dotenv
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
PINECONE_API_KEY=your_pinecone_api_key

CHAT_MODEL=your_groq_model_name
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

PINECONE_INDEX_NAME=agentic-rag
PINECONE_NAMESPACE=IT-industry-agentic-rag
ADMIN_API_KEY=replace_with_a_private_ingestion_key
```

Keep `.env` private and do not commit it. The ingestion key protects document uploads; use a strong private value. If you change it, make the same key available to the Streamlit process as the `ADMIN_API_KEY` environment variable.

## Run the application

Start the backend from the project root:

```powershell
python -m uvicorn main:app --host 127.0.0.1 --port 8000
```

In a second terminal, activate the same virtual environment and start the frontend:

```powershell
streamlit run frontend/app.py --server.port 8501
```

Open the Streamlit interface at <http://localhost:8501>.

The backend is available at <http://127.0.0.1:8000>. Interactive API documentation is at <http://127.0.0.1:8000/docs>, and the health check is at <http://127.0.0.1:8000/api/health>.

If the backend runs at a different address, set `ENTERPRISE_AI_API_URL` in the environment where Streamlit is started, for example:

```powershell
$env:ENTERPRISE_AI_API_URL = "http://127.0.0.1:8000"
```

## API endpoints

### `GET /api/health`

Returns the backend health status.

### `POST /api/chat`

Send a question as JSON:

```json
{
  "question": "What is our annual leave policy?"
}
```

The response contains the answer, its source, and the query used.

### `POST /api/ingest`

Upload one supported document as multipart form data. Include the ingestion key in the `secret-key` request header. The response reports the uploaded filename and number of document chunks added.

Supported extensions: `.pdf`, `.txt`, `.md`, and `.docx`.

The Streamlit sidebar provides a file picker and an **Upload & ingest** button for this endpoint.

## Project structure

```text
frontend/
  app.py                 Streamlit chat and upload interface
src/
  api/                   FastAPI routes
  chunking/              Document chunking
  core/                  Application settings and logging
  embeddings/             Hugging Face embeddings
  generation/             Answer generation
  ingestion/              Supported file loaders
  llm/                    Groq model and Tavily search setup
  retrieval/              Knowledge-base retrieval
  state/                  LangGraph state and structured output models
  vectordb/               Pinecone vector-store integration
  workflows/              LangGraph routing and RAG workflow
main.py                   FastAPI application entry point
requirements.txt          Python dependencies
```
