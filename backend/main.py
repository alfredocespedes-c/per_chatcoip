"""Punto de entrada compatible con Render.

Mantiene el comando existente `uvicorn backend.main:app` y reutiliza
la aplicación FastAPI real definida en `app.main`.
"""

from app.main import app

__all__ = ["app"]
