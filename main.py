from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routes import router


app = FastAPI(title="Enterprise AI Assistant", version="1.0.0")

@app.get("/")
async def root():
    return {
        "status": "ok",
        "message": "Enterprise AI Assistant API is running",
        "health": "/api/health",
        "docs": "/docs",
    }
    
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)

