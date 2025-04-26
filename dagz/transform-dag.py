from airflow import DAG
from airflow.operators.python import PythonOperator
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
    start_date=datetime(2025, 4, 25),
    schedule_interval='@daily',
    catchup=False
) as dag:

    # Task to run the transfomation function
    transform_task = PythonOperator(
        task_id='transform_product_data',
        python_callable=transform_data # this will call the transform function from the transform_products.py file
    )

    transform_task 
