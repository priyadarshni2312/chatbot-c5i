from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.db import Base, SessionLocal, engine

class ChatHistory(Base):
    __tablename__ = 'chat_history'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    question = Column(String(length=512), index=True)
    response = Column(String(length=512))
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

def create_chat_history_table():
    Base.metadata.create_all(bind=engine)

def add_chat_entry(user_id: int, question: str, response: str, db: SessionLocal):
    chat_entry = ChatHistory(user_id=user_id, question=question, response=response)
    db.add(chat_entry)
    db.commit()

def get_chat_history(user_id: int, db: SessionLocal):
    return db.query(ChatHistory).filter(ChatHistory.user_id == user_id).order_by(ChatHistory.timestamp.asc()).all()
