from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator


def python_test_func(task_number):
    print(f"task number is: {task_number}")


with DAG(
        dag_id='hw_s-merkulov_6',
        default_args={
            'depends_on_past': False,
            'email': ['merkulov.svttt@gmail.com'],
            'email_on_failure': True,
            'email_on_retry': True,
            'retries': 1,
            'retry_delay': timedelta(minutes=5)
        },
        description='DAG for Homework Task 6',
        schedule_interval=timedelta(days=1),
        start_date=datetime(2024, 4, 20),
        catchup=False,
        tags=['Task6'],
) as dag:
    for task_number in range(30):
        if task_number < 10:
            task = BashOperator(
                task_id='bash_' + str(task_number),
                bash_command="echo $NUMBER",
                env={"NUMBER": str(task_number)}
            )
        else:
            task = PythonOperator(
                task_id='python_task_' + str(task_number),
                python_callable=python_test_func,
                op_kwargs={'task_number': task_number},
            )
