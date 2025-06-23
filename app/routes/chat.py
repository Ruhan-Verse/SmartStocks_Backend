# app/routes/chat.py

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from app.services.llm import rag

router = APIRouter()

class ChatRequest(BaseModel):
    query: str

@router.post("/ask")
async def chat_with_bot(req: ChatRequest):
    try:
        query = req.query.strip()
        if not query:
            raise HTTPException(status_code=400, detail="Query cannot be empty.")
        
        response = await rag.generate_answer(query)
        return {"reply": response}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Bot error: {str(e)}")
