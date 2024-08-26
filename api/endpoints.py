import logging
from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Form, Depends, Request
from services.chatbot_service import get_openai_response_with_langchain, clear_chat_history, get_db

router = APIRouter(
    prefix="/chatbots",
    tags=["chatbots"]
)


# Parsing JSON input
class AskQuestionRequest(BaseModel):
    user_question: str
    user_id: str


class ClearChatRequest(BaseModel):
    user_id: str


@router.post("/ask")
async def ask_question(request: AskQuestionRequest, db: Session = Depends(get_db)):
    try:
        return get_openai_response_with_langchain(user_question=request.user_question.strip(), db=db, user_id=request.user_id)
    except Exception as e:
        logging.error(f"Error in /ask endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error, please check the logs."
        )


@router.delete("/clear-chat")
async def clear_chat(request: ClearChatRequest, db: Session = Depends(get_db)):
    try:
        return clear_chat_history(user_id=request.user_id, db=db)
    except Exception as e:
        logging.error(f"Error in /clear-chat endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error, please check the logs."
        )
