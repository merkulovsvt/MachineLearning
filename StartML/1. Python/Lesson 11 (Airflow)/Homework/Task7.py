from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator


def python_test_func(ts, run_id, **kwargs):
    print(kwargs['task_number'], ts, run_id)


with DAG(
        dag_id='hw_s-merkulov_7',
        default_args={
            'depends_on_past': False,
            'email': ['merkulov.svttt@gmail.com'],
            'email_on_failure': True,
            'email_on_retry': True,
            'retries': 1,
            'retry_delay': timedelta(minutes=5)
        },
        description='DAG for Homework Task 7',
        schedule_interval=timedelta(days=1),
        start_date=datetime(2024, 4, 20),
        catchup=False,
        tags=['Task7'],
) as dag:
    for task_number in range(30):
        if task_number < 10:
            task = BashOperator(
                task_id='bash_' + str(task_number),
                bash_command=f"echo {task_number}"
            )
        else:
            task = PythonOperator(
                task_id='python_task_' + str(task_number),
                python_callable=python_test_func,
                op_kwargs={'task_number': task_number},
            )
