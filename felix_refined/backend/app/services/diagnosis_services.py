from ..crud.diagnosis import (
    get_diagnosis_dictionary,
    get_diagnosis_closure,
)


def extract_ids(matches):
    return list({m["id"] for m in matches if "id" in m})


def build_tree(rows):
    """
    Builds hierarchy from closure table rows.
    """

    nodes = {}

    # create nodes
    for r in rows:
        did = r["descendant_id"]
        if did not in nodes:
            nodes[did] = {
                "id": did,
                "children": []
            }

    # build parent-child links using closure relationships
    child_map = {}

    for r in rows:
        if r["ancestor_id"] != r["descendant_id"]:
            child_map.setdefault(r["ancestor_id"], set()).add(r["descendant_id"])

    for parent_id, children in child_map.items():
        if parent_id not in nodes:
            nodes[parent_id] = {"id": parent_id, "children": []}

        for c in children:
            nodes[parent_id]["children"].append(nodes[c])

    # roots = depth 0 entries
    roots = [
        nodes[r["descendant_id"]]
        for r in rows
        if r["depth"] == 0
    ]

    # deduplicate roots
    seen = set()
    unique = []

    for r in roots:
        if r["id"] not in seen:
            unique.append(r)
            seen.add(r["id"])

    return unique


def find_diagnoses_service(db, text: str, find_best_matches_fn):
    """
    Full pipeline:
    text -> matches -> ids -> closure -> tree
    """

    dictionary = get_diagnosis_dictionary(db)
    matches = find_best_matches_fn(text, dictionary)

    ids = extract_ids(matches)

    rows = get_diagnosis_closure(db, ids)

    tree = build_tree(rows)

    return tree