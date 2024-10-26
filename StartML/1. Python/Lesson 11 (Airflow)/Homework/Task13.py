from datetime import datetime, timedelta

from airflow import DAG
from airflow.models import Variable
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import BranchPythonOperator, PythonOperator


def choose_model():
    variable = Variable.get('is_startml')
    if variable == "True":
        return 'startml_desc'
    elif variable == "False":
        return 'not_startml_desc'


def func1(**kwargs):
    print("StartML is a starter course for ambitious people")


def func2(**kwargs):
    print("Not a startML course, sorry")


with DAG(
        dag_id='hw_s-merkulov_13',
        default_args={
            'depends_on_past': False,
            'email': ['merkulov.svttt@gmail.com'],
            'email_on_failure': True,
            'email_on_retry': True,
            'retries': 1,
            'retry_delay': timedelta(minutes=5)
        },
        description='DAG for Homework Task 13',
        schedule_interval=timedelta(days=1),
        start_date=datetime(2024, 4, 20),
        catchup=False,
        tags=['Task13'],
) as dag:
    dummy1 = EmptyOperator(task_id='before_branching')

    task1 = BranchPythonOperator(
        task_id='determine_course',
        python_callable=choose_model
    )

    task2 = PythonOperator(
        task_id='startml_desc',
        python_callable=func1
    )

    task3 = PythonOperator(
        task_id='not_startml_desc',
        python_callable=func2
    )

    dummy2 = EmptyOperator(task_id='after_branching')

    dummy1 >> task1

    task1 >> [task2, task3]

    [task2, task3] >> dummy2
