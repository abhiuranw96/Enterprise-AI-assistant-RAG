from contextlib import asynccontextmanager
from importlib import import_module
from fastapi import FastAPI
from src.config import get_settings
from src.generation.graph import build_rag_graph
from src.api.routes import router as api_router


AsyncSqliteSaver = import_module(
    "langgraph.checkpoint.sqlite.aio"
).AsyncSqliteSaver


settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    checkpoint_path = settings.checkpoint_db_path
    checkpoint_path.parent.mkdir(parents=True, exist_ok=True)

    async with AsyncSqliteSaver.from_conn_string(
        str(checkpoint_path)
    ) as checkpointer:
        app.state.rag_graph = build_rag_graph(checkpointer)
        yield

app = FastAPI(
    title=settings.app_name,
    lifespan=lifespan,
)

app.include_router(api_router, prefix=settings.api_prefix)