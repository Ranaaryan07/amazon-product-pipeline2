from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys

# Add the path where the scripts are located
sys.path.append('/opt/airflow/extract')  # Path for the generate script
sys.path.append('/opt/airflow/spark_jobs')  # Path for the transform script

# Import the functions
from generate_large_dataset import generate_data  # From the generate script
from transform_products import transform_data    # From the transform script

default_args = {
    'owner': 'aryan',
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

with DAG(
    dag_id='amazon-product-pipeline-and-transform',
    default_args=default_args,
    description='Generate fake Amazon product data and transform it using Spark',
    start_date=datetime(2025, 4, 22),
    schedule_interval='@daily',
    catchup=False
) as dag:

    # Task to generate the fake product data
    generate_task = PythonOperator(
        task_id='create_fake_product_data',
        python_callable=generate_data
    )

    # Task to perform the transformation on the generated data
    transform_task = PythonOperator(
        task_id='transform_product_data',
        python_callable=transform_data
    )

    # Set the task dependencies: Generate data first, then transform
    generate_task >> transform_task
