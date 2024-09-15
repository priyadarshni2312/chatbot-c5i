from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.llm_integration import get_human_readable_summary, get_normal_response
from app.chat_history import add_chat_entry, get_chat_history
from app.db import get_db

app = APIRouter(prefix='/api')

class QueryRequest(BaseModel):
    question: str

def is_database_query(message: str) -> bool:
    db_keywords = ["revenue", "sales", "total", "profit", "customer", "product", "orders"]
    return any(keyword in message.lower() for keyword in db_keywords)

@app.post("/query/")
async def query_sales(request: QueryRequest, db: Session = Depends(get_db)):
    try:
        question = request.question
        if is_database_query(question):
            summary = get_human_readable_summary(question)
            add_chat_entry(user_id=1, question=question, response=summary, db=db)
            return {"response": summary}
        else:
            response = get_normal_response(question)
            add_chat_entry(user_id=1, question=question, response=response, db=db)
            return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/chat-history/{user_id}")
async def retrieve_chat_history(user_id: int, db: Session = Depends(get_db)):
    try:
        history = get_chat_history(user_id, db)
        return {"chat_history": history}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
