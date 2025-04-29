from airflow import DAG
# from airflow.sensors.external_task import ExternalTaskSensor
from airflow.operators.python import PythonOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from datetime import datetime, timedelta

import sys
# add the path where the transform script is located
sys.path.append('/opt/airflow/spark_jobs')

# Import the transform function
from transform_products import transform_data

# Default arguments for the DAG
default_args = {
    'owner' : 'aryan',
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

# Define the DAG
with DAG(
    dag_id='transform-amazon-product-data',
    default_args=default_args,
    description='Transform Amazon product data using Spark',
    start_date=datetime(2025, 4, 26),
    schedule_interval='@daily',
    catchup=False
) as dag:

    # Wait for the generate_large_dataset DAG to complete its task
    # wait_for_generation = ExternalTaskSensor(       # ExternalTaskSensor is a operator that waits for a task in another DAG to finish before starting the current task
    #     task_id='wait_for_generate_data',
    #     external_dag_id='amazon-product-pipeline', # the dag id of the generate_large_dataset dag
    #     external_task_id='create_fake_product_data', # the task id of the generate_large_dataset dag
    #     timeout=600, # the max time sensor will wait for external task to complete or it will raise an error.
    #     poke_interval=15, # frequency(in seconds) at which sensor will check the external task has completed.
    #     mode='poke' # poke mode means it will keep checking the status of the external task
    # )

    # Task to run the transfomation function
    transform_task = PythonOperator(
        task_id='transform_product_data',
        python_callable=transform_data # this will call the transform function from the transform_products.py file
    )

    trigger_load_dag =TriggerDagRunOperator(
        task_id='trigger_load_dag',
        trigger_dag_id='gcs_to_bigquery',
    )

    transform_task >> trigger_load_dag # task dependencies, which one runs first.
