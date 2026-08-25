import json
import os
from datetime import date
from dotenv import load_dotenv
from google import genai

load_dotenv()


def generate_sql(question: str) -> dict:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("Falta GEMINI_API_KEY en .env")

    client = genai.Client(api_key=api_key)
    prompt = f'''Eres el intérprete SQL de Forestin - ChatCoip.
Fecha actual: {date.today().isoformat()}.
Tabla incendios: id INTEGER, ubicacion TEXT, region TEXT, hectareas REAL, estado TEXT, fecha DATE.
Estados: Controlado, No controlado.
Convierte la pregunta a SQL SQLite. Solo SELECT. Usa fechas YYYY-MM-DD. Para "este año" usa el año actual y para "año pasado" el anterior. Máximo 20 filas en listados.
Devuelve EXCLUSIVAMENTE JSON válido con: {{"sql":"SELECT ...","descripcion":"..."}}.
Pregunta: {question}'''

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt,
    )
    text = response.text.strip().replace("```json", "").replace("```", "").strip()
    return json.loads(text)
