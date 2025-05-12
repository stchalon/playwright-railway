from fastapi import APIRouter
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel
from gtts import gTTS
import tempfile

router = APIRouter()

class TTSRequest(BaseModel):
    text: str
    lang: str = "en"

@router.post("/tts")
async def tts(request: TTSRequest):
    try:
        tts = gTTS(text=request.text, lang=request.lang)
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts.save(tmp.name)
        tmp.close()
        return StreamingResponse(open(tmp.name, "rb"), media_type="audio/mpeg")
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
