CREATE OR REPLACE VIEW diagnosis.diagnosis_search AS

SELECT
    d.id AS diagnosis_id,
    d.name AS canonical_name,
    d.name AS match_text
FROM diagnosis.diagnosis d

UNION

SELECT
    d.id AS diagnosis_id,
    d.name AS canonical_name,
    s.synonym AS match_text
FROM diagnosis.diagnosis_synonyms s
JOIN diagnosis.diagnosis d ON d.id = s.diagnosis_id;