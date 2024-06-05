from airflow import DAG
from airflow.operators.python import PythonOperator
from utils import env_variables, casts
from datetime import datetime, timedelta
from scripts import extract, transform, load

PIPELINE_EXECUTION_INTERVAL_IN_MINUTES: int = casts.strToInt(env_variables.readEnvVariable('PIPELINE_EXECUTION_INTERVAL_IN_MINUTES'))

default_args = {
    "owner": "Julián Pachón Castrillón",
    "depends_on_past": False,
    "start_date": datetime(2024, 6, 4),
    'email': ['julianpachon506@gmail.com'],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(seconds=60),
}

with DAG(
    "openweathermap_dag",
    default_args=default_args,
    schedule_interval=timedelta(minutes=PIPELINE_EXECUTION_INTERVAL_IN_MINUTES),
    catchup=False,
) as dag:
    extract_current_weather_data = PythonOperator(
        task_id="extract_current_weather_data",
        python_callable=extract.extractCurrentWeatherData,
    )

    transform_extracted_data = PythonOperator(
        task_id="transfrom_extracted_data",
        python_callable=transform.transformExtractedData,
    )

    load_extracted_data = PythonOperator(
        task_id="load_extracted_data", python_callable=load.upload_data
    )

    extract_current_weather_data >> transform_extracted_data >> load_extracted_data
