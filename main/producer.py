import json
import time
import requests

from kafka import KafkaProducer

API_URL = (
    "https://api.open-meteo.com/v1/forecast?"
    "latitude=45.4642&longitude=9.19&current_weather=true"
)
KAFKA_TOPIC = "weather_raw"


def main():
    producer = KafkaProducer(
        bootstrap_servers='localhost:9092',
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

    while True:
        try:
            response = requests.get(API_URL)
            response.raise_for_status()
            weather_data = response.json()
            producer.send(KAFKA_TOPIC, weather_data)
            print(f"Sent data to Kafka topic {KAFKA_TOPIC}: {weather_data}")
        except requests.RequestException as e:
            print(f"Error fetching weather data: {e}")
        except Exception as e:
            print(f"Error sending data to Kafka: {e}")

        time.sleep(300)  # Wait for 5 minutes before fetching new data


if __name__ == "__main__":
    main()
