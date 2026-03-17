# Real-Time Stock Streaming Pipeline

## Project Overview
This project demonstrates a full-lifecycle **Real-Time Data Engineering pipeline** built using Kafka, Apache Spark Structured Streaming, Docker, and AWS S3. It simulates a real-world scenario where live stock market data is continuously ingested, processed in near real time, and stored in cloud object storage for downstream analytics.

The goal was to build a scalable streaming architecture that can capture live events, process them as they arrive, and land curated output into a cloud data lake without relying on manual batch uploads.

## Architecture
**Flow:** Stock API / Python Producer -> Kafka Topic -> Spark Structured Streaming -> AWS S3


<img width="1536" height="1024" alt="Real_Time_stock_streaming" src="https://github.com/user-attachments/assets/c261fa58-bbab-4a0e-b3c3-25cbe0e5892c" />


**Technologies Used**
Language:Python
Streaming Platform:Apache Kafka
Processing Engine:Apache Spark Structured Streaming
Containerization:Docker, Docker Compose
Cloud Storage:AWS S3
Cloud CLI / Access:AWS CLI
Dependencies:Java, Hadoop AWS libraries



## 📂 Project Structure

├── scripts/
│   ├── stock_producer.py      # Python producer script to fetch/send stock data into Kafka
│   ├── stream_to_s3.py        # Spark Structured Streaming consumer that reads Kafka and writes to S3
├── docker-compose.yml         # Docker setup for Kafka/Zookeeper containers
├── requirements.txt           # Python dependencies
└── README.md
