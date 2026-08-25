from .database import execute_query
from .gemini_engine import generate_sql
from .sql_validator import validate_sql


def _natural_answer(description: str, rows: list[dict]) -> str:
    if not rows:
        return "No encontré resultados para esa consulta."
    if len(rows) == 1 and len(rows[0]) == 1:
        value = next(iter(rows[0].values()))
        return f"{description.rstrip('.')} El resultado es {value}."
    if len(rows) == 1:
        details = ", ".join(f"{key}: {value}" for key, value in rows[0].items())
        return f"{description.rstrip('.')}: {details}."
    preview = "; ".join(", ".join(f"{key}: {value}" for key, value in row.items()) for row in rows[:5])
    return f"{description.rstrip('.')}. {preview}."


def ask(question: str) -> dict:
    interpretation = generate_sql(question)
    sql = validate_sql(interpretation["sql"])
    rows = execute_query(sql)
    description = interpretation.get("descripcion", "Consulta realizada")
    return {"answer": _natural_answer(description, rows), "results": rows, "sql": sql}
