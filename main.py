from fastapi import FastAPI
from api.endpoints import router as chatbot_router

app = FastAPI()

app.include_router(chatbot_router)

@app.get("/")
# def read_root():
async def read_root():
    return {"message": "Welcome to the Clearbuy Product Recommendation Chatbot API"}
