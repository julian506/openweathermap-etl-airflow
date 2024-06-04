# Use the official Apache Airflow image
FROM apache/airflow:2.9.1

ENV AIRFLOW_HOME=/opt/airflow
WORKDIR ${AIRFLOW_HOME}

COPY requirements.txt ./

USER airflow

RUN pip install --no-cache-dir -r requirements.txt

# Switch to root user to install additional packages and set permissions
USER root

# Install necessary packages
RUN apt-get update && apt-get install -y \
    curl \
    apt-transport-https \
    gnupg \
    unixodbc \
    unixodbc-dev \
    && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql18 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*