from datetime import datetime, timedelta

import psycopg2
from airflow import DAG
from airflow.hooks.base import BaseHook
from airflow.operators.python import PythonOperator


def db_func(**kwargs):
    creds = BaseHook.get_connection(conn_id='startml_feed')
    with psycopg2.connect(
            f"postgresql://{creds.login}:{creds.password}"
            f"@{creds.host}:{creds.port}/{creds.schema}"
    ) as conn:
        with conn.cursor() as cursor:
            cursor.execute('''
            SELECT user_id, COUNT(action) as like_count
            FROM feed_action
            WHERE action = 'like'
            GROUP BY user_id
            ORDER BY COUNT(action) DESC
            LIMIT 1
            ''')
            result = cursor.fetchall()
            return {'user_id': result[0][0], 'count': result[0][1]}


with DAG(
        dag_id='hw_s-merkulov_11',
        default_args={
            'depends_on_past': False,
            'email': ['merkulov.svttt@gmail.com'],
            'email_on_failure': True,
            'email_on_retry': True,
            'retries': 1,
            'retry_delay': timedelta(minutes=5)
        },
        description='DAG for Homework Task 11',
        schedule_interval=timedelta(days=1),
        start_date=datetime(2024, 4, 20),
        catchup=False,
        tags=['Task11'],
) as dag:
    task = PythonOperator(
        task_id='python_task',
        python_callable=db_func
    )
