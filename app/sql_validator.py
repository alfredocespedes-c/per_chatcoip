import re


def validate_sql(sql: str) -> str:
    clean = sql.strip()
    upper = clean.upper()
    if not upper.startswith("SELECT"):
        raise ValueError("Solo están permitidas consultas de lectura.")
    if ";" in clean[:-1]:
        raise ValueError("No se permiten múltiples consultas SQL.")
    tables = re.findall(r"\b(?:FROM|JOIN)\s+([a-zA-Z_][a-zA-Z0-9_]*)", clean, flags=re.IGNORECASE)
    if any(table.lower() != "incendios" for table in tables):
        raise ValueError("La consulta intenta acceder a una tabla no autorizada.")
    return clean
