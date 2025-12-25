-- Создаём таблицу books
CREATE TABLE public.books (
    id SERIAL PRIMARY KEY,
    isbn TEXT,
    title TEXT,
    description TEXT,
    year INTEGER,
    rating FLOAT,
    rating_count INTEGER,
    pages INTEGER,
    authors INTEGER[]
);

--импортируем через скрипт (Lab10.py)

--проверим
SELECT COUNT(*) FROM books;
SELECT title, description FROM books LIMIT 3;

-- Добавляем сгенерированный столбец search_vector
ALTER TABLE books
ADD COLUMN search_vector tsvector
GENERATED ALWAYS AS (
    setweight(to_tsvector('english', coalesce(title, '')), 'A') ||
    setweight(to_tsvector('english', coalesce(description, '')), 'B')
) STORED;

-- Создаём GIN-индекс для ускорения поиска
CREATE INDEX idx_books_search ON books USING GIN(search_vector);

-- поиск и ранжирование
SELECT
    title,
    description,
    ts_rank(search_vector, websearch_to_tsquery('english', 'harry potter')) AS rank
FROM books
WHERE search_vector @@ websearch_to_tsquery('english', 'harry potter')
ORDER BY rank DESC
LIMIT 10;

-- Подсчёт количества книг, содержащих "Harry Potter"
SELECT COUNT(*)
FROM books
WHERE search_vector @@ plainto_tsquery('english', 'Harry Potter');

-- пользовательское ранжирование 
SELECT
    title,
    description,
    rating,
    rating_count,
    (
        ts_rank(search_vector, websearch_to_tsquery('english', 'harry potter')) * 0.5 +
        (rating / 5.0) * 0.25 +
        (log(rating_count + 1) / log((SELECT MAX(rating_count) FROM books))) * 0.25
    ) AS custom_rank
FROM books
WHERE search_vector @@ websearch_to_tsquery('english', 'harry potter')
ORDER BY custom_rank DESC
LIMIT 10;

--выделение совпадений
SELECT ts_headline('english', title, websearch_to_tsquery('english', 'Harry Potter')) AS highlighted_title,
       ts_headline('english', description, websearch_to_tsquery('english', 'Harry Potter')) AS highlighted_desc
FROM books
WHERE search_vector @@ websearch_to_tsquery('english', 'Harry Potter')
LIMIT 5;
