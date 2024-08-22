import logging
from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Form, Depends, Request
from services.chatbot_service import get_openai_response_with_langchain, clear_chat_history, get_db

router = APIRouter(
    prefix="/chatbots",
    tags=["chatbots"]
)


@router.post("/ask")
def ask_question(request: Request, user_question: str = Form(), user_id: str = Form(), db: Session = Depends(get_db)):
    try:
        return get_openai_response_with_langchain(user_question=user_question.strip(), db=db, user_id=user_id)
    except Exception as e:
        logging.error(f"Error in /ask endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error, please check the logs."
        )


@router.delete("/clear-chat")
def clear_chat(user_id: str = Form(), db: Session = Depends(get_db)):
    try:
        return clear_chat_history(user_id=user_id, db=db)
    except Exception as e:
        logging.error(f"Error in /clear-chat endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error, please check the logs."
        )
