

-- Начинаем транзакцию для безопасной демонстрации
BEGIN;

-- Этап 1: Создание таблицы для хранения книг из Goodreads
-- Включены все необходимые поля: ISBN, название, описание, рейтинг и др.
CREATE TABLE IF NOT EXISTS public.books (
    id SERIAL PRIMARY KEY,
    isbn TEXT,
    title TEXT,
    description TEXT,
    year INTEGER,
    rating FLOAT,
    rating_count INTEGER,
    pages INTEGER,
    authors INTEGER[]  -- Массив ID авторов (для будущих связей, не используется в FTS)
);

-- Примечание: данные загружаются отдельным Python-скриптом Lab10.py
-- Скрипт читает goodreads_books.json.gz и вставляет записи пакетами

-- Этап 2: Проверка успешности импорта
-- Подсчёт общего числа записей в таблице
SELECT COUNT(*) AS total_books FROM books;

-- Просмотр первых 3 записей для визуальной проверки
SELECT title, description FROM books LIMIT 3;

-- Этап 3: Создание сгенерированного tsvector-столбца для FTS
-- Вес 'A' присваивается заголовку (высокая релевантность),
-- вес 'B' — описанию (средняя релевантность)
ALTER TABLE books
ADD COLUMN IF NOT EXISTS search_vector tsvector
GENERATED ALWAYS AS (
    setweight(to_tsvector('english', coalesce(title, '')), 'A') ||
    setweight(to_tsvector('english', coalesce(description, '')), 'B')
) STORED;

-- Этап 4: Создание GIN-индекса для ускорения полнотекстового поиска
-- Индекс позволяет избежать полного сканирования таблицы (Seq Scan)
CREATE INDEX IF NOT EXISTS idx_books_search ON books USING GIN(search_vector);

-- Этап 5: Базовый полнотекстовый поиск с ранжированием по релевантности
-- Используется websearch_to_tsquery — удобен для пользовательского ввода
SELECT
    title,
    description,
    ts_rank(search_vector, websearch_to_tsquery('english', 'harry potter')) AS rank
FROM books
WHERE search_vector @@ websearch_to_tsquery('english', 'harry potter')
ORDER BY rank DESC
LIMIT 10;

-- Дополнительная проверка: количество книг, содержащих "Harry Potter"
-- Используем plainto_tsquery для сравнения с методичкой
SELECT COUNT(*) AS harry_potter_books
FROM books
WHERE search_vector @@ plainto_tsquery('english', 'Harry Potter');

-- Этап 6: Пользовательское ранжирование (рис. 22 из методички)
-- Учитываем: релевантность (50%), рейтинг (25%), популярность (25%)
-- Логарифмическая нормализация предотвращает доминирование "выбросов"
SELECT
    title,
    description,
    rating,
    rating_count,
    (
        ts_rank(search_vector, websearch_to_tsquery('english', 'harry potter')) * 0.5 +
        (COALESCE(rating, 0) / 5.0) * 0.25 +
        (log(rating_count + 1) / log((SELECT MAX(rating_count) FROM books))) * 0.25
    ) AS custom_rank
FROM books
WHERE search_vector @@ websearch_to_tsquery('english', 'harry potter')
ORDER BY custom_rank DESC
LIMIT 10;

-- Этап 7: Выделение совпадений в результатах поиска (функция ts_headline)
-- Позволяет показать пользователю "почему" книга попала в результаты
SELECT
    ts_headline('english', title, websearch_to_tsquery('english', 'Harry Potter')) AS highlighted_title,
    ts_headline('english', description, websearch_to_tsquery('english', 'Harry Potter')) AS highlighted_desc,
    rating
FROM books
WHERE search_vector @@ websearch_to_tsquery('english', 'Harry Potter')
ORDER BY ts_rank(search_vector, websearch_to_tsquery('english', 'Harry Potter')) DESC
LIMIT 5;

-- Этап 8: Проверка плана выполнения — убедимся, что используется индекс
-- В выводе должно быть "Bitmap Index Scan on idx_books_search"
EXPLAIN (ANALYZE, BUFFERS)
SELECT title
FROM books
WHERE search_vector @@ plainto_tsquery('english', 'Harry Potter');


ROLLBACK;  --  COMMIT, если нужно сохранить созданную таблицу и индекс
