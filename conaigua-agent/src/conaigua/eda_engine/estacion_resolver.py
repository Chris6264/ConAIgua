import unicodedata

import pandas as pd

NOMBRE_COL = "nombre_estacion"


class EstacionNoEncontradaError(Exception):
    def __init__(self, query: str):
        self.query = query
        super().__init__(f"No se encontraron datos para estación {query}.")


class EstacionAmbiguaError(Exception):
    def __init__(self, query: str, candidatos: list[str]):
        self.query = query
        self.candidatos = candidatos
        super().__init__(f"Estación ambigua: {query}")


def _normalize(text: str) -> str:
    text = str(text).strip().upper()
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    return " ".join(text.split())


def resolve_estacion_id(df: pd.DataFrame, query: str) -> tuple[str | None, list[str]]:
    """
    Resuelve un identificador de estación a partir de una clave numérica,
    un nombre exacto o un nombre parcial.

    Retorna una tupla (estacion_id, candidatos):
    - Si se resuelve a una única estación: (estacion_id, [])
    - Si hay ambigüedad (varias coincidencias): (None, [lista_de_candidatos])
    - Si no hay ninguna coincidencia: (None, [])

    Usar esta versión cuando se quiera manejar el resultado manualmente
    (ej. report_tool, que no pasa por filter_data).
    """
    query_norm = _normalize(query)

    ids = df["estacion_id"].astype(str)
    if query.strip() in ids.values:
        return query.strip(), []

    if NOMBRE_COL not in df.columns:
        return None, []

    nombres_norm = df[NOMBRE_COL].astype(str).map(_normalize)

    exact_matches = df.loc[nombres_norm == query_norm, "estacion_id"].astype(str).unique()
    if len(exact_matches) == 1:
        return exact_matches[0], []
    if len(exact_matches) > 1:
        return None, list(exact_matches)

    partial_mask = nombres_norm.str.contains(query_norm, na=False)
    partial_matches = df.loc[partial_mask, ["estacion_id", NOMBRE_COL]].drop_duplicates()

    if len(partial_matches) == 1:
        return str(partial_matches.iloc[0]["estacion_id"]), []
    if len(partial_matches) > 1:
        candidatos = [
            f"{row['estacion_id']} ({row[NOMBRE_COL]})"
            for _, row in partial_matches.iterrows()
        ]
        return None, candidatos

    return None, []


def resolve_estacion_id_or_raise(df: pd.DataFrame, query: str) -> str:
    """
    Igual que resolve_estacion_id, pero lanza excepciones en vez de
    devolver None. Pensada para usarse dentro de filter_data, para que
    todas las tools que filtran datos resuelvan estación automáticamente
    sin tener que repetir el manejo de ambigüedad/no-encontrado.
    """
    resolved_id, candidatos = resolve_estacion_id(df, query)

    if resolved_id is None and candidatos:
        raise EstacionAmbiguaError(query, candidatos)

    if resolved_id is None:
        raise EstacionNoEncontradaError(query)

    return resolved_id