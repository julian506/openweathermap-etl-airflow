from airflow import XComArg
from utils import env_variables, casts
from datetime import datetime, timedelta
from scripts import extract, transform, load
from airflow.decorators import dag

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

@dag(
    default_args=default_args,
    schedule_interval=timedelta(minutes=PIPELINE_EXECUTION_INTERVAL_IN_MINUTES),
    catchup=False,
)
def open_weather_map_dag() -> None:
    extracted_data: XComArg = extract.extractCurrentWeatherData()
    transformed_weather_data: XComArg = transform.transformExtractedData(extracted_data)
    load.upload_data(transformed_weather_data)
    
open_weather_map_dag()