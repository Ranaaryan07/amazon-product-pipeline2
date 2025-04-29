# Real-Time Amazon Product Data Pipeline using Airflow,Docker, PySpark & BigQuery
    This project demonstrates a real-time data ingestion and transformation pipeline that simulates Amazon product data and loads it into Google BigQuery for analytics. The entire workflow is automated using Apache Airflow and runs in a Dockerized environment.

# Project Overview
    This pipeline performs the following steps:

    Generate fake Amazon product data in JSON format.
    Transform the JSON files to Parquet using PySpark.
    Upload the Parquet files to Google Cloud Storage (GCS).
    Load the data into Google BigQuery using Airflow’s GCSToBigQueryOperator.

# Tech Stack
    Apache Airflow (orchestration)
    Docker + docker-compose (local environment)
    PySpark (data transformation)
    Google Cloud Storage (data lake)
    Google BigQuery (data warehouse)
    Pyspark + Python (custom scripts & DAG logic)

# How to Run
    1. Start Airflow
        "docker-compose up" - run this command in terminal or vscode.
    2. Trigger the pipeline
        You can use the REST API (dagz/spark_api.py) to trigger all DAGs in sequence.
    3. DAGs Included
        "amazon-product-pipeline-dag" – Generates fake product data and uploads to output folder
        "transform-dag" – Converts JSON to Parquet and uploads to GCS
        "to_gcs_to_bigquery" – Loads Parquet file to BigQuery table

# Features
    End-to-end data engineering pipeline
    Real-world cloud integration with GCS & BigQuery
    Hands-on Airflow DAG development
    Clean and modular codebase

