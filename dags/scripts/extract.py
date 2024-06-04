from typing import Any
from utils import env_variables, requests_handler, logs
from dotenv import load_dotenv

def getCoordinatesByZipCode(API_BASE_URL: str, API_KEY: str) -> dict[str, int]:
    ZIP_CODE: str = env_variables.readEnvVariable("ZIP_CODE")
    COUNTRY_CODE: str = env_variables.readEnvVariable("COUNTRY_CODE")

    request_url: str = (
        f"{API_BASE_URL}/geo/1.0/zip?zip={ZIP_CODE},{COUNTRY_CODE}&appid={API_KEY}"
    )
    data: dict[str, Any] = requests_handler.performRequest(request_url)

    logs.infoLog(f'Identified city: {data["name"]}')

    try:
        coordinates: dict[str, int] = {
            "latitude": data["lat"],
            "longitude": data["lon"],
        }
        return coordinates
    except:
        raise logs.exceptionLog(
            "Error trying to extract latitude and longitude according to the ZIP_CODE and the COUNTRY_CODE env variables"
        )


def extractCurrentWeatherData(ti) -> dict[str, Any]:
    load_dotenv()
    API_BASE_URL: str = env_variables.readEnvVariable("API_BASE_URL")
    API_KEY: str = env_variables.readEnvVariable("API_KEY")
    coordinates: dict[str, int] = getCoordinatesByZipCode(API_BASE_URL, API_KEY)
    LATITUDE: int = coordinates["latitude"]
    LONGITUDE: int = coordinates["longitude"]
    request_url: str = (
        f"{API_BASE_URL}/data/2.5/weather?lat={LATITUDE}&lon={LONGITUDE}&appid={API_KEY}"
    )
    current_weather_data: dict[str, Any] = requests_handler.performRequest(request_url)
    ti.xcom_push(key='current_weather_data', value=current_weather_data)
    return current_weather_data
