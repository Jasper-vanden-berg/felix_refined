from app.db.queries import fetch_diagnoses, fetch_closure_table


# -----------------------------
# DIAGNOSIS MAP (id → name)
# -----------------------------
def build_diagnosis_map(conn):
    rows = fetch_diagnoses(conn)

    return {
        r["diagnosis_id"]: r["diagnosis_name"]
        for r in rows
    }


# -----------------------------
# ATTRIBUTE STRUCTURE (UPDATED)
# -----------------------------
def build_attribute_structure(conn, attributes):
    result = []

    for a in attributes:
        children = fetch_closure_table(
            conn,
            "diagnosis.attributes_hierarchy",
            a["attribute_id"],
            direction="ancestor",
            depth=1
        )

        result.append({
            "attribute_id": a["attribute_id"],
            "values": [x["descendant_id"] for x in children]
        })

    return result


# -----------------------------
# CORE: LIMITED HIERARCHY BUILDER
# -----------------------------
def build_limited_hierarchy(conn, match_id, diagnosis_map):
    """
    Returns:
    - parent(s) of match
    - children + grandchildren (depth <= 2)
    """

    # -------------------------
    # STEP 1: GET PARENTS
    # -------------------------
    parent_rows = fetch_closure_table(
        conn,
        "diagnosis.diagnosis_hierarchy",
        match_id,
        direction="descendant",
        depth=1
    )

    parent_ids = list({r["ancestor_id"] for r in parent_rows})

    if not parent_ids:
        return []

    # -------------------------
    # STEP 2: GET SUBTREE (DEPTH ≤ 2)
    # -------------------------
    subtree = []

    for pid in parent_ids:
        rows = fetch_closure_table(
            conn,
            "diagnosis.diagnosis_hierarchy",
            pid,
            direction="ancestor",
            depth=2
        )
        subtree.extend(rows)

    # -------------------------
    # STEP 3: BUILD NODE MAP
    # -------------------------
    nodes = {}

    for r in subtree:
        a = r["ancestor_id"]
        d = r["descendant_id"]

        if a not in nodes:
            nodes[a] = {
                "value": a,
                "title": diagnosis_map.get(a, str(a)),
                "children": []
            }

        if d not in nodes:
            nodes[d] = {
                "value": d,
                "title": diagnosis_map.get(d, str(d)),
                "children": []
            }

    # -------------------------
    # STEP 4: BUILD EDGES (NO RECURSION)
    # -------------------------
    children_map = {}

    for r in subtree:
        a = r["ancestor_id"]
        d = r["descendant_id"]

        if a != d:
            children_map.setdefault(a, set()).add(d)

    for parent, children in children_map.items():
        nodes[parent]["children"] = [
            nodes[c] for c in children if c in nodes
        ]

    # -------------------------
    # STEP 5: ROOT NODES ONLY
    # -------------------------
    all_children = {c for children in children_map.values() for c in children}
    roots = [n for n in nodes if n not in all_children]

    return [nodes[r] for r in roots]


# -----------------------------
# OPTIONAL: FLAT HIERARCHY ENRICHMENT
# -----------------------------
def enrich_hierarchy(hierarchy, diagnosis_map):
    return [
        {
            "ancestor_id": h["ancestor_id"],
            "ancestor_name": diagnosis_map.get(h["ancestor_id"], str(h["ancestor_id"])),
            "descendant_id": h["descendant_id"],
            "descendant_name": diagnosis_map.get(h["descendant_id"], str(h["descendant_id"])),
            "depth": h["depth"],
        }
        for h in hierarchy
    ]