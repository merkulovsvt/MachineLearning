from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator


def func1(ti):
    ti.xcom_push(
        key='sample_xcom_key',
        value='xcom test'
    )


def func2(ti):
    pull_result = ti.xcom_pull(
        key='sample_xcom_key',
        task_ids='python_task_1'
    )
    print(pull_result)


with DAG(
        dag_id='hw_s-merkulov_9',
        default_args={
            'depends_on_past': False,
            'email': ['merkulov.svttt@gmail.com'],
            'email_on_failure': True,
            'email_on_retry': True,
            'retries': 1,
            'retry_delay': timedelta(minutes=5)
        },
        description='DAG for Homework Task 9',
        schedule_interval=timedelta(days=1),
        start_date=datetime(2024, 4, 20),
        catchup=False,
        tags=['Task9'],
) as dag:
    task1 = PythonOperator(
        task_id='python_task_1',
        python_callable=func1
    )

    task2 = PythonOperator(
        task_id='python_task_2',
        python_callable=func2
    )
    task1 >> task2
