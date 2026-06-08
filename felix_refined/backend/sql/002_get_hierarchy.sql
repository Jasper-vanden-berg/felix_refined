CREATE OR REPLACE VIEW diagnosis.diagnosis_closure_view AS
SELECT
    c.ancestor_id,
    c.descendant_id,
    c.depth,
    d.name AS descendant_name
FROM diagnosis.diagnosis_hierarchy c
JOIN diagnosis.diagnosis d ON d.id = c.descendant_id;