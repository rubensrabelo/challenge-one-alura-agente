from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from src.modules.chat.service import ChatService

router = APIRouter(prefix="/chat", tags=["Chat Inteligente"])

class QueryRequest(BaseModel):
    question: str = Field(..., min_length=1)

class QueryResponse(BaseModel):
    answer: str

@router.post("/ask", response_model=QueryResponse, status_code=status.HTTP_200_OK)
async def ask_agent(payload: QueryRequest):
    try:
        answer = ChatService.answer_question(payload.question)
        return QueryResponse(answer=answer)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro interno ao processar a resposta.")
