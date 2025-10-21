"""
Example Kafka consumer to read processed weather data.
This script demonstrates how to consume the processed weather data
from the 'weather_processed' Kafka topic.
"""

import json
from kafka import KafkaConsumer


def main():
    """Consume and display processed weather data from Kafka."""
    consumer = KafkaConsumer(
        'weather_processed',
        bootstrap_servers='localhost:9092',
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='weather-consumer-group',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    print("Listening for processed weather data...")
    print("Press Ctrl+C to stop\n")

    try:
        for message in consumer:
            data = message.value
            print(f"--- New Weather Data ---")
            print(f"Timestamp: {data.get('timestamp')}")
            print(f"Temperature: {data.get('temperature')}°C")
            print(f"Wind Speed: {data.get('windspeed')} m/s")
            print(f"Condition Code: {data.get('condition')}")
            print(f"Location: {data.get('location', {}).get('city')}")
            print(f"Heatwave: {data.get('is_heatwave')}")
            print(f"Processed at: {data.get('processed_timestamp')}")
            print("-" * 40 + "\n")
    except KeyboardInterrupt:
        print("\nStopping consumer...")
    finally:
        consumer.close()


if __name__ == "__main__":
    main()
