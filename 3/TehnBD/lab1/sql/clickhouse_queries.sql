--DROP TABLE IF EXISTS rasp_omgtu.schedule_gold;

SHOW TABLES FROM rasp_omgtu;

SELECT *
FROM rasp_omgtu.schedule_gold
LIMIT 20;

SELECT
    teacher_name,
    lesson_type,
    count() AS lessons_count
FROM rasp_omgtu.schedule_gold
WHERE lesson_date BETWEEN toDate('2026-04-13') AND toDate('2026-04-20')
GROUP BY teacher_name, lesson_type
ORDER BY teacher_name, lessons_count DESC;