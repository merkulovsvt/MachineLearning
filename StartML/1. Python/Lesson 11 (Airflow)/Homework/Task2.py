from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator


def test_func(ds, **kwargs):
    print(ds)


with DAG(
        dag_id='hw_s-merkulov_2',
        default_args={
            'depends_on_past': False,
            'email': ['merkulov.svttt@gmail.com'],
            'email_on_failure': True,
            'email_on_retry': True,
            'retries': 1,
            'retry_delay': timedelta(minutes=5)
        },
        description='DAG for Homework Task 2',
        schedule_interval=timedelta(days=1),
        start_date=datetime(2024, 4, 20),
        catchup=False,
        tags=['Task2'],
) as dag:
    t1 = BashOperator(
        task_id='bash_pwd',
        bash_command='pwd',
    )

    t2 = PythonOperator(
        task_id='print_ds_python',
        python_callable=test_func,
    )

    t1 >> t2
