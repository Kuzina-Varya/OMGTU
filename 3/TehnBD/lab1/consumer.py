import json
import os
import re
import traceback
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path

import clickhouse_connect
import pika


def load_env_file() -> None:
    """
    Загружает переменные из .env для локального запуска.

    Важно:
    - если переменная уже задана в системе или docker-compose, она НЕ перезаписывается;
    - сначала ищем .env рядом с consumer.py;
    - если consumer.py лежит в consumer_app, дополнительно ищем .env на уровень выше.
    """
    current_dir = Path(__file__).resolve().parent

    possible_paths = [
        current_dir / ".env",
        current_dir.parent / ".env",
    ]

    env_path = next((path for path in possible_paths if path.exists()), None)

    if env_path is None:
        print("Файл .env не найден. Будут использованы только переменные окружения системы.")
        return

    print(f"Загружаю переменные окружения из файла: {env_path}")

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()

        if not line or line.startswith("#"):
            continue

        if "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")

        if key:
            os.environ.setdefault(key, value)


def required_env(name: str) -> str:
    value = os.getenv(name)

    if value is None or value.strip() == "":
        raise RuntimeError(f"Не задана обязательная переменная окружения: {name}")

    return value.strip()


def required_int_env(name: str) -> int:
    value = required_env(name)

    try:
        return int(value)
    except ValueError as exc:
        raise RuntimeError(
            f"Переменная окружения {name} должна быть числом, сейчас: {value}"
        ) from exc


def safe_identifier(value: str, env_name: str) -> str:
    """
    Проверяет имя БД/таблицы перед вставкой в SQL.

    Имена БД и таблиц нельзя передавать через parameters как обычные значения,
    поэтому они вставляются в SQL через f-string. Чтобы это было безопаснее,
    разрешаем только буквы, цифры и подчёркивание.
    """
    if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", value):
        raise RuntimeError(
            f"Некорректное значение {env_name}: {value}. "
            "Разрешены только буквы, цифры и подчёркивание."
        )

    return value


load_env_file()

RABBITMQ_HOST = required_env("RABBITMQ_HOST")
RABBITMQ_PORT = required_int_env("RABBITMQ_PORT")
RABBITMQ_USER = required_env("RABBITMQ_USER")
RABBITMQ_PASSWORD = required_env("RABBITMQ_PASSWORD")
RABBITMQ_VHOST = required_env("RABBITMQ_VHOST")

REQUEST_QUEUE = required_env("RABBITMQ_REQUEST_QUEUE")
RESPONSE_QUEUE = required_env("RABBITMQ_RESPONSE_QUEUE")

CLICKHOUSE_HOST = required_env("CLICKHOUSE_HOST")
CLICKHOUSE_PORT = required_int_env("CLICKHOUSE_PORT")
CLICKHOUSE_USER = required_env("CLICKHOUSE_USER")
CLICKHOUSE_PASSWORD = required_env("CLICKHOUSE_PASSWORD")
CLICKHOUSE_DATABASE = safe_identifier(required_env("CLICKHOUSE_DATABASE"), "CLICKHOUSE_DATABASE")
CLICKHOUSE_TABLE = safe_identifier(required_env("CLICKHOUSE_TABLE"), "CLICKHOUSE_TABLE")

TEACHER_TYPE = required_env("ENTITY_TYPE_TEACHER")
GROUP_TYPE = required_env("ENTITY_TYPE_GROUP")
AUDITORIUM_TYPE = required_env("ENTITY_TYPE_AUDITORIUM")

PAIR_TIMES = {
    1: ("08:00", "09:35"),
    2: ("09:45", "11:20"),
    3: ("11:40", "13:15"),
    4: ("13:45", "15:20"),
    5: ("15:30", "17:05"),
    6: ("17:15", "18:50"),
}


def parse_date(value: str):
    return datetime.strptime(value, "%Y-%m-%d").date()


def date_range(start_date, end_date):
    current = start_date

    while current <= end_date:
        yield current
        current += timedelta(days=1)


def count_windows(pair_numbers):
    """
    Считает количество окон внутри дня.
    """
    if len(pair_numbers) <= 1:
        return 0

    pairs = sorted(pair_numbers)
    first_pair = pairs[0]
    last_pair = pairs[-1]

    windows = 0

    for pair in range(first_pair, last_pair + 1):
        if pair not in pair_numbers:
            windows += 1

    return windows


def get_clickhouse_client():
    return clickhouse_connect.get_client(
        host=CLICKHOUSE_HOST,
        port=CLICKHOUSE_PORT,
        username=CLICKHOUSE_USER,
        password=CLICKHOUSE_PASSWORD,
        database=CLICKHOUSE_DATABASE,
    )


def load_busy_data(client, request):
    """
    Загружает занятость преподавателя, группы/подгруппы и аудитории.
    """
    subgroup_name = (request.get("subgroup_name") or "").strip()

    sql = f"""
        SELECT
            entity_type,
            entity_id,
            lesson_date,
            pair_number,
            coalesce(group_name, '') AS group_name,
            coalesce(subgroup_name, '') AS subgroup_name
        FROM {CLICKHOUSE_DATABASE}.{CLICKHOUSE_TABLE}
        WHERE lesson_date BETWEEN %(start_date)s AND %(end_date)s
          AND pair_number IS NOT NULL
          AND (
                (
                    entity_type = %(teacher_type)s
                    AND entity_id = %(teacher_id)s
                )

             OR (
                    entity_type = %(group_type)s
                    AND entity_id = %(group_id)s
                    AND (
                           %(subgroup_name)s = ''
                        OR coalesce(subgroup_name, '') = ''
                        OR coalesce(subgroup_name, '') = %(subgroup_name)s
                        OR coalesce(group_name, '') = %(subgroup_name)s
                    )
                )

             OR (
                    entity_type = %(auditorium_type)s
                    AND entity_id = %(auditorium_id)s
                )
          )
        GROUP BY
            entity_type,
            entity_id,
            lesson_date,
            pair_number,
            group_name,
            subgroup_name
    """

    params = {
        "start_date": request["start_date"],
        "end_date": request["end_date"],
        "teacher_type": TEACHER_TYPE,
        "group_type": GROUP_TYPE,
        "auditorium_type": AUDITORIUM_TYPE,
        "teacher_id": int(request["teacher_id"]),
        "group_id": int(request["group_id"]),
        "auditorium_id": int(request["auditorium_id"]),
        "subgroup_name": subgroup_name,
    }

    result = client.query(sql, parameters=params)
    rows = result.result_rows

    print(f"Загружено строк занятости из ClickHouse: {len(rows)}")
    print(f"subgroup_name в запросе: {subgroup_name if subgroup_name else '<не задана>'}")

    busy_by_slot = defaultdict(set)
    group_pairs_by_day = defaultdict(set)
    debug_counts_by_type = defaultdict(int)

    for entity_type, entity_id, lesson_date, pair_number, group_name, row_subgroup_name in rows:
        day = lesson_date.isoformat()
        pair_number = int(pair_number)

        busy_by_slot[(day, pair_number)].add(entity_type)
        debug_counts_by_type[entity_type] += 1

        if entity_type == GROUP_TYPE:
            group_pairs_by_day[day].add(pair_number)

    debug = {
        "busy_rows_loaded": len(rows),
        "busy_rows_by_type": dict(debug_counts_by_type),
        "subgroup_name_used": subgroup_name if subgroup_name else None,
    }

    print("Диагностика загруженной занятости:")
    print(json.dumps(debug, ensure_ascii=False, indent=2))

    return busy_by_slot, group_pairs_by_day, debug


def find_slots(request, busy_by_slot, group_pairs_by_day):
    start_date = parse_date(request["start_date"])
    end_date = parse_date(request["end_date"])

    max_results = int(request.get("max_results", 5))
    candidates = []

    for current_date in date_range(start_date, end_date):
        # Воскресенье обычно не рассматриваем.
        if current_date.weekday() == 6:
            continue

        day = current_date.isoformat()

        for pair_number, pair_time in PAIR_TIMES.items():
            busy_entities = busy_by_slot.get((day, pair_number), set())

            teacher_is_busy = TEACHER_TYPE in busy_entities
            group_is_busy = GROUP_TYPE in busy_entities
            auditorium_is_busy = AUDITORIUM_TYPE in busy_entities

            if teacher_is_busy or group_is_busy or auditorium_is_busy:
                continue

            current_group_pairs = set(group_pairs_by_day.get(day, set()))
            new_group_pairs = set(current_group_pairs)
            new_group_pairs.add(pair_number)

            # Ограничение: не больше 4 занятий в день у группы/подгруппы.
            if len(new_group_pairs) > 4:
                continue

            windows_after = count_windows(new_group_pairs)

            # Ограничение: не больше одного окна.
            if windows_after > 1:
                continue

            score = (
                windows_after,
                len(new_group_pairs),
                current_date,
                pair_number,
            )

            candidates.append(
                {
                    "date": day,
                    "pair_number": pair_number,
                    "start_time": pair_time[0],
                    "end_time": pair_time[1],
                    "score": {
                        "windows_after": windows_after,
                        "group_lessons_after": len(new_group_pairs),
                    },
                    "_sort_score": score,
                }
            )

    candidates.sort(key=lambda item: item["_sort_score"])

    for item in candidates:
        item.pop("_sort_score", None)

    return candidates[:max_results]


def publish_response(channel, response, reply_to=None, correlation_id=None):
    """
    Если dashboard передал reply_to — отвечаем в персональную очередь.
    Если reply_to нет — отвечаем в общую очередь RESPONSE_QUEUE.
    """
    routing_key = reply_to or RESPONSE_QUEUE

    if not reply_to:
        channel.queue_declare(queue=RESPONSE_QUEUE, durable=True)

    channel.basic_publish(
        exchange="",
        routing_key=routing_key,
        body=json.dumps(response, ensure_ascii=False).encode("utf-8"),
        properties=pika.BasicProperties(
            delivery_mode=2,
            content_type="application/json",
            correlation_id=correlation_id,
        ),
    )


def handle_message(channel, method, properties, body):
    try:
        request = json.loads(body.decode("utf-8"))

        print(f"Получен запрос из {REQUEST_QUEUE}:")
        print(json.dumps(request, ensure_ascii=False, indent=2))

        client = get_clickhouse_client()

        busy_by_slot, group_pairs_by_day, debug = load_busy_data(
            client=client,
            request=request,
        )

        slots = find_slots(
            request=request,
            busy_by_slot=busy_by_slot,
            group_pairs_by_day=group_pairs_by_day,
        )

        response = {
            "request_id": request["request_id"],
            "status": "ok",
            "subject": request.get("subject"),
            "teacher_id": request["teacher_id"],
            "group_id": request["group_id"],
            "subgroup_name": request.get("subgroup_name"),
            "auditorium_id": request["auditorium_id"],
            "start_date": request["start_date"],
            "end_date": request["end_date"],
            "slots": slots,
            "debug": debug,
        }

        publish_response(
            channel=channel,
            response=response,
            reply_to=properties.reply_to,
            correlation_id=properties.correlation_id or request["request_id"],
        )

        # Ручной ack только после успешного расчёта и публикации ответа.
        channel.basic_ack(delivery_tag=method.delivery_tag)

        target_queue = properties.reply_to or RESPONSE_QUEUE
        print(f"Ответ отправлен в {target_queue}:")
        print(json.dumps(response, ensure_ascii=False, indent=2))

    except Exception as exc:
        print("Ошибка при обработке сообщения:")
        traceback.print_exc()

        error_response = {
            "request_id": None,
            "status": "error",
            "error": str(exc),
        }

        try:
            if body:
                request = json.loads(body.decode("utf-8"))
                error_response["request_id"] = request.get("request_id")

            publish_response(
                channel=channel,
                response=error_response,
                reply_to=properties.reply_to,
                correlation_id=properties.correlation_id,
            )

            # Ошибка обработана и отправлена в очередь ответа,
            # поэтому исходное сообщение подтверждаем, чтобы не зациклить плохой запрос.
            channel.basic_ack(delivery_tag=method.delivery_tag)

        except Exception:
            print("Не удалось отправить ответ с ошибкой. Возвращаю сообщение в очередь.")
            traceback.print_exc()

            channel.basic_nack(
                delivery_tag=method.delivery_tag,
                requeue=True,
            )


def main():
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=RABBITMQ_HOST,
            port=RABBITMQ_PORT,
            virtual_host=RABBITMQ_VHOST,
            credentials=credentials,
            heartbeat=60,
            blocked_connection_timeout=30,
        )
    )

    channel = connection.channel()

    channel.queue_declare(queue=REQUEST_QUEUE, durable=True)
    channel.queue_declare(queue=RESPONSE_QUEUE, durable=True)

    channel.basic_qos(prefetch_count=1)

    channel.basic_consume(
        queue=REQUEST_QUEUE,
        on_message_callback=handle_message,
        auto_ack=False,
    )

    print("Consumer запущен.")
    print(f"RabbitMQ: {RABBITMQ_HOST}:{RABBITMQ_PORT}")
    print(f"Очередь запросов: {REQUEST_QUEUE}")
    print(f"Очередь ответов: {RESPONSE_QUEUE}")
    print(f"ClickHouse: {CLICKHOUSE_HOST}:{CLICKHOUSE_PORT}")
    print(f"Таблица: {CLICKHOUSE_DATABASE}.{CLICKHOUSE_TABLE}")
    print("Жду сообщения...")

    channel.start_consuming()


if __name__ == "__main__":
    main()
