from datetime import datetime, timedelta

from airflow import DAG
from airflow.models import Variable
from airflow.operators.python import PythonOperator


def db_func(**kwargs):
    print(Variable.get('is_startml'))


with DAG(
        dag_id='hw_s-merkulov_12',
        default_args={
            'depends_on_past': False,
            'email': ['merkulov.svttt@gmail.com'],
            'email_on_failure': True,
            'email_on_retry': True,
            'retries': 1,
            'retry_delay': timedelta(minutes=5)
        },
        description='DAG for Homework Task 12',
        schedule_interval=timedelta(days=1),
        start_date=datetime(2024, 4, 20),
        catchup=False,
        tags=['Task12'],
) as dag:
    task = PythonOperator(
        task_id='python_task',
        python_callable=db_func
    )
