import json
import os
import time
import uuid
from datetime import date, datetime, timedelta
from typing import Any

import clickhouse_connect
import pandas as pd
import pika
import plotly.express as px
import streamlit as st


st.set_page_config(
    page_title="DuckBoard | ОмГТУ",
    page_icon="🐥",
    layout="wide",
)

# =========================
# ENV
# =========================
CLICKHOUSE_HOST = os.getenv("CLICKHOUSE_HOST", "localhost")
CLICKHOUSE_PORT = int(os.getenv("CLICKHOUSE_PORT", "8124"))
CLICKHOUSE_USER = os.getenv("CLICKHOUSE_USER", "default")
CLICKHOUSE_PASSWORD = os.getenv("CLICKHOUSE_PASSWORD", "airflow")
CLICKHOUSE_DATABASE = os.getenv("CLICKHOUSE_DATABASE", "rasp_omgtu")
CLICKHOUSE_TABLE = os.getenv("CLICKHOUSE_TABLE", "schedule_gold")

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT", "5672"))
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "guest")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD", "guest")
RABBITMQ_VHOST = os.getenv("RABBITMQ_VHOST", "/")
RABBITMQ_REQUEST_QUEUE = os.getenv("RABBITMQ_REQUEST_QUEUE", "reschedule_requests")
RABBITMQ_RESPONSE_QUEUE = os.getenv("RABBITMQ_RESPONSE_QUEUE", "reschedule_responses")

REQUEST_TIMEOUT_SEC = int(os.getenv("REQUEST_TIMEOUT_SEC", "20"))
REQUEST_POLL_INTERVAL_SEC = int(os.getenv("REQUEST_POLL_INTERVAL_SEC", "2"))

PAIR_TIME_MAP = {
    1: ("08:00", "09:35"),
    2: ("09:45", "11:20"),
    3: ("11:40", "13:15"),
    4: ("13:25", "15:00"),
    5: ("15:10", "16:45"),
    6: ("16:55", "18:30"),
    7: ("18:40", "20:15"),
}


# =========================
# STATE
# =========================
if "pending_requests" not in st.session_state:
    st.session_state.pending_requests = {}

if "completed_requests" not in st.session_state:
    st.session_state.completed_requests = {}


# =========================
# THEME
# =========================
def apply_duck_theme():
    st.markdown(
        """
        <style>
        :root {
            --cream: #FFFDF6;
            --cream-2: #FFF8E6;
            --butter: #FFECA8;
            --butter-soft: #FFF5C9;
            --duck-yellow: #F7D95B;
            --duck-orange: #F3A64A;
            --sky: #DDF4FB;
            --sky-2: #BFE7F5;
            --mint: #DDEDB9;
            --mint-2: #EEF7D7;
            --white: #FFFFFF;
            --text: #4E554E;
            --muted: #7C8278;
            --border: rgba(205, 196, 154, 0.55);
            --shadow: 0 14px 34px rgba(190, 180, 132, 0.18);
        }

        html, body, [data-testid="stAppViewContainer"] {
            background:
                radial-gradient(circle at 8% 8%, #FFF0B6 0%, transparent 22%),
                radial-gradient(circle at 88% 4%, #DDF4FB 0%, transparent 20%),
                radial-gradient(circle at 75% 85%, #E8F3C7 0%, transparent 25%),
                linear-gradient(180deg, #FFFDF6 0%, #FDF9EE 52%, #F7FBF4 100%);
            color: var(--text);
            font-size: 26px;
        }

        [data-testid="stHeader"] {
            background: rgba(255, 253, 246, 0.86);
            backdrop-filter: blur(10px);
        }

        [data-testid="stSidebar"] {
            background:
                radial-gradient(circle at 20% 10%, #FFF0B6 0%, transparent 35%),
                linear-gradient(180deg, #FFF8E6 0%, #F2FAFD 50%, #F1F8DD 100%);
            border-right: 1px solid var(--border);
        }

        [data-testid="stSidebar"] * {
            font-size: 24px !important;
            line-height: 1.55 !important;
        }

        h1 {
            font-size: 46px !important;
            line-height: 1.18 !important;
            font-weight: 850 !important;
            color: var(--text);
        }

        h2 {
            font-size: 40px !important;
            line-height: 1.22 !important;
            font-weight: 850 !important;
            color: var(--text);
        }

        h3 {
            font-size: 36px !important;
            line-height: 1.25 !important;
            font-weight: 850 !important;
            color: var(--text);
        }

        h4 {
            font-size: 31px !important;
            line-height: 1.25 !important;
            font-weight: 850 !important;
            color: var(--text);
        }

        p, label, div, span {
            color: var(--text);
        }

        p, div, span {
            font-size: 25px;
            line-height: 1.55;
        }

        label,
        [data-testid="stWidgetLabel"] p {
            font-size: 25px !important;
            font-weight: 750 !important;
        }

        .duck-hero {
            position: relative;
            overflow: hidden;
            background:
                radial-gradient(circle at 15% 22%, rgba(255, 236, 168, 0.9) 0%, transparent 28%),
                radial-gradient(circle at 78% 25%, rgba(221, 244, 251, 0.95) 0%, transparent 30%),
                radial-gradient(circle at 82% 82%, rgba(221, 237, 185, 0.85) 0%, transparent 30%),
                linear-gradient(135deg, #FFF9E8 0%, #FFFFFF 42%, #EAF8FD 72%, #F3F8DD 100%);
            border: 1px solid var(--border);
            border-radius: 32px;
            padding: 34px 38px;
            margin-bottom: 24px;
            box-shadow: var(--shadow);
        }

        .duck-hero::before {
            content: "";
            position: absolute;
            width: 190px;
            height: 190px;
            right: -50px;
            top: -55px;
            background: rgba(255, 236, 168, 0.45);
            border-radius: 50%;
        }

        .duck-hero::after {
            content: "";
            position: absolute;
            width: 260px;
            height: 120px;
            left: -45px;
            bottom: -42px;
            background: rgba(191, 231, 245, 0.42);
            border-radius: 50%;
        }

        .duck-hero-inner {
            position: relative;
            z-index: 2;
        }

        .duck-family {
            display: flex;
            gap: 12px;
            align-items: center;
            margin-bottom: 16px;
        }

        .duckling {
            width: 56px;
            height: 56px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 32px;
            box-shadow: 0 8px 18px rgba(190, 180, 132, 0.16);
            border: 1px solid rgba(255,255,255,0.85);
        }

        .duckling.yellow {
            background: linear-gradient(145deg, #FFF1A8 0%, #F7D95B 100%);
        }

        .duckling.white {
            background: linear-gradient(145deg, #FFFFFF 0%, #F6FBFD 100%);
        }

        .duck-title {
            font-size: 48px;
            font-weight: 850;
            margin-bottom: 12px;
            letter-spacing: 0.2px;
            color: var(--text);
        }

        .duck-subtitle {
            font-size: 28px;
            line-height: 1.62;
            max-width: 1050px;
            color: var(--muted);
        }

        .duck-card {
            background:
                linear-gradient(180deg, rgba(255,255,255,0.92) 0%, rgba(255,248,230,0.94) 100%);
            border: 1px solid var(--border);
            border-radius: 24px;
            padding: 24px 26px;
            margin-bottom: 18px;
            box-shadow: 0 10px 24px rgba(190, 180, 132, 0.12);
        }

        .duck-section-title {
            font-size: 40px;
            font-weight: 850;
            color: var(--text);
            margin: 14px 0 18px 0;
        }

        .duck-note {
            font-size: 26px;
            line-height: 1.65;
            color: var(--muted);
        }

        .duck-empty {
            background: linear-gradient(135deg, #FFF9D9 0%, #FFFFFF 100%);
            border: 1px dashed rgba(243, 166, 74, 0.65);
            color: #796945;
            border-radius: 20px;
            padding: 20px 22px;
            font-size: 26px;
            box-shadow: 0 8px 20px rgba(190, 180, 132, 0.10);
        }

        .duck-status-wait {
            background: linear-gradient(135deg, #FFFFFF 0%, #F0FAFD 55%, #FFF8E2 100%);
            border: 1px solid var(--border);
            border-radius: 18px;
            padding: 18px 20px;
            margin-bottom: 14px;
            font-size: 26px;
            box-shadow: 0 8px 20px rgba(190, 180, 132, 0.10);
        }

        .duck-divider {
            height: 1px;
            background: linear-gradient(
                90deg,
                transparent 0%,
                rgba(247,217,91,0.7) 25%,
                rgba(191,231,245,0.8) 55%,
                rgba(221,237,185,0.8) 80%,
                transparent 100%
            );
            margin: 24px 0;
        }

        div[data-testid="stMetric"] {
            background:
                linear-gradient(145deg, #FFFFFF 0%, #FFF8E6 100%);
            border: 1px solid var(--border);
            border-radius: 22px;
            padding: 20px 22px;
            box-shadow: 0 8px 20px rgba(190, 180, 132, 0.12);
        }

        div[data-testid="stMetricLabel"] {
            color: var(--muted);
            font-size: 24px !important;
            font-weight: 750 !important;
        }

        div[data-testid="stMetricValue"] {
            color: var(--text);
            font-size: 48px !important;
            font-weight: 850 !important;
        }

        .stTabs [data-baseweb="tab-list"] {
            gap: 10px;
            padding: 8px;
            background: linear-gradient(90deg, #FFF8E2 0%, #EAF8FD 52%, #F0F8DC 100%);
            border-radius: 18px;
            border: 1px solid var(--border);
        }

        .stTabs [data-baseweb="tab"] {
            height: 60px;
            border-radius: 14px;
            padding: 0 28px;
            color: var(--text);
            font-size: 26px !important;
            font-weight: 800 !important;
        }

        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #FFECA8 0%, #DDEDB9 48%, #BFE7F5 100%);
            color: #4E554E !important;
            font-weight: 850 !important;
        }

        .stButton > button,
        .stFormSubmitButton > button,
        .stDownloadButton > button {
            background: linear-gradient(135deg, #FFECA8 0%, #F7D95B 52%, #DDEDB9 100%);
            color: #4E554E;
            border: 1px solid rgba(198, 187, 128, 0.8);
            border-radius: 16px;
            padding: 0.82rem 1.45rem;
            font-size: 26px !important;
            font-weight: 850;
            box-shadow: 0 8px 18px rgba(190, 180, 132, 0.18);
        }

        .stButton > button:hover,
        .stFormSubmitButton > button:hover,
        .stDownloadButton > button:hover {
            border-color: #F3A64A;
            box-shadow: 0 10px 22px rgba(190, 180, 132, 0.24);
            transform: translateY(-1px);
        }

        div[data-baseweb="select"] > div,
        div[data-baseweb="input"] > div,
        .stDateInput > div > div,
        .stNumberInput > div > div,
        .stTextInput > div > div {
            background: rgba(255, 255, 255, 0.92);
            border-radius: 15px !important;
            border: 1px solid rgba(205, 196, 154, 0.72) !important;
            box-shadow: 0 4px 12px rgba(190, 180, 132, 0.07);
            min-height: 64px !important;
            font-size: 25px !important;
        }

        textarea, input {
            color: var(--text) !important;
            font-size: 25px !important;
        }

        div[data-baseweb="select"] span {
            font-size: 25px !important;
        }

        [data-testid="stDataFrame"],
        [data-testid="stTable"] {
            background: #FFFFFF;
            border: 1px solid var(--border);
            border-radius: 20px;
            overflow: hidden;
            font-size: 24px !important;
            box-shadow: 0 8px 20px rgba(190, 180, 132, 0.08);
        }

        .stAlert {
            border-radius: 18px;
            font-size: 25px !important;
        }

        .stSlider label {
            font-size: 25px !important;
            font-weight: 750 !important;
        }

        [data-testid="stCaptionContainer"] {
            font-size: 23px !important;
        }

        code {
            font-size: 22px !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

def render_hero():
    st.markdown(
        """
        <div class="duck-hero">
            <div class="duck-hero-inner">
                <div class="duck-family">
                    <div class="duckling yellow">🤍</div>
                    <div class="duckling white">🐥</div>
                    <div class="duckling yellow">🌿</div>
                    <div class="duckling white">🫧</div>
                </div>
                <div class="duck-title">Расписание ОмГТУ</div>
                <div class="duck-subtitle">
                    Аналитика расписания, поиск свободных слотов и асинхронная обработка через RabbitMQ.
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================
# CLICKHOUSE
# =========================
@st.cache_resource
def get_clickhouse_client():
    return clickhouse_connect.get_client(
        host=CLICKHOUSE_HOST,
        port=CLICKHOUSE_PORT,
        username=CLICKHOUSE_USER,
        password=CLICKHOUSE_PASSWORD,
        database=CLICKHOUSE_DATABASE,
    )


def query_df(query: str, parameters: dict[str, Any] | None = None) -> pd.DataFrame:
    client = get_clickhouse_client()
    return client.query_df(query, parameters=parameters or {})


@st.cache_data(ttl=300, show_spinner=False)
def get_date_bounds() -> tuple[date, date]:
    sql = f"""
    SELECT
        min(lesson_date) AS min_date,
        max(lesson_date) AS max_date
    FROM {CLICKHOUSE_DATABASE}.{CLICKHOUSE_TABLE}
    """
    df = query_df(sql)
    if df.empty or pd.isna(df.loc[0, "min_date"]) or pd.isna(df.loc[0, "max_date"]):
        today = date.today()
        return today - timedelta(days=30), today
    return df.loc[0, "min_date"], df.loc[0, "max_date"]


@st.cache_data(ttl=300, show_spinner=False)
def get_summary_metrics(date_from: date, date_to: date) -> pd.DataFrame:
    sql = f"""
    SELECT
        uniqExactIf(entity_id, entity_type = 'person') AS teachers_count,
        uniqExactIf(entity_id, entity_type = 'group') AS groups_count,
        uniqExactIf(entity_id, entity_type = 'auditorium') AS auditoriums_count,
        count() AS rows_count
    FROM {CLICKHOUSE_DATABASE}.{CLICKHOUSE_TABLE}
    WHERE lesson_date BETWEEN toDate(%(date_from)s) AND toDate(%(date_to)s)
    """
    return query_df(sql, {"date_from": str(date_from), "date_to": str(date_to)})


@st.cache_data(ttl=300, show_spinner=False)
def get_top_teachers(date_from: date, date_to: date, top_n: int = 10) -> pd.DataFrame:
    sql = f"""
    SELECT
        teacher_name,
        entity_id AS teacher_id,
        count() AS lessons_count
    FROM {CLICKHOUSE_DATABASE}.{CLICKHOUSE_TABLE}
    WHERE entity_type = 'person'
      AND teacher_name IS NOT NULL
      AND teacher_name != ''
      AND lesson_date BETWEEN toDate(%(date_from)s) AND toDate(%(date_to)s)
    GROUP BY teacher_name, teacher_id
    ORDER BY lessons_count DESC, teacher_name ASC
    LIMIT %(top_n)s
    """
    return query_df(
        sql,
        {
            "date_from": str(date_from),
            "date_to": str(date_to),
            "top_n": top_n,
        },
    )


@st.cache_data(ttl=300, show_spinner=False)
def get_lesson_type_distribution(date_from: date, date_to: date) -> pd.DataFrame:
    sql = f"""
    SELECT
        ifNull(nullIf(lesson_type, ''), 'Не указано') AS lesson_type,
        count() AS lessons_count
    FROM {CLICKHOUSE_DATABASE}.{CLICKHOUSE_TABLE}
    WHERE lesson_date BETWEEN toDate(%(date_from)s) AND toDate(%(date_to)s)
    GROUP BY lesson_type
    ORDER BY lessons_count DESC
    """
    return query_df(sql, {"date_from": str(date_from), "date_to": str(date_to)})


@st.cache_data(ttl=300, show_spinner=False)
def get_teachers() -> pd.DataFrame:
    sql = f"""
    SELECT
        entity_id AS teacher_id,
        anyIf(teacher_name, teacher_name IS NOT NULL AND teacher_name != '') AS teacher_name
    FROM {CLICKHOUSE_DATABASE}.{CLICKHOUSE_TABLE}
    WHERE entity_type = 'person'
    GROUP BY entity_id
    HAVING teacher_name IS NOT NULL AND teacher_name != ''
    ORDER BY teacher_name ASC
    """
    return query_df(sql)


@st.cache_data(ttl=300, show_spinner=False)
def get_groups() -> pd.DataFrame:
    sql = f"""
    SELECT
        entity_id AS group_id,
        anyIf(group_name, group_name IS NOT NULL AND group_name != '') AS group_name
    FROM {CLICKHOUSE_DATABASE}.{CLICKHOUSE_TABLE}
    WHERE entity_type = 'group'
    GROUP BY entity_id
    ORDER BY group_name ASC, group_id ASC
    """
    df = query_df(sql)
    if "group_name" in df.columns:
        df["group_name"] = df["group_name"].fillna(df["group_id"].astype(str).map(lambda x: f"Группа {x}"))
    return df


@st.cache_data(ttl=300, show_spinner=False)
def get_auditoriums() -> pd.DataFrame:
    sql = f"""
    SELECT
        entity_id AS auditorium_id,
        anyIf(room, room IS NOT NULL AND room != '') AS room_name
    FROM {CLICKHOUSE_DATABASE}.{CLICKHOUSE_TABLE}
    WHERE entity_type = 'auditorium'
    GROUP BY entity_id
    ORDER BY room_name ASC, auditorium_id ASC
    """
    df = query_df(sql)
    if "room_name" in df.columns:
        df["room_name"] = df["room_name"].fillna(df["auditorium_id"].astype(str).map(lambda x: f"Аудитория {x}"))
    return df


@st.cache_data(ttl=300, show_spinner=False)
def get_subgroups_for_group(group_id: int) -> list[str]:
    sql = f"""
    SELECT DISTINCT subgroup_name
    FROM {CLICKHOUSE_DATABASE}.{CLICKHOUSE_TABLE}
    WHERE entity_type = 'group'
      AND entity_id = %(group_id)s
      AND subgroup_name IS NOT NULL
      AND subgroup_name != ''
    ORDER BY subgroup_name ASC
    """
    df = query_df(sql, {"group_id": group_id})
    if df.empty:
        return []
    return df["subgroup_name"].dropna().tolist()


@st.cache_data(ttl=300, show_spinner=False)
def get_subjects_for_pair(teacher_id: int, group_id: int) -> list[str]:
    sql = f"""
    SELECT discipline
    FROM {CLICKHOUSE_DATABASE}.{CLICKHOUSE_TABLE}
    WHERE discipline IS NOT NULL
      AND discipline != ''
      AND (
            (entity_type = 'person' AND entity_id = %(teacher_id)s)
         OR (entity_type = 'group'  AND entity_id = %(group_id)s)
      )
    GROUP BY discipline
    HAVING
        countIf(entity_type = 'person' AND entity_id = %(teacher_id)s) > 0
        AND
        countIf(entity_type = 'group' AND entity_id = %(group_id)s) > 0
    ORDER BY discipline ASC
    """
    df = query_df(sql, {"teacher_id": teacher_id, "group_id": group_id})
    if df.empty:
        fallback_sql = f"""
        SELECT DISTINCT discipline
        FROM {CLICKHOUSE_DATABASE}.{CLICKHOUSE_TABLE}
        WHERE entity_type = 'person'
          AND entity_id = %(teacher_id)s
          AND discipline IS NOT NULL
          AND discipline != ''
        ORDER BY discipline ASC
        """
        fallback_df = query_df(fallback_sql, {"teacher_id": teacher_id})
        if fallback_df.empty:
            return []
        return fallback_df["discipline"].dropna().tolist()

    return df["discipline"].dropna().tolist()


# =========================
# RABBITMQ
# =========================
def get_rabbitmq_connection() -> pika.BlockingConnection:
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
    params = pika.ConnectionParameters(
        host=RABBITMQ_HOST,
        port=RABBITMQ_PORT,
        virtual_host=RABBITMQ_VHOST,
        credentials=credentials,
        heartbeat=30,
        blocked_connection_timeout=30,
    )
    return pika.BlockingConnection(params)


def publish_reschedule_request(payload: dict[str, Any]) -> tuple[str, str]:
    request_id = payload["request_id"]
    reply_queue = f"reschedule_reply_{request_id}"

    connection = get_rabbitmq_connection()
    channel = connection.channel()

    channel.queue_declare(queue=RABBITMQ_REQUEST_QUEUE, durable=True)
    channel.queue_declare(queue=reply_queue, durable=False, exclusive=False, auto_delete=True)

    channel.basic_publish(
        exchange="",
        routing_key=RABBITMQ_REQUEST_QUEUE,
        body=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        properties=pika.BasicProperties(
            content_type="application/json",
            delivery_mode=2,
            reply_to=reply_queue,
            correlation_id=request_id,
        ),
    )

    connection.close()
    return request_id, reply_queue


def try_read_one_message(queue_name: str, request_id: str) -> dict[str, Any] | None:
    connection = get_rabbitmq_connection()
    channel = connection.channel()

    try:
        method_frame, properties, body = channel.basic_get(queue=queue_name, auto_ack=False)

        if not method_frame:
            connection.close()
            return None

        payload = json.loads(body.decode("utf-8"))

        same_request = False

        if properties and properties.correlation_id:
            same_request = properties.correlation_id == request_id
        else:
            same_request = payload.get("request_id") == request_id

        if same_request:
            channel.basic_ack(method_frame.delivery_tag)
            try:
                if queue_name.startswith("reschedule_reply_"):
                    channel.queue_delete(queue=queue_name)
            except Exception:
                pass
            connection.close()
            return payload

        channel.basic_nack(method_frame.delivery_tag, requeue=True)
        connection.close()
        return None

    except Exception:
        connection.close()
        return None


def try_read_reply(request_id: str, reply_queue: str) -> dict[str, Any] | None:
    # Сначала ищем ответ в персональной reply-queue.
    payload = try_read_one_message(reply_queue, request_id)
    if payload is not None:
        return payload

    # Fallback на общий reschedule_responses,
    # чтобы дашборд работал даже если consumer ещё не переделан на reply_to.
    payload = try_read_one_message(RABBITMQ_RESPONSE_QUEUE, request_id)
    return payload


# =========================
# HELPERS
# =========================
def safe_pair_time(pair_number: int | None) -> tuple[str, str]:
    if pair_number in PAIR_TIME_MAP:
        return PAIR_TIME_MAP[pair_number]
    return "", ""


def build_teacher_options(df: pd.DataFrame) -> tuple[list[str], dict[str, int]]:
    labels = []
    mapping = {}
    for _, row in df.iterrows():
        label = f"{row['teacher_name']} — ID {int(row['teacher_id'])}"
        labels.append(label)
        mapping[label] = int(row["teacher_id"])
    return labels, mapping


def build_group_options(df: pd.DataFrame) -> tuple[list[str], dict[str, int]]:
    labels = []
    mapping = {}
    for _, row in df.iterrows():
        group_name = row["group_name"] if pd.notna(row["group_name"]) else f"Группа {int(row['group_id'])}"
        label = f"{group_name} — ID {int(row['group_id'])}"
        labels.append(label)
        mapping[label] = int(row["group_id"])
    return labels, mapping


def build_auditorium_options(df: pd.DataFrame) -> tuple[list[str], dict[str, int]]:
    labels = []
    mapping = {}
    for _, row in df.iterrows():
        room_name = row["room_name"] if pd.notna(row["room_name"]) else f"Аудитория {int(row['auditorium_id'])}"
        label = f"{room_name} — ID {int(row['auditorium_id'])}"
        labels.append(label)
        mapping[label] = int(row["auditorium_id"])
    return labels, mapping


def format_slot_table(slots: list[dict[str, Any]]) -> pd.DataFrame:
    rows = []
    for slot in slots:
        start_time = slot.get("start_time")
        end_time = slot.get("end_time")

        if (not start_time or not end_time) and slot.get("pair_number") in PAIR_TIME_MAP:
            start_time, end_time = safe_pair_time(slot.get("pair_number"))

        score = slot.get("score", {}) or {}

        rows.append(
            {
                "Дата": slot.get("date", ""),
                "Пара": slot.get("pair_number", ""),
                "Начало": start_time or "",
                "Конец": end_time or "",
                "Окон после переноса": score.get("windows_after", ""),
                "Пар у группы после переноса": score.get("group_lessons_after", ""),
            }
        )

    return pd.DataFrame(rows)


# =========================
# ANALYTICS TAB
# =========================
def render_analytics_tab():
    st.markdown('<div class="duck-section-title">Аналитика расписания</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="duck-note">Ниже — сводные показатели и графики по данным из ClickHouse.</div>',
        unsafe_allow_html=True,
    )

    min_date, max_date = get_date_bounds()

    col_filter1, col_filter2 = st.columns([2, 1])
    with col_filter1:
        selected_range = st.date_input(
            "Период аналитики",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date,
        )

    with col_filter2:
        top_n = st.slider("Топ преподавателей", min_value=5, max_value=20, value=10, step=1)

    if isinstance(selected_range, tuple) and len(selected_range) == 2:
        date_from, date_to = selected_range
    else:
        date_from, date_to = min_date, max_date

    metrics_df = get_summary_metrics(date_from, date_to)
    top_teachers_df = get_top_teachers(date_from, date_to, top_n=top_n)
    lesson_type_df = get_lesson_type_distribution(date_from, date_to)

    if metrics_df.empty:
        st.markdown(
            '<div class="duck-empty">🫧 В таблице ClickHouse пока нет данных для аналитики.</div>',
            unsafe_allow_html=True,
        )
        return

    metrics = metrics_df.iloc[0]

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Преподаватели", int(metrics["teachers_count"]))
    c2.metric("Группы", int(metrics["groups_count"]))
    c3.metric("Аудитории", int(metrics["auditoriums_count"]))
    c4.metric("Всего записей", int(metrics["rows_count"]))

    st.markdown('<div class="duck-divider"></div>', unsafe_allow_html=True)

    left, right = st.columns(2)

    with left:
        st.markdown('<div class="duck-card">', unsafe_allow_html=True)
        st.markdown("#### Топ преподавателей по количеству пар")

        if top_teachers_df.empty:
            st.markdown(
                '<div class="duck-empty">За выбранный период нет данных по преподавателям.</div>',
                unsafe_allow_html=True,
            )
        else:
            top_teachers_df = top_teachers_df.copy()
            top_teachers_df["teacher_label"] = top_teachers_df["teacher_name"] + " — ID " + top_teachers_df["teacher_id"].astype(str)

            fig_bar = px.bar(
                top_teachers_df.sort_values("lessons_count", ascending=True),
                x="lessons_count",
                y="teacher_label",
                orientation="h",
                text="lessons_count",
                color="teacher_label",
                color_discrete_sequence=[
                    "#FFECA8",
                    "#DDEDB9",
                    "#BFE7F5",
                    "#FFF8E6",
                    "#F7D95B",
                    "#EAF8FD",
                    "#F3DFA0",
                    "#D6E9B5",
                    "#DDF4FB",
                    "#FFDCA7",
                ],
            )
            fig_bar.update_layout(
                height=520,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=10, r=10, t=20, b=20),
                xaxis_title="Количество пар",
                yaxis_title="Преподаватель",
                showlegend=False,
                font=dict(color="#4E554E", size=26),
                xaxis=dict(
                    title_font=dict(size=26),
                    tickfont=dict(size=23),
                ),
                yaxis=dict(
                    title_font=dict(size=26),
                    tickfont=dict(size=23),
                ),
            )
            st.plotly_chart(fig_bar, use_container_width=True)

        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown('<div class="duck-card">', unsafe_allow_html=True)
        st.markdown("#### Распределение по видам занятий")

        if lesson_type_df.empty:
            st.markdown(
                '<div class="duck-empty">За выбранный период нет данных по типам занятий.</div>',
                unsafe_allow_html=True,
            )
        else:
            fig_pie = px.pie(
                lesson_type_df,
                names="lesson_type",
                values="lessons_count",
                hole=0.42,
                color_discrete_sequence=[
                    "#FFECA8",
                    "#BFE7F5",
                    "#DDEDB9",
                    "#FFF8E6",
                    "#F7D95B",
                    "#FFDCA7",
                    "#EAF8FD",
                ],
            )
            fig_pie.update_layout(
                height=520,
                paper_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=10, r=10, t=20, b=20),
                legend_title_text="Тип занятия",
                font=dict(color="#4E554E", size=26),
                legend=dict(
                    font=dict(size=24),
                    title_font=dict(size=25),
                ),
            )
            fig_pie.update_traces(
                textfont_size=24,
            )
            st.plotly_chart(fig_pie, use_container_width=True)

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="duck-card">', unsafe_allow_html=True)
    st.markdown("#### Таблица: агрегаты по типам занятий")
    if not lesson_type_df.empty:
        table_df = lesson_type_df.rename(
            columns={
                "lesson_type": "Тип занятия",
                "lessons_count": "Количество",
            }
        )
        st.dataframe(table_df, use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)


# =========================
# ASYNC STATUS FRAGMENT
# =========================
@st.fragment(run_every="2s")
def render_requests_fragment():
    pending_requests = st.session_state.pending_requests
    completed_requests = st.session_state.completed_requests

    # Проверяем pending-запросы
    now_ts = time.time()
    for request_id, info in list(pending_requests.items()):
        reply = try_read_reply(request_id=request_id, reply_queue=info["reply_queue"])

        if reply is not None:
            info["status"] = "done"
            info["result"] = reply
            info["finished_at_ts"] = now_ts
            completed_requests[request_id] = info
            del pending_requests[request_id]
            continue

        if now_ts - info["submitted_at_ts"] > REQUEST_TIMEOUT_SEC:
            info["status"] = "timeout"
            info["result"] = {
                "request_id": request_id,
                "status": "timeout",
                "message": f"Не удалось получить ответ за {REQUEST_TIMEOUT_SEC} сек.",
                "slots": [],
            }
            info["finished_at_ts"] = now_ts
            completed_requests[request_id] = info
            del pending_requests[request_id]

    st.session_state.pending_requests = pending_requests
    st.session_state.completed_requests = completed_requests

    st.markdown('<div class="duck-section-title">Статус запросов</div>', unsafe_allow_html=True)

    if not pending_requests and not completed_requests:
        st.markdown(
            '<div class="duck-empty">🐥 Здесь будут появляться результаты поиска свободных слотов.</div>',
            unsafe_allow_html=True,
        )
        return

    if pending_requests:
        st.markdown("#### В обработке")
        for request_id, info in pending_requests.items():
            payload = info["payload"]
            st.markdown(
                f"""
                <div class="duck-status-wait">
                    🌿 Запрос <b>{request_id[:8]}</b> ожидает ответ.<br>
                    Преподаватель ID: <b>{payload["teacher_id"]}</b>,
                    группа ID: <b>{payload["group_id"]}</b>,
                    аудитория ID: <b>{payload["auditorium_id"]}</b>,
                    период: <b>{payload["start_date"]}</b> — <b>{payload["end_date"]}</b>
                </div>
                """,
                unsafe_allow_html=True,
            )

    if completed_requests:
        st.markdown("#### Готовые результаты")

        sort_items = sorted(
            completed_requests.items(),
            key=lambda x: x[1].get("finished_at_ts", 0),
            reverse=True,
        )

        for idx, (request_id, info) in enumerate(sort_items):
            payload = info["payload"]
            result = info["result"]
            title = (
                f"Результат {request_id[:8]} | "
                f"teacher={payload['teacher_id']}, group={payload['group_id']}, room={payload['auditorium_id']}"
            )

            with st.expander(title, expanded=(idx == 0)):
                st.write("**Исходный запрос:**")
                st.json(payload)

                status = result.get("status")

                if status == "ok":
                    slots = result.get("slots", [])
                    if slots:
                        st.success(f"Найдено слотов: {len(slots)}")
                        slots_df = format_slot_table(slots)
                        st.dataframe(slots_df, use_container_width=True, hide_index=True)
                    else:
                        st.warning("Подходящие свободные слоты не найдены.")
                elif status == "timeout":
                    st.warning(result.get("message", "Истекло время ожидания ответа."))
                else:
                    st.error(result.get("message", "Произошла ошибка при обработке запроса."))

        c1, _ = st.columns([1, 5])
        with c1:
            if st.button("Очистить историю"):
                st.session_state.completed_requests = {}
                st.rerun()


# =========================
# RESCHEDULE TAB
# =========================
def render_reschedule_tab():
    st.markdown('<div class="duck-section-title">Поиск свободного слота</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="duck-card">
            <div class="duck-note">
                Выберите преподавателя, группу, аудиторию и период поиска. 
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    teachers_df = get_teachers()
    groups_df = get_groups()
    auditoriums_df = get_auditoriums()

    if teachers_df.empty or groups_df.empty or auditoriums_df.empty:
        st.markdown(
            '<div class="duck-empty">Для формы не хватает данных в ClickHouse</div>',
            unsafe_allow_html=True,
        )
        return

    teacher_labels, teacher_map = build_teacher_options(teachers_df)
    group_labels, group_map = build_group_options(groups_df)
    auditorium_labels, auditorium_map = build_auditorium_options(auditoriums_df)

    with st.form("reschedule_form", clear_on_submit=False):
        teacher_label = st.selectbox("Преподаватель", teacher_labels)
        selected_teacher_id = teacher_map[teacher_label]

        group_label = st.selectbox("Группа", group_labels)
        selected_group_id = group_map[group_label]

        subgroup_list = get_subgroups_for_group(selected_group_id)
        subgroup_options = ["Вся группа"] + subgroup_list
        subgroup_choice = st.selectbox("Подгруппа", subgroup_options)

        subgroup_manual = st.text_input("Подгруппа вручную, если её нет в списке")

        auditorium_label = st.selectbox("Аудитория", auditorium_labels)
        selected_auditorium_id = auditorium_map[auditorium_label]

        min_date, max_date = get_date_bounds()
        default_from = min_date
        default_to = min(max_date, min_date + timedelta(days=6))

        period = st.date_input(
            "Период поиска",
            value=(default_from, default_to),
            min_value=min_date,
            max_value=max_date,
        )

        max_results = st.number_input(
            "Количество вариантов",
            min_value=1,
            max_value=20,
            value=5,
            step=1,
        )

        subject_candidates = get_subjects_for_pair(selected_teacher_id, selected_group_id)

        if subject_candidates:
            subject_from_list = st.selectbox("Дисциплина", subject_candidates)
        else:
            subject_from_list = ""

        subject_manual = st.text_input("Дисциплина вручную, если нужно")

        submitted = st.form_submit_button("Найти свободные слоты 🐥")

    if submitted:
        if not isinstance(period, tuple) or len(period) != 2:
            st.error("Нужно выбрать диапазон дат.")
            return

        start_date, end_date = period

        subgroup_name = ""
        if subgroup_manual.strip():
            subgroup_name = subgroup_manual.strip()
        elif subgroup_choice != "Вся группа":
            subgroup_name = subgroup_choice

        subject = subject_manual.strip() or subject_from_list.strip() or "Без названия дисциплины"

        request_id = str(uuid.uuid4())

        payload = {
            "request_id": request_id,
            "teacher_id": int(selected_teacher_id),
            "group_id": int(selected_group_id),
            "auditorium_id": int(selected_auditorium_id),
            "subject": subject,
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "max_results": int(max_results),
        }

        if subgroup_name:
            payload["subgroup_name"] = subgroup_name

        try:
            _, reply_queue = publish_reschedule_request(payload)
            st.session_state.pending_requests[request_id] = {
                "request_id": request_id,
                "reply_queue": reply_queue,
                "payload": payload,
                "submitted_at_ts": time.time(),
                "status": "pending",
            }
            st.success("Запрос отправлен в RabbitMQ.")
            st.rerun()
        except Exception as e:
            st.error(f"Не удалось отправить запрос в RabbitMQ: {e}")

    render_requests_fragment()


# =========================
# SIDEBAR
# =========================
def render_sidebar():
    st.sidebar.markdown("## 🐥 DuckBoard")
    st.sidebar.markdown(
        """
        Панель для:
        - аналитики расписания
        - поиска свободных слотов
        - асинхронной обработки через RabbitMQ
        """
    )

    st.sidebar.markdown("---")
    st.sidebar.caption("ClickHouse")
    st.sidebar.code(
        f"{CLICKHOUSE_HOST}:{CLICKHOUSE_PORT}\nDB: {CLICKHOUSE_DATABASE}",
        language="text",
    )

    st.sidebar.caption("RabbitMQ")
    st.sidebar.code(
        f"{RABBITMQ_HOST}:{RABBITMQ_PORT}\nQueue: {RABBITMQ_REQUEST_QUEUE}",
        language="text",
    )

    st.sidebar.markdown("---")
    


# =========================
# MAIN
# =========================
def main():
    apply_duck_theme()
    render_sidebar()
    render_hero()

    tab_analytics, tab_reschedule = st.tabs(["📊 Аналитика", "🗓️ Перенос занятия"])

    with tab_analytics:
        render_analytics_tab()

    with tab_reschedule:
        render_reschedule_tab()


if __name__ == "__main__":
    main()