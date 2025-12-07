import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:\\Users\\ADT\\Downloads\\crypto-data-pipeline-477720-7bc814b59dac.json"

from google.cloud import bigquery
import pandas as pd
import sqlite3

# Load from SQLite

conn = sqlite3.connect("database.db")
df = pd.read_sql_query("SELECT * FROM COINBASE", conn)


# Load to BigQuery

client = bigquery.Client()
table_id = "crypto-data-pipeline-477720.coinbase_data.ticker"
client.load_table_from_dataframe(df, table_id).result()