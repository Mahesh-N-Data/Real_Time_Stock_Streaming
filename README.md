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

## How It Works

### 1. Streaming Infrastructure Starts**
The pipeline begins by starting the local streaming infrastructure using **Docker Compose**.  
This brings up the required Kafka services so the project has a running message broker to handle live stock events.

### 2. Kafka Topic Acts as the Streaming Buffer**
A Kafka topic is created to hold incoming stock market events.  
This topic acts as the central buffer between the producer and the Spark consumer, allowing ingestion and processing to remain decoupled.

### 3. Stock Producer Sends Live Market Events**
The `stock_producer.py` script is then executed.  
This producer connects to a stock market API (or simulated source), fetches stock price data, and publishes each event into the Kafka topic in real time.

In simple terms:

- producer fetches stock data
- producer pushes messages into Kafka
- Kafka stores the messages temporarily until Spark reads them

### 4. Spark Structured Streaming Consumes Kafka Data**
Once the producer is sending data, the Spark streaming application is started using `spark-submit`.

The Spark job:
- connects to the Kafka topic
- continuously reads stock events as they arrive
- parses the incoming records
- applies the required schema
- performs transformations and aggregations on the stream

This is the real-time processing layer of the project.

### 5. Real-Time Aggregation Happens in Spark**
Inside the Spark pipeline, the incoming stock messages are processed in **micro-batches** using **Spark Structured Streaming**.  
Instead of waiting for a full batch file, Spark keeps consuming new Kafka records continuously and performs near real-time aggregation.

Examples of processing done here can include:
- grouping by stock symbol
- calculating average price
- counting events
- tracking min/max values
- preparing curated output for analytics

### 6. Processed Streaming Output is Written to Amazon S3**
After processing the stock stream, Spark writes the aggregated output into **Amazon S3**.  
S3 acts as the cloud storage layer for durable persistence, so the streaming results are no longer only in memory or Kafka—they are stored for downstream analytics.

This means the pipeline flow becomes:

`Producer -> Kafka -> Spark Streaming -> S3`

### 7. S3 Becomes the Analytics Storage Layer**
Once data lands in S3, it can be used by downstream systems such as:
- Athena
- AWS Glue
- Redshift
- dashboards
- reporting tools
- additional ETL pipelines

So even though this is a real-time ingestion project, the final output is stored in a format that supports batch analytics and future reporting.




## 📂 Project Structure

├── scripts/
│   ├── stock_producer.py      # Python producer script to fetch/send stock data into Kafka
│   ├── stream_to_s3.py        # Spark Structured Streaming consumer that reads Kafka and writes to S3
├── docker-compose.yml         # Docker setup for Kafka/Zookeeper containers
├── requirements.txt           # Python dependencies
└── README.md
