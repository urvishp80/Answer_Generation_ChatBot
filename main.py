import os
from fastapi import FastAPI
from api.endpoints import router as chatbot_router

app = FastAPI()

app.include_router(chatbot_router)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Clearbuy Product Recommendation Chatbot API"}

if __name__ == '__main__':
    import uvicorn
    port = int(os.environ.get('PORT', 5000))
    uvicorn.run(app, host="0.0.0.0", port=port)
