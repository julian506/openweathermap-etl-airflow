
# OpenWeatherMap ETL with Airflow

This is a simple ETL built using Python, Airflow and an Azure SQL Database in order to practice basic knowledge for Data Engineers and Python Developers, by retrieving temperature data from the OpenWeatherMap [Current Weather API](https://openweathermap.org/current) for a given city.

This project was built during my internship at Globant.


## Features

- Recognition of the city that you want to extract the data from, using the OpenWeatherMap [Geocoding API](https://openweathermap.org/api/geocoding-api).
- Temperature data extraction from OpenWeatherMap [Current Weather API](https://openweathermap.org/current).
- Simple data transformation in order to convert the Kelvin degrees to Celsius degrees. **(More transformations are coming soon!)**
- Data loading to an [Azure SQL Database](https://azure.microsoft.com/es-es/products/azure-sql/database/) instance, always checking that the loaded data is new in order to avoid duplicated registers.
- Implementation of a DAG using Apache Airflow to orchestrate the ETL Pipeline, providing the container to run it.


## Requirements

You need to have installed the latest version of [Docker and Docker Compose](https://docs.docker.com/engine/install/) in order to run this project.

You'll also need an Azure SQL Database with a table with the next schema:

```sql
CREATE TABLE [dbo].[weather] (
    [uuid]         UNIQUEIDENTIFIER NOT NULL,
    [datetime]     DATETIME         NOT NULL,
    [consulted_at] DATETIME         NOT NULL,
    [temp]         REAL             NOT NULL,
    [temp_min]     REAL             NOT NULL,
    [temp_max]     REAL             NOT NULL,
    [feels_like]   REAL             NOT NULL,
    CONSTRAINT [PK_weather] PRIMARY KEY CLUSTERED ([uuid] ASC)
);
```


## Deployment

To deploy this project, follow the next steps:

First, you must setup the env variables by creating a `.env` file from the `.env.example` file and set the values as follows:
- `ZIP_CODE` is the zip code of the country of the city you want to retrieve the data from. (You can search it [here](https://worldpostalcode.com/))
-  `COUNTRY_CODE` is the [ISO 3166 Alpha-2 code](https://www.iso.org/obp/ui/#search) of the country of the city
- `API_BASE_URL` is the common URL for all the requests, having the default value of `https://api.openweathermap.org`. **Don't change it unless OpenWeatherMap changes the URLs for their APIs, what's unlikely to happen.**
- `API_KEY` is the key that OpenWeatherMap provides when you create an account on their website. You can get your API key [here](https://home.openweathermap.org/api_keys)
- `PIPELINE_EXECUTION_INTERVAL_IN_MINUTES` defines the interval in which the ETL will be executing. By default is set in five minutes but you can customize it as you want.
- `AZURE_ODBC_CONNECTION_STRING` is the connection string used to connect to the Azure SQL Database, you can find more information [here](https://learn.microsoft.com/en-us/azure/azure-sql/database/connect-query-content-reference-guide?view=azuresql#get-adonet-connection-information-optional---sql-database-only)
- `AZURE_TABLE_NAME` is the name of the table in Azure SQL Database where you want to store the transformed data.
- `POSTGRES_USER` and `POSTGRES_PASSWORD` are the definition of the credentials of the postgres container used as the Metadata DB for Airflow. Change them as you wish.
- `AIRFLOW_UID` **is an important variable to setup** because it setups the right folders permissions for the container. In your linux machine or WSL run the command `id -u` and set this variable to the value returned by the command. ([Reference](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html#setting-the-right-airflow-user))
- `_AIRFLOW_WWW_USER_USERNAME` and `_AIRFLOW_WWW_USER_PASSWORD` are the credentials of the user to login to the webserver in the `localhost:8080` URI. Change them as you wish.
- `AIRFLOW__CORE__FERNET_KEY` is the variable that is used in order to [encrypt passwords in the connection configuration and the variable configuration](https://airflow.apache.org/docs/apache-airflow/stable/security/secrets/fernet.html). You can generate your own Fernet key running the next command_ `python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"`

Then, you can run the docker container by using the next command:
```bash
  docker compose up
```

