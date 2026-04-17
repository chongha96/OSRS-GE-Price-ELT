FROM apache/airflow:3.2.0-python3.12

COPY --chown=airflow:root requirements.txt .

USER root

RUN apt-get update && \
    apt-get install -y --no-install-recommends libpq-dev gcc python3-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

#Setup permissions & directory
RUN mkdir -p /opt/airflow/rs-price-project && \
    chown -R airflow:root /opt/airflow/rs-price-project && \
    chmod -R 775 /opt/airflow/rs-price-project

USER airflow

ENV PATH="${PATH}:/home/airflow/.local/bin"
ENV PYTHONPATH="${PYTHONPATH}:/opt/airflow/scripts"
ENV DBT_PROFILES_DIR="/home/airflow/.dbt"
ENV DBT_LOG_PATH="/tmp/dbt_logs"
ENV DBT_TARGET_PATH="/tmp/dbt_target"

RUN pip install --no-cache-dir -r requirements.txt
