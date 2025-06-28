
from fastapi import FastAPI
from routes.voice_chat import router as voice_router
from routes.text_chat import router as text_router

app = FastAPI()

app.include_router(voice_router)
app.include_router(text_router)


@app.get("/")
def root():
    return {"message": "Ayouta API is running 🦋"}