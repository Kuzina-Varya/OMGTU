from airflow.decorators import dag, task
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator
from airflow.utils.trigger_rule import TriggerRule
from datetime import datetime
import random

@dag(
    dag_id='hype_dag_v3',
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=['respect', 'airflow3']
)
def generate_hype_dag():

    start = EmptyOperator(task_id='start')

    @task(task_id='fetch_data')
    def get_data_metric():
        v = random.randint(1, 10)
        print(f"Получено значение: {v}")
        return v

    @task.branch(task_id='check_quality_branch')
    def check_quality(metric: int):
        print(f"Проверка метрики: {metric}")
        if metric > 5:
            return 'train_model'
        else:
            return 'skip_processing'

    train_model = BashOperator(
        task_id='train_model',
        bash_command='echo "Метрика респект! Запускаю обучение" && sleep 2'
    )

    skip_processing = BashOperator(
        task_id='skip_processing',
        bash_command='echo "Метрика плохая"'
    )

    final = EmptyOperator(
        task_id='end',
        trigger_rule=TriggerRule.NONE_FAILED_MIN_ONE_SUCCESS
    )

    metric_value = get_data_metric()
    branch_result = check_quality(metric_value)

    start >> metric_value

    # зависимости
    branch_result >> [train_model, skip_processing] >> final

# инициализация
generate_hype_dag()