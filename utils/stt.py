import wave
import vosk
import json

model = vosk.Model("vosk-model-small-en-us-0.15")

def voice_to_text(audio_path: str) -> str:
    wf = wave.open(audio_path, "rb")

    if wf.getnchannels() != 1 or wf.getframerate() != 16000:
        raise ValueError("Audio must be mono and 16000 Hz")

    rec = vosk.KaldiRecognizer(model, wf.getframerate())

    results = ""
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            results += json.loads(rec.Result())["text"] + " "

    results += json.loads(rec.FinalResult())["text"]
    return results.strip()
