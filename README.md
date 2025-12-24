# Real-Time Crypto Analytics Pipeline

This project implements a real-time data pipeline that ingests live crypto marke data from the Coinbase WebSocket API, stores it in Google BigQuery, transforms it using dbt, and visualizes insights through Power BI dashboards.

## 🚀 Overview

- **Data Ingestion API**: Custom-built Python API that connects to the Coinbase WebSocket feed and streams real-time trade and order book data.
- **Data Warehouse**: Google BigQuery stores raw and transformed data for scalable querying and analysis.
- **Data Transformation**: dbt (data build tool) is used to model and transform raw data into analytics-ready tables.
- **Visualization**: Power BI dashboards provide real-time insights into market trends, volumes, and price movements.


