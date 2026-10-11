"""
FastAPI server for phonetic translator.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
import logging

from translator import PhoneticTranslator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Phonetic Translator API",
    description="Translate text between languages via phonetic transcription",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

translator = PhoneticTranslator()


class TranslateRequest(BaseModel):
    text: str
    source: str
    target: str


class TranslateResponse(BaseModel):
    source: str
    target: str
    src_ipa: str
    tgt_ipa: str
    confidence: float
    source_lang: str
    target_lang: str


class BatchRequest(BaseModel):
    items: List[TranslateRequest]


class BatchResponse(BaseModel):
    results: List[TranslateResponse]


class TransliterateRequest(BaseModel):
    text: str
    language: str


class TransliterateResponse(BaseModel):
    text: str
    ipa: str
    language: str


@app.get("/")
def root():
    return {"message": "Phonetic Translator API", "version": "1.0.0", "docs": "/docs"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/languages")
def list_languages():
    return {"languages": translator.supported_languages()}


@app.post("/translate", response_model=TranslateResponse)
def translate(request: TranslateRequest):
    try:
        result = translator.translate(request.text, request.source, request.target)
        return TranslateResponse(**result)
    except Exception as e:
        logger.error(f"Translation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/batch", response_model=BatchResponse)
def batch_translate(request: BatchRequest):
    try:
        items = [(item.text, item.source, item.target) for item in request.items]
        results = translator.batch_translate(items)
        return BatchResponse(results=[TranslateResponse(**r) for r in results])
    except Exception as e:
        logger.error(f"Batch translation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/transliterate", response_model=TransliterateResponse)
def transliterate(request: TransliterateRequest):
    try:
        ipa = translator.text_to_ipa(request.text, request.language)
        return TransliterateResponse(text=request.text, ipa=ipa, language=request.language)
    except Exception as e:
        logger.error(f"Transliteration failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
