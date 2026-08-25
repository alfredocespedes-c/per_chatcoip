# Forestin - ChatCoip

POC de consulta conversacional sobre datos de incendios forestales.

**Versión:** 2026.08.25.1

## Arquitectura

- Python + FastAPI
- Gemini Cloud para interpretar preguntas
- SQLite con datos dummy para la POC
- PostgreSQL como destino para SIDCO
- Frontend HTML/CSS/JavaScript responsive

## Flujo

Pregunta → Gemini → SQL validado → base de datos → respuesta breve

## Seguridad

Las credenciales se configuran mediante `.env` y no deben versionarse. La capa SQL acepta únicamente consultas de lectura sobre tablas autorizadas.

## Desarrollo local

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python scripts/crear_dummy.py
uvicorn app.main:app --host 0.0.0.0 --port 8119
```

Abrir `http://127.0.0.1:8119`.
