from fastapi import FastAPI
from api.endpoints import router as chatbot_router

app = FastAPI()

app.include_router(chatbot_router)

@app.get("/")
# def read_root():
async def read_root():
    return {"message": "Welcome to the Clearbuy Product Recommendation Chatbot API"}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8878)
