# 🎵 Spotify Streaming Data Pipeline

> **Real-time music streaming analytics with Kafka, Airflow, DBT, and Snowflake**

[![Apache Kafka](https://img.shields.io/badge/Kafka-Event%20Streaming-231F20?style=flat-square&logo=apache-kafka)](https://kafka.apache.org/)
[![Apache Airflow](https://img.shields.io/badge/Airflow-Orchestration-017CEE?style=flat-square&logo=apache-airflow)](https://airflow.apache.org/)
[![DBT](https://img.shields.io/badge/DBT-Data%20Transformation-FF694B?style=flat-square&logo=dbt)](https://www.getdbt.com/)
[![Snowflake](https://img.shields.io/badge/Snowflake-Data%20Warehouse-29B5E8?style=flat-square&logo=snowflake)](https://www.snowflake.com/)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?style=flat-square&logo=docker)](https://www.docker.com/)

## 🎯 Overview

A **production-ready streaming analytics platform** simulating Spotify's real-time event processing infrastructure. Ingests user activity events (plays, skips, playlist adds) through Kafka, stores in MinIO data lake, loads to Snowflake, and transforms into actionable user engagement metrics using DBT.

### ✨ Key Features

- **⚡ Real-time Event Streaming** - Kafka for low-latency music event ingestion (1 event/second)
- **📊 User Engagement Analytics** - DAU, retention, skip rates, device usage
- **🏗️ Medallion Architecture** - Bronze (raw events) → Silver (cleansed) → Gold (aggregated KPIs)
- **🔄 Automated Orchestration** - Airflow DAGs for hourly batch processing
- **🛠️ DBT Transformations** - 7+ analytical models for music streaming insights
- **💾 Data Lake Storage** - MinIO (S3-compatible) with time-partitioned data
- **🐳 Fully Containerized** - Docker Compose for reproducible infrastructure

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────────────────┐
│               DATA GENERATION LAYER                          │
├──────────────────────────────────────────────────────────────┤
│  🎲 Event Simulator (Faker + Python)                        │
│  • 20 simulated users, 6 songs, 4 event types               │
│  • Event Types: play, pause, skip, add_to_playlist          │
│  • Devices: mobile, desktop, web                             │
│  • Countries: US, UK, CA, AU, IN, DE                         │
│  • UUID-based song & user identification                     │
└──────────────────────────────────────────────────────────────┘
                            ↓
                  🐍 Python Producer Script
                            ↓
┌──────────────────────────────────────────────────────────────┐
│               STREAMING INGESTION                            │
├──────────────────────────────────────────────────────────────┤
│  ⚡ Apache Kafka + Zookeeper                                 │
│  • Topic: spotify-events                                     │
│  • Producer: Publishes 1 event/second                        │
│  • Consumer: Batch processing (10 events/batch)              │
│  🖥️ Kafdrop UI - Real-time topic monitoring                │
└──────────────────────────────────────────────────────────────┘
                            ↓
                  🐍 Python Consumer Script
                            ↓
┌──────────────────────────────────────────────────────────────┐
│               DATA LAKE (BRONZE LAYER)                       │
├──────────────────────────────────────────────────────────────┤
│  💾 MinIO (S3-Compatible Object Storage)                    │
│  • Bucket: spotify-data-lake                                 │
│  • Path Structure: bronze/date=YYYY-MM-DD/hour=HH/           │
│  • Format: Newline-delimited JSON (NDJSON)                   │
│  • Batch uploads every 10 events                             │
└──────────────────────────────────────────────────────────────┘
                            ↓
┌──────────────────────────────────────────────────────────────┐
│               ORCHESTRATION LAYER                            │
├──────────────────────────────────────────────────────────────┤
│  🔄 Apache Airflow                                           │
│  • DAG: spotify_minio_to_snowflake_bronze                    │
│  • Schedule: @hourly                                         │
│  • Tasks:                                                    │
│    1. Extract: Read JSON files from MinIO                    │
│    2. Load: Bulk insert into Snowflake Bronze table          │
│  • PostgreSQL metadata database                              │
└──────────────────────────────────────────────────────────────┘
                            ↓
┌──────────────────────────────────────────────────────────────┐
│               DATA WAREHOUSE (SNOWFLAKE)                     │
├──────────────────────────────────────────────────────────────┤
│  ❄️ Bronze Layer (SPOTIFY_DB.BRONZE)                        │
│  • Table: spotify_events_bronze                              │
│  • Schema: event_id, user_id, song_id, artist_name,         │
│            song_name, event_type, device_type,               │
│            country, timestamp                                │
└──────────────────────────────────────────────────────────────┘
                            ↓
                    🛠️ DBT Transformations
                            ↓
┌──────────────────────────────────────────────────────────────┐
│               DBT TRANSFORMATION LAYER                       │
├─────────────────────────┬────────────────────────────────────┤
│  🥈 SILVER              │  • Data cleansing & validation     │
│                         │  • Timestamp parsing               │
│                         │  • Null filtering                  │
│                         │  • Model: spotify_silver           │
├─────────────────────────┼────────────────────────────────────┤
│  🥇 GOLD                │  • Business Metrics & KPIs         │
│                         │  1. daily_active_user.sql          │
│                         │  2. user_retention.sql             │
│                         │  3. top_songs.sql                  │
│                         │  4. skip_rate_by_song.sql          │
│                         │  5. device_usage.sql               │
│                         │  6. country_wise_engagement.sql    │
│                         │  7. user_engagement.sql            │
└─────────────────────────┴────────────────────────────────────┘
                            ↓
┌──────────────────────────────────────────────────────────────┐
│               ANALYTICS & INSIGHTS                           │
├──────────────────────────────────────────────────────────────┤
│  📊 Gold Layer Views (Ready for BI Tools)                   │
│  • User behavior patterns                                    │
│  • Content performance metrics                               │
│  • Geographic engagement analysis                            │
│  • Device & platform trends                                  │
└──────────────────────────────────────────────────────────────┘
```

## 🛠️ Technical Stack

### **Streaming & Messaging**
- **⚡ Apache Kafka** - Distributed event streaming platform
- **🐘 Zookeeper** - Kafka cluster coordination
- **🖥️ Kafdrop** - Web UI for Kafka monitoring
- **🐍 kafka-python** - Python client for producers/consumers

### **Storage & Orchestration**
- **💾 MinIO** - S3-compatible object storage (data lake)
- **🔄 Apache Airflow** - Workflow automation & scheduling
- **🐘 PostgreSQL** - Airflow metadata database

### **Data Warehouse & Transformation**
- **❄️ Snowflake** - Cloud data warehouse
- **🛠️ DBT (Data Build Tool)** - SQL-based transformations
- **📊 Medallion Architecture** - Bronze → Silver → Gold

### **Infrastructure**
- **🐳 Docker & Docker Compose** - Containerization
- **🐍 Python 3.8+** - Data generation & processing
- **🎭 Faker** - Realistic test data generation
- **🔐 python-dotenv** - Environment management

## 📊 Data Models (DBT)

### **Silver Layer** - Data Cleansing
```sql
-- silver.sql: Parse timestamps, filter nulls, basic validation
WITH bronze_data AS (
    SELECT
        event_id, user_id, song_id, artist_name, song_name,
        event_type, device_type, country,
        TRY_TO_TIMESTAMP_TZ(timestamp) AS event_ts
    FROM bronze.spotify_events_bronze
)
SELECT * FROM bronze_data
WHERE event_id IS NOT NULL
  AND user_id IS NOT NULL
  AND song_id IS NOT NULL
  AND event_ts IS NOT NULL
```

### **Gold Layer** - Business Metrics

**1. Daily Active Users (DAU)**
```sql
-- Track unique users per day
SELECT
    DATE_TRUNC('day', event_ts) AS day,
    COUNT(DISTINCT user_id) AS daily_active_users
FROM spotify_silver
GROUP BY day
```

**2. User Retention**
```sql
-- Measure user engagement frequency
SELECT
    user_id,
    COUNT(DISTINCT DATE_TRUNC('day', event_ts)) AS active_days,
    MIN(DATE(event_ts)) AS first_seen,
    MAX(DATE(event_ts)) AS last_seen
FROM spotify_silver
GROUP BY user_id
```

**3. Skip Rate by Song**
```sql
-- Identify songs with high skip rates
SELECT
    song_id, song_name, artist_name,
    COUNT(CASE WHEN event_type = 'play' THEN 1 END) AS total_plays,
    COUNT(CASE WHEN event_type = 'skip' THEN 1 END) AS total_skips,
    ROUND(total_skips * 1.0 / NULLIF(total_plays, 0), 2) AS skip_rate
FROM spotify_silver
GROUP BY song_id, song_name, artist_name
ORDER BY skip_rate DESC
```

**4. Device Usage Distribution**
```sql
-- Platform preference analysis
SELECT
    device_type,
    COUNT(*) AS total_events,
    COUNT(DISTINCT user_id) AS unique_users,
    ROUND(COUNT(*) * 1.0 / SUM(COUNT(*)) OVER (), 2) AS device_event_pct
FROM spotify_silver
GROUP BY device_type
```

**5. Country-wise Engagement**
```sql
-- Geographic activity patterns
SELECT
    country,
    DATE_TRUNC('day', event_ts) AS day,
    COUNT(CASE WHEN event_type = 'play' THEN 1 END) AS plays,
    COUNT(CASE WHEN event_type = 'skip' THEN 1 END) AS skips,
    COUNT(CASE WHEN event_type = 'add_to_playlist' THEN 1 END) AS playlist_adds
FROM spotify_silver
GROUP BY country, day
```

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.8+
- Snowflake account

### Setup

```bash
# 1. Clone repository
git clone https://github.com/Bayzid03/spotify-streaming-data-pipeline.git
cd spotify-streaming-data-pipeline

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Configure environment variables
cp .env.example .env
# Edit .env with your Snowflake credentials and MinIO settings

# 4. Start infrastructure
cd docker/
docker-compose up -d

# Access Points:
# - Kafdrop: http://localhost:9000
# - MinIO: http://localhost:9001 (admin/password123)
# - Airflow: http://localhost:8080 (admin/admin)

# 5. Start data generation
cd ../producer/
python producer.py  # Runs continuously

# 6. Start data ingestion (in new terminal)
cd ../consumer/
python kafka_to_minio.py  # Runs continuously

# 7. Setup DBT
cd ../dbt_models/
dbt init
dbt run  # Execute all transformations
```

### Verify Pipeline

```bash
# Check Kafka topic
docker exec -it kafka kafka-topics --list --bootstrap-server localhost:9092

# Verify MinIO storage
# Access http://localhost:9001 → Browse bucket

# Check Airflow DAG
# Access http://localhost:8080 → DAGs → spotify_minio_to_snowflake_bronze

# Query Snowflake
USE DATABASE SPOTIFY_DB;
USE SCHEMA BRONZE;
SELECT COUNT(*) FROM spotify_events_bronze;
```

## 📁 Project Structure

```
spotify-streaming-data-pipeline/
├── producer/
│   ├── producer.py                    # Kafka event generator
│   └── .env                          # Producer configuration
├── consumer/
│   ├── kafka_to_minio.py             # Kafka → MinIO consumer
│   └── .env                          # Consumer configuration
├── docker/
│   ├── docker-compose.yml            # Infrastructure definition
│   ├── dags/
│   │   └── minio_to_snowflake.py     # Airflow DAG
│   └── .env                          # Docker configuration
├── dbt_models/
│   ├── silver/
│   │   └── silver.sql                # Data cleansing
│   ├── gold/
│   │   ├── daily_active_user.sql     # DAU metric
│   │   ├── user_retention.sql        # Retention analysis
│   │   ├── top_songs.sql             # Popular songs
│   │   ├── skip_rate_by_song.sql     # Content quality
│   │   ├── device_usage.sql          # Platform trends
│   │   ├── country_wise_engagement.sql # Geographic insights
│   │   └── user_engagement.sql       # User behavior
│   └── source.yml                    # DBT source configuration
├── requirements.txt                   # Python dependencies
└── README.md
```

## 📈 Streaming Pipeline Workflow

1. **Event Generation** (Continuous)
   - Python producer simulates user events
   - Publishes to Kafka topic `spotify-events`
   - 1 event per second with realistic patterns

2. **Stream Processing** (Real-time)
   - Consumer reads from Kafka in batches of 10
   - Time-partitioned writes to MinIO (Bronze)
   - Path: `bronze/date=YYYY-MM-DD/hour=HH/`

3. **Batch Loading** (Hourly)
   - Airflow DAG extracts JSON files from MinIO
   - Bulk insert into Snowflake Bronze table
   - Idempotent operations for replay safety

4. **Data Transformation** (On-demand)
   - DBT runs Silver layer cleansing
   - Gold layer generates 7 analytical views
   - Version-controlled SQL transformations

## 🎯 Key Metrics & KPIs

### **User Engagement**
- **Daily Active Users (DAU)** - Unique users per day
- **User Retention** - Days active, cohort analysis
- **Session Patterns** - Play/pause/skip behavior

### **Content Performance**
- **Top Songs** - Most played tracks
- **Skip Rate** - Song quality indicator (plays vs skips)
- **Playlist Adds** - Content discovery metric

### **Platform Analytics**
- **Device Usage** - Mobile vs desktop vs web distribution
- **Country Engagement** - Geographic user activity
- **Event Volume** - Overall platform health

## 🌟 Advanced Features

### **Batch Processing Optimization**
- **10-event batching** in consumer for efficiency
- **Time-partitioned storage** (date/hour) in MinIO
- **Idempotent Airflow tasks** for safe re-runs

### **Data Quality**
- **Timestamp validation** with TRY_TO_TIMESTAMP_TZ
- **Null filtering** on critical fields
- **UUID-based identifiers** for data integrity

### **Scalability**
- **Horizontal scaling** - Add Kafka partitions & consumers
- **Storage efficiency** - NDJSON format with compression
- **Compute separation** - Snowflake warehouse scaling

### **Monitoring & Observability**
- **Kafdrop** - Real-time Kafka topic inspection
- **Airflow logs** - Task execution history
- **DBT docs** - Auto-generated data lineage

## 🎯 Real-world Use Cases

- **🎵 Music Streaming Platforms** - User behavior analytics (Spotify, Apple Music)
- **📺 Video Streaming** - Content recommendation engines (Netflix, YouTube)
- **🎮 Gaming Analytics** - Player engagement tracking
- **📱 Mobile Apps** - Feature usage and retention
- **🛒 E-commerce** - Real-time product interaction events

## 🚀 Future Enhancements

- [ ] **🤖 ML Integration** - Song recommendation models
- [ ] **📊 Power BI Dashboards** - Real-time visualization
- [ ] **⚡ Change Data Capture** - Incremental DBT models
- [ ] **🔔 Alerting** - Anomaly detection for skip rates
- [ ] **🌍 Multi-region** - Geographic data locality
- [ ] **📈 A/B Testing** - Feature experiment analytics

## 🤝 Contributing

Contributions welcome! Focus areas:
- **📊 Additional Metrics** - New analytical views
- **🔧 Performance Tuning** - Query optimization
- **🧪 Testing** - DBT tests & data quality checks
- **📱 Visualization** - Dashboard integration

## 📄 License

MIT License - See [LICENSE](LICENSE) for details.

---

**Real-time music streaming analytics at scale** 🎵⚡
