from sqlalchemy.orm import Session
from sqlalchemy import text

def get_diagnosis_dictionary(db):
    query = text("""
        SELECT
            diagnosis_id,
            match_text,
            canonical_name
        FROM diagnosis.diagnosis_search
    """)

    rows = db.execute(query).fetchall()

    return [
        {
            "match": r[1].lower(),
            "canonical": r[2],
            "id": r[0]
        }
        for r in rows
    ]

def get_diagnosis_closure(db, ancestor_ids: list[int]):
    """
    Fetches hierarchy from closure table for given root diagnoses.

    Returns flat closure rows:
    ancestor_id, descendant_id, depth
    """

    if not ancestor_ids:
        return []

    query = text("""
        SELECT
            ancestor_id,
            descendant_id,
            depth
        FROM diagnosis.diagnosis_closure_view
        WHERE ancestor_id = ANY(:ids)
        ORDER BY depth ASC
    """)

    rows = db.execute(query, {"ids": ancestor_ids}).fetchall()

    return [
        {
            "ancestor_id": r[0],
            "descendant_id": r[1],
            "depth": r[2],
        }
        for r in rows
    ]


def extract_diagnosis_ids(matches: list[dict]):
    """
    Converts match results into unique diagnosis IDs.
    """

    return list({m["id"] for m in matches if "id" in m})