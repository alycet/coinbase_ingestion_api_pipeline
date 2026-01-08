# Near–Real-Time Crypto Analytics Pipeline


## 📋 Table of Contents

- [Overview](https://github.com/alycet/coinbase_ingestion_api_pipeline?tab=readme-ov-file#-overview)
- [Architecture & Design Decisions](https://github.com/alycet/coinbase_ingestion_api_pipeline?tab=readme-ov-file#%EF%B8%8F-architecture--design-decisions)
- [Technologies](https://github.com/alycet/coinbase_ingestion_api_pipeline?tab=readme-ov-file#%EF%B8%8F-technologies)
- [Data Model & Layers](https://github.com/alycet/coinbase_ingestion_api_pipeline?tab=readme-ov-file#-data-model--layers)
- [Dashboard Snapshot](https://github.com/alycet/coinbase_ingestion_api_pipeline?tab=readme-ov-file#-dashboard-snapshot)
- [Getting Started](https://github.com/alycet/coinbase_ingestion_api_pipeline?tab=readme-ov-file#-getting-started)
- [Future Enhancements](https://github.com/alycet/coinbase_ingestion_api_pipeline?tab=readme-ov-file#-future-enhancements)

---

## 🚀 Overview

This project implements a **near–real-time data pipeline** that ingests live cryptocurrency market data from the **Coinbase WebSocket API**, processes it using a **hybrid streaming and batch architecture**, stores it in **Google BigQuery**, transforms it with **dbt**, and visualizes insights through **Power BI dashboards**.

### Project Features:

- **Continuous Streaming Ingestion**  
  A FastAPI application continuously streams live market data from the Coinbase WebSocket API at container startup. Incoming events are ingested via an API endpoint and persisted with minimal transformation to support near–real-time analytics.

- **API-Driven Batch Loading**  
  A dedicated FastAPI load endpoint batches newly ingested records and loads them into Google BigQuery, decoupling continuous ingestion from downstream processing.

- **Orchestrated Hybrid Processing**  
  Apache NiFi schedules and orchestrates batch loads and downstream transformations, enabling reliable coordination between streaming ingestion and batch analytics workflows.

- **Analytics Engineering–Focused Transformations**  
  dbt models transform raw data into clean staging tables and analytics-ready fact and dimension tables using batch and incremental processing.

- **Near–Real-Time Analytics & Visualization**  
    Power BI dashboards consume transformed datasets to provide near–real-time visibility into crypto price movements, trading volumes, and market trends

### Potential Use Cases:

- Real-time crypto price monitoring
- Trade volume and liquidity analysis
- Market trend analysis
- Analytics-ready datasets for downstream reporting

### Data Sources:

#### Coinbase WebSocket API

This pipeline consumes live cryptocurrency market data from the **Coinbase WebSocket API**, which provides real-time event-driven updates for active trading pairs.

The data includes:
- Trade executions (price, size, side)
- Market statistics (24h volume, high/low, best bid/ask)
- Timestamps and sequencing metadata for ordering and deduplication

WebSocket messages are streamed continuously and ingested into the raw (bronze) layer with minimal transformation to preserve source fidelity.

---

## 🏗️ Architecture & Design Decisions

![Architecture Diagram](https://github.com/alycet/coinbase_ingestion_api_pipeline/blob/main/Coinbase_Data_Ingestion_System_Architecture.jpg)

### Near–Real-Time Architecture
The pipeline is designed to deliver **near–real-time insights** by continuously streaming market data from the Coinbase WebSocket API while relying on batch and incremental processing for data correctness and reliability. This approach balances low-latency data availability with the operational stability required for analytics workloads.

### Hybrid Streaming and Batch Processing
A hybrid architecture was intentionally chosen to decouple ingestion from downstream processing:

- **Continuous streaming ingestion** via a FastAPI service ensures rapid capture of raw market events
- **Scheduled batch loading and incremental transformations** ensure data quality, deduplication, and consistency over time

This design supports late-arriving data, enables reliable backfills, and prevents downstream failures from interrupting ingestion.

### Analytics Engineering–First Modeling
Data transformations are implemented using dbt and follow analytics engineering best practices:

- Clear separation between raw, staging, and marts layers
- Staging models standardize and clean incoming data
- Fact and dimension tables support analytics and BI use cases
- Version-controlled and testable transformation logic

### Warehouse-Centric Processing
Google BigQuery serves as the central processing and storage layer, chosen for:

- Serverless scalability
- Cost-efficient batch and incremental analytics
- Native compatibility with dbt and BI tools

-----


## 🛠️ Technologies

- **Python & FastAPI** – Continuous streaming ingestion and batch load API endpoints  
- **Coinbase WebSocket API** – Live cryptocurrency market data  
- **SQLite** – Lightweight local storage for temporary streaming ingestion  
- **Google BigQuery** – Cloud data warehouse for raw and transformed data  
- **Apache NiFi** – Orchestration and scheduling of batch loads and dbt jobs  
- **dbt (Data Build Tool)** – Staging and marts transformations with incremental and batch modeling  
- **Power BI** – Analytics and visualization dashboards for near–real-time insights  
- **Docker** – Containerized services for ingestion, orchestration, and transformations

---

## 🧱 Data Model & Layers

The data warehouse follows a layered modeling approach inspired by the **modern analytics stack**.

### Raw Layer
- Stores raw, append-only streaming data from the Coinbase WebSocket API
- Minimal transformations applied
- Preserves source fidelity for debugging, replay, and auditing

### Staging Layer
- Cleans and standardizes raw data
- Applies light transformations such as:
  - Type casting
  - Renaming columns
  - Basic normalization
- Serves as the foundation for analytics models

### Marts Layer (Facts & Dimensions)
The marts layer contains analytics-ready datasets modeled using **star schema principles**.

#### Fact Tables
- Capture measurable business events (e.g., trades, price updates)
- Optimized for aggregation and analytical queries
- Designed to support time-based and volume-based analysis

#### Dimension Tables
- Provide descriptive context (e.g., products, trading pairs, timestamps)
- Enable flexible slicing and filtering in BI tools

This structure supports performant querying, clear business logic, and maintainable analytics over time.

![Data Model](https://github.com/alycet/coinbase_ingestion_api_pipeline/blob/main/Coinbase_Market_Dimensional_Model.jpeg)

---

### 📊 Dashboard Snapshot

![Dashboard Snapshot](https://github.com/alycet/coinbase_ingestion_api_pipeline/blob/main/Coinbase_Market_Pulse_Dashboard.jpg)

**Note**: This dashboard is based on test data collected during development and may not represent continuously ingested data. Aggregate values are provided for demonstration purposes only.

---


## 🔄 Getting Started


Follow these instructions to run the near–real-time crypto analytics pipeline locally using Docker.

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/yourusername/crypto-pipeline.git
cd crypto-pipeline
```
### 2️⃣ Start the Services
```bash
docker-compose up
```
This will start three containers:

FastAPI – Handles continuous ingestion from the Coinbase WebSocket API and batch load endpoints

Apache NiFi – Orchestrates batch loads and triggers dbt transformations

dbt – Runs staging and marts transformations for analytics-ready tables

### 3️⃣ How It Works

The FastAPI container automatically streams Coinbase market data into SQLite as soon as it starts

NiFi schedules batch loads from SQLite to BigQuery and triggers dbt models to transform the data

Power BI dashboards can query the transformed BigQuery tables for near–real-time analytics

---

## 🔮 Future Enhancements

- **Scalable Streaming Architecture**  
  Introduce a message broker (e.g., Kafka or Pub/Sub) between FastAPI and BigQuery to handle higher throughput and distributed ingestion.

- **Data Quality & Reliability Improvements**  
  - Implement Dead Letter Queues (DLQs) for malformed or failed events.  
  - Add schema validation and evolution support to handle changes from Coinbase.  
  - Monitor data freshness and completeness with automated alerts.

- **Performance Optimizations**  
  - Partition BigQuery tables and optimize incremental batch loads for faster queries.  
  - Parallelize ingestion and batch processing for larger data volumes.

- **Enhanced Observability**  
  - Track metrics such as ingestion rate, batch duration, and transformation success.  
  - Add logging dashboards and alerting for failed NiFi or dbt jobs.

---

