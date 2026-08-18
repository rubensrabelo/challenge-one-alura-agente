from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.modules.document.router import router as document_router
from src.modules.chat.router import router as chat_router

app = FastAPI(
    title="Alura Agente - Monolito Modular",
    description="Backend estruturado com pasta 'src' e APIRouter"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(document_router)
app.include_router(chat_router)

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/")
def health_check():
    return {"status": "healthy", "architecture": "Modular Monolith (src)"}
