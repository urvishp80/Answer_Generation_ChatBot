from sqlalchemy import Column, Integer, String, DateTime, func, create_engine, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ChatHistory(Base):
    __tablename__ = "chat_history"
    __table_args__ = {'schema': 'clearbuydb'}  # Specify the schema

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(50), nullable=False)
    question = Column(Text, nullable=False)  # Using Text type for question
    answer = Column(Text, nullable=False)  # Using Text type for answer
    created_at = Column(DateTime, default=func.now(), nullable=False)

# Uncomment below lines if you want to create table "chat_history" again in 'clearbuydb' DB.
# from core.config import settings
# engine = create_engine(settings.DATABASE_URI)
# Base.metadata.create_all(bind=engine)
