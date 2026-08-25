from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from .chatcoip import ask

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"

app = FastAPI(title="Forestin - ChatCoip", version="2026.08.25.2")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://alfredocespedes-c.github.io",
        "http://127.0.0.1:8119",
        "http://localhost:8119",
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type"],
)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

class Question(BaseModel):
    pregunta: str

@app.get("/health")
def health():
    return {"status": "ok", "service": "forestin_chatcoip", "version": "2026.08.25.2"}

@app.get("/")
def home():
    return FileResponse(STATIC_DIR / "index.html")

@app.post("/api/preguntar")
def preguntar(payload: Question):
    question = payload.pregunta.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Escribe una pregunta.")
    try:
        result = ask(question)
        return {"respuesta": result["answer"]}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
