from rapidfuzz import fuzz
from app.utils.text import normalize
from app.services.hierarchy import (
    build_diagnosis_map,
    build_limited_hierarchy,
)
from app.db.session import get_conn
from app.db.queries import fetch_attributes
from app.services.hierarchy import (
    build_diagnosis_map,
    build_attribute_structure,
    build_limited_hierarchy
)

conn = get_conn()


# -----------------------------
# STEP A: LOAD DIAGNOSES
# -----------------------------
def load_all_diagnoses(conn):
    from app.db.queries import fetch_diagnoses

    rows = fetch_diagnoses(conn)

    synonym_map = {}
    base_rows = []

    for r in rows:
        base_rows.append(r)

        cid = r["diagnosis_id"]
        syn = r["synonym"]

        if cid not in synonym_map:
            synonym_map[cid] = []

        if syn:
            synonym_map[cid].append(syn)

    return base_rows, synonym_map


# -----------------------------
# STEP B: FILTER CANDIDATES (unchanged)
# -----------------------------
def get_candidate_ids(line, base_rows, limit=50):
    line_n = normalize(line)
    line_tokens = set(line_n.split())

    scored = []

    for r in base_rows:
        name_tokens = set(normalize(r["diagnosis_name"]).split())
        overlap = len(line_tokens & name_tokens)
        scored.append((overlap, r["diagnosis_id"]))

    scored.sort(reverse=True, key=lambda x: x[0])

    seen = set()
    result = []

    for _, cid in scored:
        if cid not in seen:
            seen.add(cid)
            result.append(cid)
        if len(result) >= limit:
            break

    return set(result)


# -----------------------------
# STEP D: LINE FUZZY SCORING (ONLY for ranking within matched context)
# -----------------------------
def score_line(line_n, diagnosis_name):
    """
    Used ONLY if exact match fails.
    """
    diag_n = normalize(diagnosis_name)
    return fuzz.partial_ratio(line_n, diag_n) / 100


# -----------------------------
# STEP E: FIND BEST MATCH (FIXED LOGIC)
# -----------------------------
def find_best_match(line, base_rows, synonym_map, candidate_ids):
    line_n = normalize(line)

    best_fuzzy = None
    best_fuzzy_score = 0

    exact_matches = []

    for r in base_rows:
        cid = r["diagnosis_id"]

        if cid not in candidate_ids:
            continue

        diagnosis_name = r["diagnosis_name"]
        synonyms = synonym_map.get(cid, [])

        all_forms = [diagnosis_name] + synonyms

        # -----------------------------
        # 1. EXACT MATCH COLLECTION
        # -----------------------------
        for form in all_forms:
            if normalize(form) == line_n:
                exact_matches.append({
                    "diagnosis_id": cid,
                    "diagnosis_name": diagnosis_name,
                    "matched_text": form,
                })

        # -----------------------------
        # 2. FUZZY FALLBACK
        # -----------------------------
        score = fuzz.partial_ratio(line_n, normalize(diagnosis_name)) / 100

        if score > best_fuzzy_score:
            best_fuzzy_score = score
            best_fuzzy = {
                "diagnosis_id": cid,
                "diagnosis_name": diagnosis_name,
                "matched_text": diagnosis_name,
                "score": round(score, 4),
            }

    # -----------------------------
    # 3. RESOLVE EXACT MATCHES
    # -----------------------------
    if exact_matches:
        best_exact = max(
            exact_matches,
            key=lambda x: len(x["matched_text"])
        )

        return {
            "diagnosis_id": best_exact["diagnosis_id"],
            "diagnosis_name": best_exact["diagnosis_name"],
            "matched_text": best_exact["matched_text"],
            "score": 1.0,
        }

    return best_fuzzy


# -----------------------------
# STEP F: PIPELINE
# -----------------------------
def process_lines(lines):
    conn = get_conn()

    # -----------------------------
    # LOAD ONCE (IMPORTANT)
    # -----------------------------
    base_rows, synonym_map = load_all_diagnoses(conn)
    diagnosis_map = build_diagnosis_map(conn)

    results = []

    # -----------------------------
    # PROCESS EACH LINE
    # -----------------------------
    for line in lines:

        candidate_ids = get_candidate_ids(line, base_rows)

        match = find_best_match(
            line,
            base_rows,
            synonym_map,
            candidate_ids
        )

        if not match:
            results.append({
                "line": line,
                "match": None,
                "hierarchy": [],
                "attributes": []
            })
            continue

        diag_id = match["diagnosis_id"]

        # -----------------------------
        # HIERARCHY (NEW LOGIC)
        # -----------------------------
        hierarchy = build_limited_hierarchy(
            conn,
            diag_id,
            diagnosis_map
        )

        # -----------------------------
        # ATTRIBUTES
        # -----------------------------
        attributes_raw = fetch_attributes(conn, diag_id)

        attributes = build_attribute_structure(
            conn,
            attributes_raw
        )

        # -----------------------------
        # RESULT
        # -----------------------------
        results.append({
            "line": line,
            "match": match,
            "hierarchy": hierarchy,
            "attributes": attributes
        })

    return results