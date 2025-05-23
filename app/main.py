
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from pydantic import BaseModel
from app.extractor import extract_text_from_medium
from app.translator import translate_text_to_french
from app.summarize import generate_exec_summary
from typing import Optional, Dict

from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, JSONResponse
from app.tts import tts_handler

app = FastAPI()

class ExtractRequest(BaseModel):
    url: str
    cookies: Optional[Dict[str, str]] = None

class TranslateRequest(BaseModel):
    text: str

@app.post("/extract")
def extract(req: ExtractRequest):
    try:
        content = extract_text_from_medium(req.url, cookies=req.cookies)
        return {"text": content}
    except Exception as e:
        return {"error": str(e)}

@app.post("/translate")
def translate(req: TranslateRequest):
    try:
        french = translate_text_to_french(req.text)
        return {"translated": french}
    except Exception as e:
        return {"error": str(e)}

@app.post("/summarize")
async def summarize(request: Request):
    try:
        body = await request.json()
        text = body.get("text", "")
        summary = generate_exec_summary(text, sentence_count=3)
        return {"summarized": summary}
    except Exception as e:
        import traceback
        return JSONResponse(status_code=500, content={"error": traceback.format_exc()})

@app.post("/tts")
async def tts(request: Request):
    try:
        data = await request.json()
        return await tts_handler(data)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
