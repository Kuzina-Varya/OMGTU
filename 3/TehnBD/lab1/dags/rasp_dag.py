# https://rasp.omgtu.ru/api/schedule/person/1003026?start=2026.02.02&finish=2026.02.08&lng=1
# https://rasp.omgtu.ru/api/schedule/person/{teacher_id}?start={data_start}&finish={data_finish}&lng=1

# https://rasp.omgtu.ru/api/search?term={name}&type=person

from tracemalloc import start
from airflow.decorators import dag, task
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.empty import EmptyOperator
from airflow.utils.trigger_rule import TriggerRule
from datetime import datetime
from airflow.models import Param
import os
import requests
FILE_PATH = "../opt/airflow/dags/configs/start_process.conf"

@dag(
    dag_id='rasp_dag',
    start_date=datetime(2026, 2, 1),
    schedule=None,
    catchup=False,
    tags=['omgtu', 'schedule'],
    params={
        'name': Param('', description='Введите имя преподавателя'),
        'date_start': Param('', format='date', description='Введите дату начала'),
        'date_end': Param('', format='date', description='Введите дату конца')
    }
)


def rasp_dag():
    start = EmptyOperator(task_id='start')

    @task(task_id='create_file')
    def create_file():
        os.makedirs(os.path.dirname(FILE_PATH), exist_ok=True)
        open(FILE_PATH, "w").close()
        print(f"Файл создан: {FILE_PATH}")


    @task(task_id='check_file')
    def check_file():
        if os.path.exists(FILE_PATH):
            return "fetch_id"
        else:
            return "stop_dag"


    @task(task_id='fetch_id')
    def fetch_id(**context):
        name = context['params']['name']
        url = f"https://rasp.omgtu.ru/api/search?term={name}&type=person"
        response = requests.get(url)
        data = response.json()
        teacher_id = data[0]['id']
        context['ti'].xcom_push(key='teacher_id', value=teacher_id)
        return teacher_id

    stop_dag = EmptyOperator(task_id='stop_dag')

    @task(task_id='get_schedule')
    def get_schedule(**context):
        date_start = context['params']['date_start']
        date_end = context['params']['date_end']
        teacher_id = context['ti'].xcom_pull(key='teacher_id', task_ids='fetch_id')
        url = f"https://rasp.omgtu.ru/api/schedule/person/{teacher_id}?start={date_start}&finish={date_end}&lng=1"
        response = requests.get(url)
        schedule= response.json()
        if(len(schedule) == 0):
            print("На этой неделе пар у коллеги нет, можно отдыхать")
            return "stop_dag"
        else:
            for lesson in schedule:
                subject = lesson['discipline']
                print (subject + "\n")
            return len(schedule)


    fetch_id_task = fetch_id()
    start >> create_file() >> check_file() >> [fetch_id_task, stop_dag]
    fetch_id_task >> get_schedule() >> stop_dag
rasp_dag()
    