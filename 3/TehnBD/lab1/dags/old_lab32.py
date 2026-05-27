import pendulum

from airflow.sdk import Asset, dag, task
from airflow.hooks.base import BaseHook


# ДОЛЖЕН БЫТЬ ТОЧНО ТАКОЙ ЖЕ, КАК ВО 2 ЛАБЕ
BRONZE_SCHEDULE_ASSET = Asset("hdfs://namenode:9000/user/airflow/old_lab23/schedule")

# Куда будем складывать parquet
SILVER_BASE_PATH = "/user/airflow/silver/schedule"

# Airflow Connection к ClickHouse
CLICKHOUSE_CONN_ID = "clickhouse_http"

# ClickHouse: БД и таблица
CLICKHOUSE_DB = "rasp_omgtu"
CLICKHOUSE_TABLE = "schedule_gold_old_lab3"


@dag(
    dag_id="old_lab32_dag",
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

        date_str = last_event.extra["date"]
        bronze_dir = last_event.extra["hdfs_dir"]

        year = int(date_str[0:4])
        month = int(date_str[5:7])
        day = int(date_str[8:10])

        silver_day_path = (
            f"{SILVER_BASE_PATH}/"
            f"year={year}/month={month:02d}/day={day:02d}"
        )

        bronze_day_dir = f"hdfs://namenode:9000{bronze_dir}"

        return {
        "date_str": date_str,
        "year": year,
        "month": month,
        "day": day,
        "bronze_dir": bronze_dir,
        "bronze_day_dir": bronze_day_dir,
        "silver_day_path": silver_day_path,
        }

    @task
    def bronze_to_silver(meta: dict) -> dict:
        date_str = meta["date_str"]
        bronze_day_dir = meta["bronze_day_dir"]
        silver_day_path = meta["silver_day_path"]

        print(f"[bronze_to_silver] date_str={date_str}")
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

        # Если внутри JSON есть массив schedule — разворачиваем его
        if "schedule" in raw.columns and isinstance(raw.schema["schedule"].dataType, ArrayType):
            tmp = raw.select(
                "_source_path",
                F.explode_outer(F.col("schedule")).alias("_item"),
            )
            if isinstance(tmp.schema["_item"].dataType, StructType):
                df = tmp.select("_source_path", F.col("_item.*"))
            else:
                df = tmp.withColumn("raw_item", F.col("_item").cast("string")).drop("_item")
        else:
            df = raw

        # teacher_id тащим из пути teacher_id=...
        df = df.withColumn(
            "teacher_id",
            F.regexp_extract(F.col("_source_path"), r"teacher_id=(\d+)", 1).cast("int")
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

        date_candidates = ["date", "lessonDate", "dateLesson", "dayDate", "day"]
        teacher_name_candidates = ["teacher", "teacherName", "lecturer", "fio", "fullName"]
        lesson_type_candidates = ["lesson_type", "lessonType", "kindOfWork", "type"]
        discipline_candidates = ["discipline", "subject", "name", "title"]
        group_name_candidates = ["group", "groupName", "group_name"]
        room_candidates = ["room", "auditorium", "auditorie", "aud"]
        pair_number_candidates = [
            "pair_number", "pairNumber", "pair",
            "lessonNumber", "lessonNumberStart", "number"
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
            lesson_date_col = F.coalesce(*date_exprs, F.lit(date_str).cast("date")).alias("lesson_date")
        else:
            lesson_date_col = F.lit(date_str).cast("date").alias("lesson_date")

        cleaned = df.select(
            lesson_date_col,
            F.col("teacher_id").cast("int").alias("teacher_id"),
            first_existing_str(teacher_name_candidates, "teacher_name"),
            first_existing_str(lesson_type_candidates, "lesson_type"),
            first_existing_str(discipline_candidates, "discipline"),
            first_existing_str(group_name_candidates, "group_name"),
            first_existing_str(room_candidates, "room"),
            first_existing_int(pair_number_candidates, "pair_number"),
        ).withColumn(
            "load_date", F.lit(date_str).cast("date")
        )

        cleaned.printSchema()
        cleaned.show(20, truncate=False)

        (
            cleaned.write
            .mode("overwrite")
            .parquet(f"hdfs://namenode:9000{silver_day_path}")
        )

        spark.stop()

        return {
            "date_str": date_str,
            "silver_day_path": silver_day_path,
        }

    @task
    def silver_to_clickhouse(meta: dict):
        """
        Создаёт таблицу при необходимости, чистит данные за день и грузит parquet из HDFS в ClickHouse.
        """
        date_str = meta["date_str"]
        silver_day_path = meta["silver_day_path"]

        conn = BaseHook.get_connection(CLICKHOUSE_CONN_ID)

        print(f"[silver_to_clickhouse] date_str={date_str}")
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
        teacher_id UInt32,
        teacher_name Nullable(String),
        lesson_type Nullable(String),
        discipline Nullable(String),
        group_name Nullable(String),
        room Nullable(String),
        pair_number Nullable(UInt8),
        load_date Date
    )
    ENGINE = MergeTree
    PARTITION BY lesson_date
    ORDER BY (lesson_date, teacher_id)
    """

        # Идемпотентность:
        # перед новой загрузкой удаляем старые данные за эту дату
        delete_sql = f"""
        ALTER TABLE {CLICKHOUSE_DB}.{CLICKHOUSE_TABLE}
        DELETE WHERE lesson_date = toDate('{date_str}')
        """

        # ClickHouse умеет читать HDFS через hdfs(...)
        # и поддерживает glob-шаблоны в пути.
        insert_sql = f"""
        INSERT INTO {CLICKHOUSE_DB}.{CLICKHOUSE_TABLE}
        SELECT
            lesson_date,
            teacher_id,
            teacher_name,
            lesson_type,
            discipline,
            group_name,
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

        print("[silver_to_clickhouse] DELETE old rows for date ...")
        client.command(delete_sql)

        print("[silver_to_clickhouse] INSERT parquet from HDFS ...")
        client.command(insert_sql)

    meta = resolve_bronze_input()
    silver_meta = bronze_to_silver(meta)
    silver_to_clickhouse(silver_meta)


lab3_dag()