from fastapi import APIRouter
from pydantic import BaseModel
from utils.chat_bot import ask_bot

router = APIRouter()

class MessageInput(BaseModel):
    message: str

@router.post("/chat-text/")
async def chat_text(input: MessageInput):
    print(f"Received text: {input.message}")
    try:
        reply = ask_bot(input.message)
        return {"question": input.message, "answer": reply}
    except Exception as e:
        print(f"Error: {e}")
        return {"error": str(e)}
