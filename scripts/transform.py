import datetime
from typing import Any
from utils import logs
from logging import Logger

logger: Logger = logs.getLogger()


def extractTemperatureValues(data) -> dict[str, float]:
    try:
        return {**data["main"]}
    except:
        message = "There was an error trying to get the temperature values from the extracted data"
        logger.exception(message)
        raise Exception(message)


def kelvinToCelsius(temp: float) -> float:
    try:
        return round(temp - 273.15, 2)
    except:
        message = "There was an error trying to convert from Kelvin degrees to Celsius degrees"
        logger.exception(message)
        raise Exception(message)


def convertTemperatureValuesToCelsius(
    temperature_values: dict[str, float]
) -> dict[str, float]:
    try:
        celsius_temperature_values: dict[str, float] = {
            key: kelvinToCelsius(value)
            for key, value in temperature_values.items()
            if key.startswith("temp") or key == "feels_like"
        }
        return celsius_temperature_values
    except:
        message = "There was an error creating the celsius_temperature_values dictionary from the original Kelvin degrees values"
        logger.exception(message)
        raise Exception(message)


def extractUtcDatetime(extracted_data: dict[str, Any]) -> int:
    try:
        return extracted_data["dt"]
    except:
        message = "There was an error while extracting the UTC datetime from the extracted data"
        logger.exception(message)
        raise Exception(message)


def addTimestampToData(
    celsius_temperature_values: dict[str, float], data_utc_datetime: int
) -> dict[str, float | datetime.datetime]:
    try:
        data_with_timestamp: dict[str, float | datetime.datetime] = {
            **celsius_temperature_values
        }
        data_with_timestamp["consulted_at"] = datetime.datetime.now()
        data_with_timestamp["datetime"] = datetime.datetime.fromtimestamp(
            data_utc_datetime
        )
        return data_with_timestamp
    except:
        message = "There was an error trying to add the timestamps to the celsius_temperature_values"
        logger.exception(message)
        raise Exception(message)


def transformExtractedData(
    extracted_data: dict[str, Any],
) -> dict[str, float | datetime.datetime]:
    temperature_values: dict[str, float] = extractTemperatureValues(extracted_data)

    data_utc_datetime: int = extractUtcDatetime(extracted_data)

    celsius_temperature_values: dict[str, float] = convertTemperatureValuesToCelsius(
        temperature_values
    )

    transformed_temperature_values: dict[str, float | datetime.datetime] = (
        addTimestampToData(celsius_temperature_values, data_utc_datetime)
    )

    return transformed_temperature_values
