import json
import gzip
import psycopg2
from psycopg2.extras import execute_values

# Параметры подключения к БД
DB_CONFIG = {
    'dbname': 'goodreads',
    'user': 'postgres',
    'password': '0000',
    'host': 'localhost',
    'port': '5432'
}

# Путь к JSON-файлу (сейчас .gz)
JSON_FILE_PATH = 'goodreads_books.json.gz'  

BATCH_SIZE = 5000

def create_table(conn):
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id SERIAL PRIMARY KEY,
                title TEXT,
                description TEXT,
                rating NUMERIC,
                rating_count INTEGER
            );
        """)
        conn.commit()
    print(" Таблица 'books' создана или уже существует.")

def parse_json_line(line):
    try:
        data = json.loads(line)
        title = data.get('title') or ''
        description = data.get('description') or ''
        rating_str = data.get('average_rating', '0')
        rating = float(rating_str) if rating_str not in (None, '', '0') else 0.0
        rating_count = int(data.get('ratings_count', 0) or 0)
        return (title, description, rating, rating_count)
    except Exception:
        return None

def import_books():
    conn = psycopg2.connect(**DB_CONFIG)
    create_table(conn)

    batch = []
    total = 0
    skipped = 0

    # Открываем .gz файл
    with gzip.open(JSON_FILE_PATH, 'rt', encoding='utf-8') as f:
        for line in f:
            record = parse_json_line(line)
            if record is None:
                skipped += 1
                continue

            batch.append(record)

            if len(batch) >= BATCH_SIZE:
                insert_batch(conn, batch)
                total += len(batch)
                print(f" Вставлено {total} записей...")
                batch = []

    # Вставляем остаток
    if batch:
        insert_batch(conn, batch)
        total += len(batch)
        print(f" Вставлено {total} записей (финальный батч).")

    print(f" Импорт завершён. Всего: {total} записей. Пропущено: {skipped}")
    conn.close()

def insert_batch(conn, batch):
    try:
        with conn.cursor() as cur:
            execute_values(
                cur,
                "INSERT INTO books (title, description, rating, rating_count) VALUES %s",
                batch
            )
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f" Ошибка при вставке батча: {e}")
        raise

if __name__ == '__main__':
    import_books()