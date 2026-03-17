import os
import json
import time
import requests
from datetime import datetime
from kafka import KafkaProducer
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("ALPHA_API_KEY")
BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
TOPIC = os.getenv("KAFKA_TOPIC")

SYMBOLS = ["AAPL", "MSFT", "NVDA", "AMZN", "GOOGL"]

producer = KafkaProducer(
    bootstrap_servers=BOOTSTRAP_SERVERS,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

def fetch_quote(symbol):
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "GLOBAL_QUOTE",
        "symbol": symbol,
        "apikey": API_KEY
    }

    response = requests.get(url, params=params)
    data = response.json()

    if "Global Quote" not in data or not data["Global Quote"]:
        return None

    quote = data["Global Quote"]

    return {
        "ticker": symbol,
        "price": float(quote["05. price"]),
        "volume": int(quote["06. volume"]),
        "timestamp": datetime.utcnow().isoformat()
    }


def main():
    print(f"Producing stock data to Kafka topic: {TOPIC}")

    while True:
        for symbol in SYMBOLS:
            try:
                quote = fetch_quote(symbol)
                if quote:
                    producer.send(TOPIC, quote)
                    print("Sent:", quote)
            except Exception as e:
                print(f"Error for {symbol}: {e}")

        producer.flush()
        time.sleep(15)


if __name__ == "__main__":
    main()