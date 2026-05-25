DROP TABLE IF EXISTS rasp_omgtu.schedule_gold;

SHOW TABLES FROM rasp_omgtu;

SELECT
    lesson_date,
    entity_type,
    entity_id,
    teacher_name,
    lesson_type,
    discipline,
    group_name,
    subgroup_name,
    room,
    pair_number,
    load_date
FROM rasp_omgtu.schedule_gold
ORDER BY lesson_date, entity_type, entity_id, pair_number
LIMIT 50;

SELECT
    entity_type,
    count() AS rows_count
FROM rasp_omgtu.schedule_gold
GROUP BY entity_type
ORDER BY entity_type;

SELECT
    entity_type,
    entity_id,
    count() AS lessons_count
FROM rasp_omgtu.schedule_gold
WHERE lesson_date BETWEEN toDate('2026-05-12') AND toDate('2026-05-18')
GROUP BY entity_type, entity_id
ORDER BY entity_type, entity_id;