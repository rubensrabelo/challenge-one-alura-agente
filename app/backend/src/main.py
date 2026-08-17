from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.modules.document.router import router as document_router
from src.modules.chat.router import router as chat_router

app = FastAPI(
    title="Alura Agente - Monolito Modular",
    description="Backend estruturado com pasta 'src' e APIRouter",
    version="2.2.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(document_router)
app.include_router(chat_router)

@app.get("/")
def health_check():
    return {"status": "healthy", "architecture": "Modular Monolith (src)"}
