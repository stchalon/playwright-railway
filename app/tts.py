from fastapi.responses import StreamingResponse, JSONResponse
from gtts import gTTS
import tempfile

async def tts_handler(data: dict):
    text = data.get("text")
    lang = data.get("lang", "en")

    if not text:
        return JSONResponse(status_code=400, content={"error": "Missing 'text'"})

    try:
        tts = gTTS(text=text, lang=lang)
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts.save(tmp.name)
        tmp.close()
        return StreamingResponse(open(tmp.name, "rb"), media_type="audio/mpeg")
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
