from datetime import datetime, timedelta
from textwrap import dedent

from airflow import DAG
from airflow.operators.bash import BashOperator


def python_test_func(task_number):
    print(f"task number is: {task_number}")


with DAG(
        dag_id='hw_s-merkulov_5',
        default_args={
            'depends_on_past': False,
            'email': ['merkulov.svttt@gmail.com'],
            'email_on_failure': True,
            'email_on_retry': True,
            'retries': 1,
            'retry_delay': timedelta(minutes=5)
        },
        description='DAG for Homework Task 5',
        schedule_interval=timedelta(days=1),
        start_date=datetime(2024, 4, 20),
        catchup=False,
        tags=['Task5'],
) as dag:
    templated_command = dedent(
        """
    {% for i in range(5) %}
        echo "{{ ts }}"
    {% endfor %}
    echo "{{ run_id }}"
    """
    )

    task = BashOperator(
        task_id='bash_task',
        bash_command=templated_command
    )
