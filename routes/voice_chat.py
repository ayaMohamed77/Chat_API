# routes/voice_chat.py

from fastapi import APIRouter, UploadFile, File
import uuid
from pydub import AudioSegment
import os
from utils.stt import voice_to_text
from utils.chat_bot import ask_bot

router = APIRouter()

@router.post("/chat-voice/")
async def chat_with_voice(file: UploadFile = File(...)):

    temp_filename = f"temp_audio_{uuid.uuid4()}.wav"
    with open(temp_filename, "wb") as buffer:
        buffer.write(await file.read())

    def convert_audio_to_wav_16000_mono(input_path: str) -> str:
        output_path = input_path.replace(".", "_converted.")
        audio = AudioSegment.from_file(input_path)
        audio = audio.set_channels(1)
        audio = audio.set_frame_rate(16000)
        audio.export(output_path, format="wav")
        return output_path

    converted_path = convert_audio_to_wav_16000_mono(temp_filename)

    try:
        question = voice_to_text(converted_path)

        if not question:
            return {"error": "No speech detected."}

        answer = ask_bot(question)

        return {
            "question": question,
            "answer": answer
        }

    except Exception as e:
        return {"error": str(e)}

    finally:
        if os.path.exists(temp_filename):
            os.remove(temp_filename)
        if os.path.exists(converted_path):
            os.remove(converted_path)
