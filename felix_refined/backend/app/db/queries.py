def fetch_diagnoses(conn):
    query = """
    SELECT
        d.id AS diagnosis_id,
        d.name AS diagnosis_name,
        s.synonym
    FROM diagnosis.diagnosis d
    LEFT JOIN diagnosis.diagnosis_synonyms s
        ON d.id = s.diagnosis_id
    """
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()
    
    
def fetch_attributes(conn, diagnosis_id):
    query = """
    SELECT diagnosis_id, attribute_id
    FROM diagnosis.diagnosis_attributes
    WHERE diagnosis_id = %s
    """

    with conn.cursor() as cur:
        cur.execute(query, (diagnosis_id,))
        return cur.fetchall()
    


def fetch_closure_table(
    conn,
    table: str,
    target_id: int,
    direction: str = "descendant",  # "ancestor" or "descendant"
    depth: int | None = None
):
    """
    Generic closure table fetcher for diagnosis / attributes / any taxonomy.
    """

    if direction not in ("ancestor", "descendant"):
        raise ValueError("direction must be 'ancestor' or 'descendant'")
    
    if table not in {"diagnosis.diagnosis_hierarchy","diagnosis.attributes_hierarchy"}:
        raise ValueError("Invalid table")

    filter_col = "descendant_id" if direction == "descendant" else "ancestor_id"

    query = f"""
        SELECT ancestor_id, descendant_id, depth
        FROM {table}
        WHERE {filter_col} = %s
    """

    params = [target_id]

    if depth is not None:
        query += " AND depth <= %s"
        params.append(depth)

    with conn.cursor() as cur:
        cur.execute(query, params)
        return cur.fetchall()