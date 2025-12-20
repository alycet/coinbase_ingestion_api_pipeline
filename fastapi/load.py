import os
from google.cloud import bigquery
from google.api_core.exceptions import NotFound
import pandas as pd
import sqlite3

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv(
    "GOOGLE_APPLICATION_CREDENTIALS",
    "../secrets/key.json"
)

#def load_to_bigquery():
#    # Load from SQLite
#    conn = sqlite3.connect("database.db")
#    df = pd.read_sql_query("SELECT * FROM COINBASE", conn)
#    conn.close()

    # Load to BigQuery
#    client = bigquery.Client()
#    table_id = "crypto-data-pipeline-477720.coinbase_data.ticker"
#    client.load_table_from_dataframe(df, table_id).result()

#    return len(df)

def load_to_bigquery():
    # Get newest timestamp from biquery table

    client = bigquery.Client()
    table_id = "crypto-data-pipeline-477720.coinbase_data.ticker"

    try:
        query = f"""SELECT MAX(time) AS max_ts FROM `{table_id}`"""
        result = client.query(query).result()
        row = list(result)[0]
        last_loaded_ts = row.max_ts if row else None
    except NotFound:
        last_loaded_ts = None
    # Load only new rows from sqlite

    conn = sqlite3.connect("database.db")

    if last_loaded_ts is None:
        df = pd.read_sql_query("SELECT * FROM COINBASE", conn)
    else:
        df = pd.read_sql_query("SELECT * FROM COINBASE WHERE time > ?", conn, params = [last_loaded_ts])
    
    conn.close()

    if df.empty:
        print("No new rows to load")
    else:
        print("number of rows to add:", len(df))

    # Load to bigquery

    client.load_table_from_dataframe(df, table_id).result()
    return len(df)

if __name__ == "__main__":
    load_to_bigquery()



