# ==============================================================================
# AIRFLOW DAG TO RUN THE SPARK JOB FOR INVENTORY TRANSFORMATION
# ==============================================================================

# Import required libraries
from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from datetime import datetime

# Define default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 7, 3),
    'retries': 1,
}

# Instantiate the DAG
with DAG(
    dag_id='inventory_transformation_pipeline',
    default_args=default_args,
    description='A DAG to run the inventory transformation Spark job.',
    schedule_interval='@daily', # Run once every day
    catchup=False,
    tags=['retail', 'spark', 'inventory'],
) as dag:

    # Define the Spark Submit task in local mode
    # This task will run Spark job locally without cluster
    submit_spark_job = SparkSubmitOperator(
        task_id='submit_inventory_spark_job',
        application='/opt/bitnami/spark/jobs/transform_job.py', # Path inside the Spark container
        verbose=False,
        # This package is crucial to allow Spark to connect to PostgreSQL
        packages='org.postgresql:postgresql:42.2.18' 
    )