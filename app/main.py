
from fastapi import FastAPI, Request
from pydantic import BaseModel
from app.extractor import extract_text_from_medium
from app.translator import translate_text_to_french
from typing import Optional, Dict

from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
import sys
import os

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
def summarize(req: TranslateRequest):
    try:
        content = generate_exec_summary(req.text, sentence_count=3)
        return {"summarized": content}
    except Exception as e:
        return {"error": str(e)}
