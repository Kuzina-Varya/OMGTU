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

    @task(task_id="prepare_teacher_name_paths")
    def prepare_teacher_name_paths(**context) -> list[str]:
        names_str = context["params"]["teacher_names"]
        names = [x.strip() for x in names_str.split(",") if x.strip() != ""]

        run_dt = context["logical_date"]

        hook = WebHDFSHook(webhdfs_conn_id="webhdfs")
        client = hook.get_conn()

        result_paths = []

        for i, name in enumerate(names, start=1):
            hdfs_path = (
            f"/user/airflow/teacher_name_requests/"
            f"year={run_dt.year}/month={run_dt.month:02d}/day={run_dt.day:02d}/"
            f"idx={i:02d}/name.json"
            )

            client.makedirs(os.path.dirname(hdfs_path))

            payload = json.dumps({"name": name}, ensure_ascii=False, indent=2).encode("utf-8")
            client.write(hdfs_path, payload, overwrite=True)

            result_paths.append(hdfs_path)

        return result_paths

    @task(task_id="find_teacher_id")
    def find_teacher_id(name_path: str, **context) -> str:
        hook = WebHDFSHook(webhdfs_conn_id="webhdfs")
        client = hook.get_conn()

        with client.read(name_path) as r:
            data = json.loads(r.read().decode("utf-8"))

        name = data["name"]

        r = requests.get(
        f"https://rasp.omgtu.ru/api/search?term={name}&type=person",
        timeout=30,
        )
        r.raise_for_status()
        api_data = r.json()

        if not api_data:
            result_obj = {"name": name, "teacher_id": None}
        else:
            result_obj = {"name": name, "teacher_id": int(api_data[0]["id"])}

        run_dt = context["logical_date"]
        idx_part = [part for part in name_path.split("/") if part.startswith("idx=")][0]

        result_path = (
        f"/user/airflow/teacher_id_results/"
        f"year={run_dt.year}/month={run_dt.month:02d}/day={run_dt.day:02d}/"
        f"{idx_part}/teacher.json"
        )

        client.makedirs(os.path.dirname(result_path))

        payload = json.dumps(result_obj, ensure_ascii=False, indent=2).encode("utf-8")
        client.write(result_path, payload, overwrite=True)

        return result_path

    @task(task_id="get_teachers")
    def get_teachers(result_paths: list[str], **context) -> str:
        teacher_ids: list[int] = []
        skipped: list[str] = []

        hook = WebHDFSHook(webhdfs_conn_id="webhdfs")
        client = hook.get_conn()

        for result_path in result_paths:
            with client.read(result_path) as r:
                item = json.loads(r.read().decode("utf-8"))

            if item["teacher_id"] is None:
                skipped.append(item["name"])
            else:
                teacher_ids.append(int(item["teacher_id"]))

        payload_obj = {"teacher_ids": teacher_ids, "skipped": skipped}

        run_dt = context["logical_date"]
        hdfs_path = (
        f"/user/airflow/teacher_ids/"
        f"year={run_dt.year}/month={run_dt.month:02d}/day={run_dt.day:02d}/"
        f"teachers.json"
        )

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
    name_paths = prepare_teacher_name_paths()
    teacher_result_paths = find_teacher_id.expand(name_path=name_paths)
    teachers_file = get_teachers(teacher_result_paths)

    start >> name_paths >> teacher_result_paths >> teachers_file

    skipped_text = format_skipped(teachers_file)
    teacher_ids = extract_teacher_ids(teachers_file)
    mapped = process_teacher_schedule.expand(teacher_id=teacher_ids)

    skipped_text >> report_skipped
    report_skipped >> mapped >> end

lab2_dag()