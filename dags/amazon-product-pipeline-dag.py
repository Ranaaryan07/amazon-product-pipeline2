from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from datetime import datetime, timedelta

import sys # allows us to interact with python runtime environment
sys.path.append('/opt/airflow/extract') # adds the directory to python's search path
                                        # airflow will use this path to find and import the python script

from generate_large_dataset import generate_data    # this is the task that will run inside the dag

default_args = {
    'owner': 'aryan',
    'retries':1,
    'retry_delay': timedelta(minutes=1)
}

with DAG(
    dag_id='amazon-product-pipeline',
    default_args=default_args,
    description='Create fake Amazon product data and save as JSON',
    start_date=datetime(2025, 4, 25),
    schedule_interval='@daily',
    catchup=False
) as dag:

#  this is the task which is going to run when the task goes to python_callable it will call generate_data
#  which was imported earlier from the generate file
    generate_task = PythonOperator(
        task_id='create_fake_product_data',
        python_callable=generate_data
    )

    trigger_transform_dag = TriggerDagRunOperator(
        task_id='trigger_transform_dag',
        trigger_dag_id='transform-amazon-product-data',  # the second DAG
    )

    generate_task >> trigger_transform_dag # this is the task dependency, which one runs first.
