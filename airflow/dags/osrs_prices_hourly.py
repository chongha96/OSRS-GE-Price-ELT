from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
from price_update import main
import os
import sys

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2026, 3, 10),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

#Orchestrates DAG to run every 5 minutes, extracting data from prices.runescape.wiki, 
#loading it into the dev tables, and transforming with dbt to a normalized star schema
with DAG(
    'rs_price_update',
    default_args=default_args,
    description='Automated RS Price Updates stored',
    schedule=timedelta(minutes=5),
    catchup=False
) as dag:

    update_task = PythonOperator(
        task_id='run_price_update',
        python_callable=main,
    )

    dbt_run_task = BashOperator(
        task_id='dbt_run',
        bash_command='cd /opt/airflow/rs-price-project && dbt run'
    )
    # Link the tasks
    update_task >> dbt_run_task
