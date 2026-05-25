import pendulum

from airflow.sdk import Asset, dag, task
from airflow.sdk.bases.hook import BaseHook


BRONZE_SCHEDULE_ASSET = Asset("hdfs://namenode:9000/user/airflow/schedule")

SILVER_BASE_PATH = "/user/airflow/silver/schedule"

CLICKHOUSE_CONN_ID = "clickhouse_http"

CLICKHOUSE_DB = "rasp_omgtu"
CLICKHOUSE_TABLE = "schedule_gold"


@dag(
    dag_id="lab3_dag",
    start_date=pendulum.datetime(2026, 3, 17, tz="UTC"),
    catchup=False,
    schedule=[BRONZE_SCHEDULE_ASSET],
    tags=["omgtu", "lab3", "spark", "clickhouse", "silver"],
)
def lab3_dag():

    @task(inlets=[BRONZE_SCHEDULE_ASSET])
    def resolve_bronze_input(*, inlet_events=None) -> dict:
        events = inlet_events[BRONZE_SCHEDULE_ASSET]
        last_event = events[-1]

        extra = last_event.extra or {}

        date_str = extra["date"]
        bronze_dir = extra["hdfs_dir"]

        # Эти даты приходят из ЛР2 через Asset Metadata.
        # Если их нет, используем date_str, чтобы DAG не падал на старых событиях.
        period_start = extra.get("period_start", date_str)
        period_end = extra.get("period_end", date_str)

        year = int(date_str[0:4])
        month = int(date_str[5:7])
        day = int(date_str[8:10])

        silver_day_path = (
            f"{SILVER_BASE_PATH}/"
            f"year={year}/month={month:02d}/day={day:02d}"
        )

        bronze_day_dir = f"hdfs://namenode:9000{bronze_dir}"

        print("[resolve_bronze_input] Получены данные из Asset Metadata")
        print(f"[resolve_bronze_input] date_str={date_str}")
        print(f"[resolve_bronze_input] period_start={period_start}")
        print(f"[resolve_bronze_input] period_end={period_end}")
        print(f"[resolve_bronze_input] bronze_dir={bronze_dir}")
        print(f"[resolve_bronze_input] bronze_day_dir={bronze_day_dir}")
        print(f"[resolve_bronze_input] silver_day_path={silver_day_path}")

        return {
            "date_str": date_str,
            "year": year,
            "month": month,
            "day": day,
            "period_start": period_start,
            "period_end": period_end,
            "bronze_dir": bronze_dir,
            "bronze_day_dir": bronze_day_dir,
            "silver_day_path": silver_day_path,
        }

    @task
    def bronze_to_silver(meta: dict) -> dict:
        date_str = meta["date_str"]
        period_start = meta.get("period_start", date_str)
        period_end = meta.get("period_end", date_str)

        bronze_day_dir = meta["bronze_day_dir"]
        silver_day_path = meta["silver_day_path"]

        print(f"[bronze_to_silver] date_str={date_str}")
        print(f"[bronze_to_silver] period_start={period_start}")
        print(f"[bronze_to_silver] period_end={period_end}")
        print(f"[bronze_to_silver] bronze_day_dir={bronze_day_dir}")
        print(f"[bronze_to_silver] silver_day_path={silver_day_path}")

        from pyspark.sql import SparkSession
        from pyspark.sql import functions as F
        from pyspark.sql.types import ArrayType, StructType

        spark = (
            SparkSession.builder
            .appName("lab3_bronze_to_silver")
            .master("local[*]")
            .getOrCreate()
        )

        spark.conf.set("spark.sql.ansi.enabled", "false")
        spark._jsc.hadoopConfiguration().set("fs.defaultFS", "hdfs://namenode:9000")

        raw = (
            spark.read
            .option("multiline", "true")
            .option("recursiveFileLookup", "true")
            .option("pathGlobFilter", "*.json")
            .json(bronze_day_dir)
            .withColumn("_source_path", F.input_file_name())
        )

        print("[bronze_to_silver] raw columns:", raw.columns)

        if "schedule" in raw.columns and isinstance(raw.schema["schedule"].dataType, ArrayType):
            tmp = raw.select(
                "_source_path",
                F.explode_outer(F.col("schedule")).alias("_item"),
            )

            if isinstance(tmp.schema["_item"].dataType, StructType):
                df = tmp.select("_source_path", F.col("_item.*"))
            else:
                df = (
                    tmp
                    .withColumn("raw_item", F.col("_item").cast("string"))
                    .drop("_item")
                )
        else:
            df = raw

        # Из нового HDFS-пути достаём универсальные признаки сущности:
        # type=person/id=...
        # type=group/id=...
        # type=auditorium/id=...
        df = (
            df
            .withColumn(
                "entity_type",
                F.regexp_extract(F.col("_source_path"), r"type=([^/]+)", 1)
            )
            .withColumn(
                "entity_id",
                F.regexp_extract(F.col("_source_path"), r"id=(\d+)", 1).cast("int")
            )
        )

        # Отбрасываем старые файлы формата teacher_id=..., если они вдруг остались в HDFS.
        df = df.filter(
            (F.col("entity_type") != "") &
            (F.col("entity_id").isNotNull())
        )

        def first_existing_str(column_names, alias):
            exprs = [F.col(c).cast("string") for c in column_names if c in df.columns]

            if exprs:
                return F.coalesce(*exprs).alias(alias)

            return F.lit(None).cast("string").alias(alias)

        def first_existing_int(column_names, alias):
            exprs = [F.col(c).cast("int") for c in column_names if c in df.columns]

            if exprs:
                return F.coalesce(*exprs).alias(alias)

            return F.lit(None).cast("int").alias(alias)

        date_candidates = [
            "date",
            "lessonDate",
            "dateLesson",
            "dayDate",
            "day",
        ]

        teacher_name_candidates = [
            "teacher",
            "teacherName",
            "lecturer",
            "fio",
            "fullName",
        ]

        lesson_type_candidates = [
            "lesson_type",
            "lessonType",
            "kindOfWork",
            "type",
        ]

        discipline_candidates = [
            "discipline",
            "subject",
            "name",
            "title",
        ]

        group_name_candidates = [
            "group",
            "groupName",
            "group_name",
        ]

        # Поддержка подгрупп.
        # Если API отдаёт поле подгруппы под другим названием, оно попадёт сюда через coalesce.
        subgroup_name_candidates = [
            "subgroup",
            "subGroup",
            "sub_group",
            "subgroupName",
            "subGroupName",
            "studentSubgroup",
            "student_subgroup",
            "part",
            "groupPart",
            "group_part",
        ]

        room_candidates = [
            "room",
            "auditorium",
            "auditorie",
            "aud",
        ]

        pair_number_candidates = [
            "pair_number",
            "pairNumber",
            "pair",
            "lessonNumber",
            "lessonNumberStart",
            "number",
        ]

        date_exprs = []

        for c in date_candidates:
            if c in df.columns:
                src = F.col(c).cast("string")
                src_dash = F.regexp_replace(src, r"\.", "-")

                date_exprs.append(F.to_date(src, "yyyy-MM-dd"))
                date_exprs.append(F.to_date(src, "yyyy.MM.dd"))
                date_exprs.append(F.to_date(src, "dd.MM.yyyy"))
                date_exprs.append(F.to_date(src_dash, "yyyy-MM-dd"))
                date_exprs.append(F.to_date(src_dash, "dd-MM-yyyy"))

        if date_exprs:
            lesson_date_col = F.coalesce(
                *date_exprs,
                F.lit(date_str).cast("date")
            ).alias("lesson_date")
        else:
            lesson_date_col = F.lit(date_str).cast("date").alias("lesson_date")

        cleaned = df.select(
            lesson_date_col,
            F.col("entity_type").cast("string").alias("entity_type"),
            F.col("entity_id").cast("int").alias("entity_id"),
            first_existing_str(teacher_name_candidates, "teacher_name"),
            first_existing_str(lesson_type_candidates, "lesson_type"),
            first_existing_str(discipline_candidates, "discipline"),
            first_existing_str(group_name_candidates, "group_name"),
            first_existing_str(subgroup_name_candidates, "subgroup_name"),
            first_existing_str(room_candidates, "room"),
            first_existing_int(pair_number_candidates, "pair_number"),
        ).withColumn(
            "load_date",
            F.lit(date_str).cast("date")
        )

        # Удаление дублей средствами PySpark.
        # Дубликаты возможны из-за повторяющихся записей в API или пересечения данных
        # преподавателя, группы и аудитории.
        cleaned = cleaned.dropDuplicates([
            "lesson_date",
            "entity_type",
            "entity_id",
            "teacher_name",
            "lesson_type",
            "discipline",
            "group_name",
            "subgroup_name",
            "room",
            "pair_number",
        ])

        print("[bronze_to_silver] cleaned schema:")
        cleaned.printSchema()

        print("[bronze_to_silver] cleaned preview:")
        cleaned.show(50, truncate=False)

        (
            cleaned.write
            .mode("overwrite")
            .parquet(f"hdfs://namenode:9000{silver_day_path}")
        )

        spark.stop()

        return {
            "date_str": date_str,
            "period_start": period_start,
            "period_end": period_end,
            "silver_day_path": silver_day_path,
        }

    @task
    def silver_to_clickhouse(meta: dict):
        date_str = meta["date_str"]
        period_start = meta.get("period_start", date_str)
        period_end = meta.get("period_end", date_str)

        silver_day_path = meta["silver_day_path"]

        conn = BaseHook.get_connection(CLICKHOUSE_CONN_ID)

        print(f"[silver_to_clickhouse] date_str={date_str}")
        print(f"[silver_to_clickhouse] period_start={period_start}")
        print(f"[silver_to_clickhouse] period_end={period_end}")
        print(f"[silver_to_clickhouse] silver_day_path={silver_day_path}")
        print(f"[silver_to_clickhouse] host={conn.host}")
        print(f"[silver_to_clickhouse] port={conn.port}")

        import clickhouse_connect

        client = clickhouse_connect.get_client(
            host=conn.host,
            port=conn.port,
            username=conn.login or "default",
            password=conn.password,
            interface=conn.schema or "http",
        )

        client.command(f"CREATE DATABASE IF NOT EXISTS {CLICKHOUSE_DB}")

        create_sql = f"""
        CREATE TABLE IF NOT EXISTS {CLICKHOUSE_DB}.{CLICKHOUSE_TABLE}
        (
            lesson_date Date,
            entity_type LowCardinality(String),
            entity_id UInt32,
            teacher_name Nullable(String),
            lesson_type Nullable(String),
            discipline Nullable(String),
            group_name Nullable(String),
            subgroup_name Nullable(String),
            room Nullable(String),
            pair_number Nullable(UInt8),
            load_date Date
        )
        ENGINE = MergeTree
        PARTITION BY toYYYYMM(lesson_date)
        ORDER BY (lesson_date, entity_type, entity_id)
        """

        # Идемпотентность:
        # при повторном запуске удаляем старые строки именно этого запуска.
        delete_sql = f"""
        ALTER TABLE {CLICKHOUSE_DB}.{CLICKHOUSE_TABLE}
        DELETE WHERE load_date = toDate('{date_str}')
        SETTINGS mutations_sync = 1
        """

        insert_sql = f"""
        INSERT INTO {CLICKHOUSE_DB}.{CLICKHOUSE_TABLE}
        SELECT
            lesson_date,
            entity_type,
            entity_id,
            teacher_name,
            lesson_type,
            discipline,
            group_name,
            subgroup_name,
            room,
            pair_number,
            load_date
        FROM hdfs(
            'hdfs://namenode:9000{silver_day_path}/*.parquet',
            'Parquet'
        )
        """

        print("[silver_to_clickhouse] CREATE TABLE ...")
        client.command(create_sql)

        print("[silver_to_clickhouse] DELETE old rows for load_date ...")
        client.command(delete_sql)

        print("[silver_to_clickhouse] INSERT parquet from HDFS ...")
        client.command(insert_sql)

        stats_sql = f"""
        SELECT
            count() AS rows_count,
            min(lesson_date) AS min_lesson_date,
            max(lesson_date) AS max_lesson_date
        FROM {CLICKHOUSE_DB}.{CLICKHOUSE_TABLE}
        WHERE load_date = toDate('{date_str}')
        """

        stats = client.query(stats_sql).result_rows[0]

        print("[silver_to_clickhouse] Проверка загруженных данных")
        print(f"[silver_to_clickhouse] rows_count={stats[0]}")
        print(f"[silver_to_clickhouse] min_lesson_date={stats[1]}")
        print(f"[silver_to_clickhouse] max_lesson_date={stats[2]}")
        print(f"[silver_to_clickhouse] expected_period_start={period_start}")
        print(f"[silver_to_clickhouse] expected_period_end={period_end}")

    meta = resolve_bronze_input()
    silver_meta = bronze_to_silver(meta)
    silver_to_clickhouse(silver_meta)


lab3_dag()