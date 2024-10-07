import logging
from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Form, Depends, Request
from services.chatbot_service import get_openai_response_with_langchain, clear_chat_history, get_db, get_user_chat_history
from core.bot_history_db import ChatHistory

router = APIRouter(
    prefix="/chatbots",
    tags=["chatbots"]
)


# Define Pydantic models for parsing JSON input
class AskQuestionRequest(BaseModel):
    user_question: str
    user_id: str


class ClearChatRequest(BaseModel):
    user_id: str


class ChatHistoryRequest(BaseModel):
    user_id: str


@router.post("/ask")
# def ask_question(request: Request, user_question: str = Form(), user_id: str = Form(), db: Session = Depends(get_db)):
async def ask_question(request: AskQuestionRequest, db: Session = Depends(get_db)):
    try:
        return get_openai_response_with_langchain(user_question=request.user_question.strip(), db=db, user_id=request.user_id)
        # return get_openai_response_with_langchain(user_question=user_question.strip(), db=db, user_id=user_id)
    except Exception as e:
        logging.error(f"Error in /ask endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error, please check the logs."
        )


@router.delete("/clear-chat")
async def clear_chat(request: ClearChatRequest, db: Session = Depends(get_db)):
    try:
        # Check if the user_id exists in the database
        user_exists = db.query(ChatHistory).filter(ChatHistory.user_id == request.user_id).first() is not None
        if not user_exists:
            raise HTTPException(
                status_code=404,
                detail=f"No records found for user ID: {request.user_id}."
            )

        return clear_chat_history(user_id=request.user_id, db=db)
    except HTTPException as e:
        raise e
    except Exception as e:
        logging.warning(f"Error in /clear-chat endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error, please check the logs."
        )

    
@router.post("/chat-history")
async def chat_history(request: ChatHistoryRequest, db: Session = Depends(get_db)):
    try:
        # Check if the user_id exists in the database
        user_exists = db.query(ChatHistory).filter(ChatHistory.user_id == request.user_id).first() is not None
        if not user_exists:
            raise HTTPException(
                status_code=404,
                detail=f"No Chat history found for user ID: {request.user_id}."
            )
        return get_user_chat_history(user_id=request.user_id, db=db)
    except HTTPException as e:
        raise e
    except Exception as e:
        logging.error(f"Error in /chat-history endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error, please check the logs."
        )
