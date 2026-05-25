import argparse
import json
import os
import uuid
from datetime import date, timedelta
from pathlib import Path

import pika


def load_env_file() -> None:
    """
    Локально подгружаем переменные из .env.
    Зависимость python-dotenv не нужна.
    """
    current_dir = Path(__file__).resolve().parent
    env_path = current_dir / ".env"

    if not env_path.exists():
        print(f".env не найден по пути: {env_path}")
        return

    print(f"Загружаю переменные окружения из файла: {env_path}")

    with env_path.open("r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            if "=" not in line:
                continue

            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")

            # Не перетираем переменные, если они уже заданы в системе
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


load_env_file()

RABBITMQ_HOST = required_env("RABBITMQ_HOST")
RABBITMQ_PORT = required_int_env("RABBITMQ_PORT")
RABBITMQ_USER = required_env("RABBITMQ_USER")
RABBITMQ_PASSWORD = required_env("RABBITMQ_PASSWORD")
RABBITMQ_VHOST = required_env("RABBITMQ_VHOST")

REQUEST_QUEUE = required_env("RABBITMQ_REQUEST_QUEUE")


def parse_args():
    today = date.today()

    parser = argparse.ArgumentParser(
        description="Отправка запроса на поиск времени переноса занятия в RabbitMQ"
    )

    parser.add_argument(
        "--teacher-id",
        type=int,
        required=True,
        help="ID преподавателя. Это entity_id из ClickHouse, где entity_type = 'person'",
    )

    parser.add_argument(
        "--group-id",
        type=int,
        required=True,
        help="ID группы. Это entity_id из ClickHouse, где entity_type = 'group'",
    )

    parser.add_argument(
        "--subgroup-name",
        type=str,
        default="",
        help="Название подгруппы. Если не указано, поиск идёт для всей группы.",
    )

    parser.add_argument(
        "--auditorium-id",
        type=int,
        required=True,
        help="ID аудитории. Это entity_id из ClickHouse, где entity_type = 'auditorium'",
    )

    parser.add_argument(
        "--subject",
        type=str,
        default="Технологии больших данных",
        help="Название дисциплины",
    )

    parser.add_argument(
        "--start-date",
        type=str,
        default=today.isoformat(),
        help="Дата начала поиска в формате YYYY-MM-DD",
    )

    parser.add_argument(
        "--end-date",
        type=str,
        default=(today + timedelta(days=7)).isoformat(),
        help="Дата конца поиска в формате YYYY-MM-DD",
    )

    parser.add_argument(
        "--max-results",
        type=int,
        default=5,
        help="Сколько подходящих слотов вернуть",
    )

    return parser.parse_args()


def build_message(args) -> dict:
    message = {
        "request_id": str(uuid.uuid4()),
        "teacher_id": args.teacher_id,
        "group_id": args.group_id,
        "auditorium_id": args.auditorium_id,
        "subject": args.subject,
        "start_date": args.start_date,
        "end_date": args.end_date,
        "max_results": args.max_results,
    }

    subgroup_name = args.subgroup_name.strip()

    if subgroup_name:
        message["subgroup_name"] = subgroup_name

    return message


def main():
    args = parse_args()
    message = build_message(args)

    credentials = pika.PlainCredentials(
        username=RABBITMQ_USER,
        password=RABBITMQ_PASSWORD,
    )

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

    channel.queue_declare(
        queue=REQUEST_QUEUE,
        durable=True,
    )

    channel.basic_publish(
        exchange="",
        routing_key=REQUEST_QUEUE,
        body=json.dumps(message, ensure_ascii=False).encode("utf-8"),
        properties=pika.BasicProperties(
            delivery_mode=2,
            content_type="application/json",
        ),
    )

    print(f"Сообщение отправлено в очередь {REQUEST_QUEUE}:")
    print(json.dumps(message, ensure_ascii=False, indent=2))

    connection.close()


if __name__ == "__main__":
    main()