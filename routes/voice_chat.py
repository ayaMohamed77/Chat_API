from fastapi import APIRouter, UploadFile, File
import uuid
from pydub import AudioSegment
import os
from utils.stt import voice_to_text

router = APIRouter()

@router.post("/chat-voice/")
async def chat_with_voice(file: UploadFile = File(...)):
    file_extension = file.filename.split(".")[-1]
    temp_filename = f"temp_audio_{uuid.uuid4()}.{file_extension}"
    with open(temp_filename, "wb") as buffer:
        buffer.write(await file.read())

    def convert_audio_to_wav_16000_mono(input_path: str) -> str:
        output_path = input_path.rsplit(".", 1)[0] + "_converted.wav"
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

        return {
            "transcription": question
        }

    except Exception as e:
        return {"error": str(e)}

    finally:
        for path in [temp_filename, converted_path]:
            if os.path.exists(path):
                os.remove(path)
