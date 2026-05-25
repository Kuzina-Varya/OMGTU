from airflow.decorators import dag, task
from airflow.operators.empty import EmptyOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
from airflow.models import Param
import requests
import json
from airflow.providers.apache.hdfs.hooks.webhdfs import WebHDFSHook
import os

from airflow.sdk import Asset, Metadata

BRONZE_SCHEDULE_ASSET = Asset("hdfs://namenode:9000/user/airflow/schedule")

@dag(
    dag_id="lab2_dag",
    start_date=datetime(2026, 2, 1),
    schedule=None,
    catchup=False,
    tags=["omgtu", "schedule2","lab2"],
    params={
    "teacher_names": Param(
        default="",
        description="Фамилии преподавателей через запятую: Иванов, Петров, Сидоров",
    ),
    "group_ids": Param(
        default="",
        description="ID групп через запятую: 4, 5",
    ),
    "auditorium_ids": Param(
        default="",
        description="ID аудиторий через запятую: 254, 698",
    ),
    "schedule_start_date": Param(
        default="",
        description="Дата начала периода расписания в формате YYYY-MM-DD. Если пусто, берётся начало недели logical_date.",
    ),
    "schedule_end_date": Param(
        default="",
        description="Дата конца периода расписания в формате YYYY-MM-DD. Если пусто, берётся конец недели logical_date.",
    ),
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

    @task(task_id="get_targets")
    def get_targets(teachers_hdfs_path: str, **context) -> str:
        hook = WebHDFSHook(webhdfs_conn_id="webhdfs")
        client = hook.get_conn()

        with client.read(teachers_hdfs_path) as r:
            teachers_data = json.loads(r.read().decode("utf-8"))

        teacher_ids = teachers_data["teacher_ids"]

        group_ids_str = context["params"].get("group_ids", "")
        auditorium_ids_str = context["params"].get("auditorium_ids", "")

        group_ids = [
            int(x.strip())
            for x in group_ids_str.split(",")
            if x.strip() != ""
        ]

        auditorium_ids = [
            int(x.strip())
            for x in auditorium_ids_str.split(",")
            if x.strip() != ""
        ]

        targets = []

        for teacher_id in teacher_ids:
            targets.append({
                "type": "person",
                "id": int(teacher_id),
            })

        for group_id in group_ids:
            targets.append({
                "type": "group",
                "id": int(group_id),
            })

        for auditorium_id in auditorium_ids:
            targets.append({
                "type": "auditorium",
                "id": int(auditorium_id),
            })

        run_dt = context["logical_date"]

        hdfs_path = (
            f"/user/airflow/targets/"
            f"year={run_dt.year}/month={run_dt.month:02d}/day={run_dt.day:02d}/"
            f"targets.json"
        )

        client.makedirs(os.path.dirname(hdfs_path))

        payload = json.dumps(
            {
                "targets": targets,
                "source_teachers_file": teachers_hdfs_path,
            },
            ensure_ascii=False,
            indent=2
        ).encode("utf-8")

        client.write(hdfs_path, payload, overwrite=True)

        return hdfs_path


    @task(task_id="extract_targets")
    def extract_targets(hdfs_path: str) -> list[dict]:
        hook = WebHDFSHook(webhdfs_conn_id="webhdfs")
        client = hook.get_conn()

        with client.read(hdfs_path) as r:
            data = json.loads(r.read().decode("utf-8"))

        return data["targets"]

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

    @task(task_id="process_target_schedule")
    def process_target_schedule(target: dict, **context) -> str:
        target_type = target["type"]
        target_id = int(target["id"])

        ld = context["logical_date"].date()

        start_param = context["params"].get("schedule_start_date", "")
        end_param = context["params"].get("schedule_end_date", "")

        if start_param and end_param:
            week_start = datetime.strptime(start_param, "%Y-%m-%d").date()
            week_finish = datetime.strptime(end_param, "%Y-%m-%d").date()
        else:
            week_start = ld - timedelta(days=ld.weekday())
            week_finish = week_start + timedelta(days=6)

        def fmt(d):
            return f"{d.year:04d}.{d.month:02d}.{d.day:02d}"

        url = (
            f"https://rasp.omgtu.ru/api/schedule/"
            f"{target_type}/{target_id}"
            f"?start={fmt(week_start)}&finish={fmt(week_finish)}&lng=1"
        )

        print(f"[process_target_schedule] target_type={target_type}")
        print(f"[process_target_schedule] target_id={target_id}")
        print(f"[process_target_schedule] url={url}")

        r = requests.get(url, timeout=30)
        r.raise_for_status()
        schedule = r.json()

        hdfs_path = (
            f"/user/airflow/schedule/"
            f"year={ld.year}/month={ld.month:02d}/day={ld.day:02d}/"
            f"type={target_type}/id={target_id}/schedule.json"
        )

        hook = WebHDFSHook(webhdfs_conn_id="webhdfs")
        client = hook.get_conn()

        client.makedirs(hdfs_path.rsplit("/", 1)[0])

        payload = json.dumps(
            schedule,
            ensure_ascii=False,
            indent=2
        ).encode("utf-8")

        client.write(hdfs_path, payload, overwrite=True)

        return hdfs_path


    @task(task_id="publish_bronze_asset", outlets=[BRONZE_SCHEDULE_ASSET])
    def publish_bronze_asset(**context):
        ld = context["logical_date"].date()

        day_path = (
            f"/user/airflow/schedule/"
            f"year={ld.year}/month={ld.month:02d}/day={ld.day:02d}/"
        )

        start_param = context["params"].get("schedule_start_date", "")
        end_param = context["params"].get("schedule_end_date", "")

        if start_param and end_param:
            period_start = start_param
            period_end = end_param
        else:
            week_start = ld - timedelta(days=ld.weekday())
            week_finish = week_start + timedelta(days=6)
            period_start = week_start.isoformat()
            period_end = week_finish.isoformat()

        yield Metadata(
            BRONZE_SCHEDULE_ASSET,
            extra={
                "date": ld.isoformat(),
                "hdfs_dir": day_path,
                "period_start": period_start,
                "period_end": period_end,
            },
        )

    end = EmptyOperator(task_id="end")

    #  путь -> чтение -> mapping
    
    name_paths = prepare_teacher_name_paths()
    teacher_result_paths = find_teacher_id.expand(name_path=name_paths)
    teachers_file = get_teachers(teacher_result_paths)

    start >> name_paths >> teacher_result_paths >> teachers_file
##с отмашкой 3 дагу
    skipped_text = format_skipped(teachers_file)

    targets_file = get_targets(teachers_file)
    targets = extract_targets(targets_file)

    mapped = process_target_schedule.expand(target=targets)
    publish = publish_bronze_asset()

    skipped_text >> report_skipped
    report_skipped >> targets_file >> targets >> mapped >> publish >> end

lab2_dag()