from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, JSONResponse
from gtts import gTTS
import tempfile

app = FastAPI()

@app.post("/tts")
async def tts(request: Request):
    data = await request.json()
    text = data.get("text", "")
    lang = data.get("lang", "en")

    if not text:
        return JSONResponse(status_code=400, content={"error": "Missing 'text'"})

    try:
        tts = gTTS(text=text, lang=lang)
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts.save(temp_file.name)
        temp_file.close()

        return StreamingResponse(open(temp_file.name, "rb"), media_type="audio/mpeg")
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
