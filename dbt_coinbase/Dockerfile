FROM python:3.10-slim

WORKDIR /opt/dbt

RUN pip install --no-cache-dir dbt-bigquery

COPY . .

CMD ["sleep", "infinity"]