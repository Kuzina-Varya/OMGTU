from airflow.decorators import dag, task
from airflow.operators.empty import EmptyOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
from airflow.models import Param
import requests
import json
from airflow.providers.apache.hdfs.hooks.webhdfs import WebHDFSHook
import os

@dag(
    dag_id="lab2_dag",
    start_date=datetime(2026, 2, 1),
    schedule=None,
    catchup=False,
    tags=["omgtu", "schedule2"],
    params={
        "teacher_names": Param(
            default="",
            description="Введи фамилии через запятую: Иванов, Петров, Сидоров, Кузнецов, Смирнов",
        )
    },
)
def lab2_dag():
    start = EmptyOperator(task_id="start")

    @task(task_id="get_teachers")
    def get_teachers(**context) -> str:
        names_str = context["params"]["teacher_names"]
        names = [x.strip() for x in names_str.split(",") if x.strip()]

        teacher_ids: list[int] = []
        skipped: list[str] = []

        for name in names:
            r = requests.get(
                f"https://rasp.omgtu.ru/api/search?term={name}&type=person",
                timeout=30,
            )
            r.raise_for_status()
            data = r.json()

            if not data:
                skipped.append(name)
                continue
            teacher_ids.append(int(data[0]["id"]))

        payload_obj = {"teacher_ids": teacher_ids, "skipped": skipped}

        run_dt = context["logical_date"]
        hdfs_path = (
            f"/user/airflow/teacher_ids/"
            f"year={run_dt.year}/month={run_dt.month:02d}/day={run_dt.day:02d}/"
            f"teachers.json"
        )

        hook = WebHDFSHook(webhdfs_conn_id="webhdfs")
        client = hook.get_conn()

        client.makedirs(os.path.dirname(hdfs_path))

        payload = json.dumps(payload_obj, ensure_ascii=False, indent=2).encode("utf-8")
        client.write(hdfs_path, payload, overwrite=True)

        return hdfs_path

    @task(task_id="extract_teacher_ids")
    def extract_teacher_ids(hdfs_path: str) -> list[int]:
        hook = WebHDFSHook(webhdfs_conn_id="webhdfs")
        client = hook.get_conn()

        with client.read(hdfs_path) as r:
            data = r.read().decode("utf-8")
            teacher_ids = json.loads(data)["teacher_ids"]

        return teacher_ids

    @task(task_id="format_skipped")
    def format_skipped(hdfs_path: str) -> str:
        hook = WebHDFSHook(webhdfs_conn_id="webhdfs")
        client = hook.get_conn()

        with client.read(hdfs_path) as r:
            data = r.read().decode("utf-8")
            skipped = json.loads(data)["skipped"]

        if not skipped:
            return "Пропущенных нет"
        return ", ".join(skipped)

    report_skipped = BashOperator(
        task_id="report_skipped",
        bash_command="""
        echo "Пропущены (не найдены): {{ ti.xcom_pull(task_ids='format_skipped') }}"
        """,
    )

    @task(task_id="process_teacher_schedule")
    def process_teacher_schedule(teacher_id: int, **context) -> str:
        ld = context["logical_date"].date()
        week_start = ld - timedelta(days=ld.weekday())
        week_finish = week_start + timedelta(days=6)

        def fmt(d):
            return f"{d.year:04d}.{d.month:02d}.{d.day:02d}"

        r = requests.get(
            f"https://rasp.omgtu.ru/api/schedule/person/{teacher_id}?start={fmt(week_start)}&finish={fmt(week_finish)}&lng=1",
            timeout=30,
        )
        r.raise_for_status()
        schedule = r.json()

        hdfs_path = (
            f"/user/airflow/schedule/"
            f"year={ld.year}/month={ld.month:02d}/day={ld.day:02d}/"
            f"teacher_id={teacher_id}/schedule.json"
        )

        hook = WebHDFSHook(webhdfs_conn_id="webhdfs")
        client = hook.get_conn()

        client.makedirs(hdfs_path.rsplit("/", 1)[0])

        payload = json.dumps(schedule, ensure_ascii=False, indent=2).encode("utf-8")
        client.write(hdfs_path, payload, overwrite=True)

        return hdfs_path

    end = EmptyOperator(task_id="end")

    #  путь -> чтение -> mapping
    teachers_file = get_teachers()

    skipped_text = format_skipped(teachers_file)
    teacher_ids = extract_teacher_ids(teachers_file)

    mapped = process_teacher_schedule.expand(teacher_id=teacher_ids)

    start >> teachers_file
    skipped_text >> report_skipped
    report_skipped >> mapped >> end

lab2_dag()