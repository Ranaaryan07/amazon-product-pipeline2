from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.providers.google.cloud.hooks.gcs import GCSHook
import os

# Constants
BUCKET_NAME = 'amazon-products-bucket'
LOCAL_FOLDER_PATH = '/opt/airflow/transformed/otpt.parquet'
GCS_FOLDER = 'products'
BQ_PROJECT_DATASET = 'crucial-axon-458017-j5.product_dataset'
BQ_TABLE = 'refined_table'

default_args = {
    'start_date' : datetime(2024, 1, 1),
    'retries' : 1,
}

with DAG(
    dag_id='gcs_to_bigquery',
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
    tags=['gcs', 'bigquery', 'amazon-products']
) as dag:

    def upload_parquet_to_gcs():
        # Upload the local parquet file to GCS.
        gcs_hook = GCSHook(gcp_conn_id='google_cloud_default') # using GCP connection

        # List of parquet files from the directory
        parquet_files = [f for f in os.listdir(LOCAL_FOLDER_PATH) if f.endswith('.parquet')]
        if not parquet_files:
            raise FileNotFoundError("No parquet files found in the directory.")

        selected_file = parquet_files[0]  # Select the first file for upload
        local_file_path =os.path.join(LOCAL_FOLDER_PATH, selected_file)
        gcs_dest_path = f'{GCS_FOLDER}/{selected_file}'


        gcs_hook.upload(
            bucket_name=BUCKET_NAME,
            object_name=gcs_dest_path,
            filename=local_file_path
        )
        print(f"File {local_file_path} to gs://{BUCKET_NAME}/{gcs_dest_path}")

        # store for next task
        return gcs_dest_path

    upload_to_gcs =PythonOperator(
            task_id='upload_to_gcs',
            python_callable=upload_parquet_to_gcs
    )

    load_gcs_to_bq =GCSToBigQueryOperator(
            task_id='load_gcs_to_bigquery',
            bucket=BUCKET_NAME,
            source_objects=["products/*.parquet"],
            destination_project_dataset_table=f'{BQ_PROJECT_DATASET}.{BQ_TABLE}',
            source_format='PARQUET',
            autodetect=True,
            write_disposition='WRITE_TRUNCATE', # Overwrites existing table data
            gcp_conn_id='google_cloud_default'
    )

    upload_to_gcs >> load_gcs_to_bq