import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    from_json,
    to_timestamp,
    window,
    avg,
    date_format
)
from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    DoubleType,
    IntegerType
)
from dotenv import load_dotenv

load_dotenv()

BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
TOPIC = os.getenv("KAFKA_TOPIC", "stock-prices")
S3_BUCKET = os.getenv("S3_BUCKET")
AWS_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

if not S3_BUCKET:
    raise ValueError("S3_BUCKET is missing in .env")

checkpoint_path = f"s3a://{S3_BUCKET}/checkpoints/stock_5min_avg/"
output_path = f"s3a://{S3_BUCKET}/output/stock_5min_avg/"

schema = StructType([
    StructField("ticker", StringType(), True),
    StructField("price", DoubleType(), True),
    StructField("high", DoubleType(), True),
    StructField("low", DoubleType(), True),
    StructField("open", DoubleType(), True),
    StructField("prev_close", DoubleType(), True),
    StructField("api_timestamp", IntegerType(), True),
    StructField("event_time", StringType(), True),
    StructField("source", StringType(), True),
])

spark = (
    SparkSession.builder
    .appName("RealTimeStockStreaming")
    .config("spark.hadoop.fs.s3a.access.key", AWS_ACCESS_KEY_ID)
    .config("spark.hadoop.fs.s3a.secret.key", AWS_SECRET_ACCESS_KEY)
    .config("spark.hadoop.fs.s3a.endpoint.region", AWS_REGION)
    .config("spark.hadoop.fs.s3a.aws.credentials.provider",
            "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider")
    .config("spark.sql.shuffle.partitions", "4")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

raw_df = (
    spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", BOOTSTRAP_SERVERS)
    .option("subscribe", TOPIC)
    ..option("startingOffsets", "earliest")
    .load()
)

parsed_df = (
    raw_df
    .selectExpr("CAST(value AS STRING) as json_str")
    .select(from_json(col("json_str"), schema).alias("data"))
    .select("data.*")
    .withColumn("event_ts", to_timestamp(col("event_time")))
)

# Sliding window: every 1 minute, compute over previous 5 minutes
agg_df = (
    parsed_df
    .withWatermark("event_ts", "10 minutes")
    .groupBy(
        window(col("event_ts"), "5 minutes", "1 minute"),
        col("ticker")
    )
    .agg(avg("price").alias("avg_price"))
    .select(
        col("ticker"),
        col("avg_price"),
        col("window.start").alias("window_start"),
        col("window.end").alias("window_end"),
        date_format(col("window.start"), "yyyy-MM-dd").alias("date")
    )
)

query = (
    agg_df.writeStream
    .format("parquet")
    .outputMode("append")
    .option("path", output_path)
    .option("checkpointLocation", checkpoint_path)
    .partitionBy("date", "ticker")
    .trigger(processingTime="1 minute")
    .start()
)

query.awaitTermination()