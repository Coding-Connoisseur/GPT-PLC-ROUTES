from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
import datetime
import os
import tempfile

router = APIRouter()

radio_logs = []  # basic in-memory log (timestamp, transcription, source)

class TextMessage(BaseModel):
    message: str
    voice: str = "default"

@router.post("/send")
def send_radio_message(msg: TextMessage):
    """Simulates sending a message over walkie (to be implemented with audio hardware)."""
    # TODO: generate speech + push to radio audio out
    ts = datetime.datetime.now().isoformat()
    radio_logs.append({"timestamp": ts, "direction": "outgoing", "text": msg.message})
    return {"status": "sent", "timestamp": ts}

@router.post("/receive")
def receive_radio_audio(file: UploadFile = File(...)):
    """Accepts uploaded radio audio file and simulates transcription."""
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(file.file.read())
            tmp_path = tmp.name

        # TODO: pass tmp_path to Whisper or other STT engine
        fake_transcript = f"[simulated transcript of {file.filename}]"
        ts = datetime.datetime.now().isoformat()
        radio_logs.append({"timestamp": ts, "direction": "incoming", "text": fake_transcript})

        os.remove(tmp_path)
        return {"status": "received", "transcript": fake_transcript, "timestamp": ts}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/logs")
def get_logs():
    """Returns recent radio messages."""
    return radio_logs[-25:]