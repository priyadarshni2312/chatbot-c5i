from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.llm_integration import get_human_readable_summary
from app.chat_history import add_chat_entry, get_chat_history
from app.db import get_db

app = APIRouter()

@app.post("/query/")
async def query_sales(question: str, db: Session = Depends(get_db)):
    try:
        summary = get_human_readable_summary(question)
        add_chat_entry(user_id=1, question=question, response=summary, db=db)
        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/chat-history/{user_id}")
async def retrieve_chat_history(user_id: int, db: Session = Depends(get_db)):
    try:
        history = get_chat_history(user_id, db)
        return {"chat_history": history}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
