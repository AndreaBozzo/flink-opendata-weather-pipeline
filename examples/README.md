# Examples

This directory contains example scripts for working with the weather pipeline.

## Consumer Example

The `consumer_example.py` script demonstrates how to consume processed weather data from Kafka.

### Usage

1. Ensure Docker Compose services are running:
   ```bash
   docker-compose up -d
   ```

2. Start the producer (in a separate terminal):
   ```bash
   poetry run python main/producer.py
   ```

3. Start the Flink job (in another terminal):
   ```bash
   poetry run python jobs/flink_job.py
   ```

4. Run the consumer example:
   ```bash
   poetry run python examples/consumer_example.py
   ```

You should see processed weather data being printed to the console in real-time.

## Custom Consumer

To create your own consumer, use the `weather_processed` topic:

```python
from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'weather_processed',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

for message in consumer:
    weather_data = message.value
    # Process your data here
    print(weather_data)
```

## Data Format

Processed messages follow this structure:

```json
{
  "timestamp": "2024-10-21T14:00",
  "temperature": 15.5,
  "windspeed": 10.2,
  "condition": 2,
  "processed_timestamp": "2024-10-21T14:05:23.123456+00:00",
  "is_heatwave": false,
  "location": {
    "latitude": 45.4642,
    "longitude": 9.19,
    "city": "Milan",
    "country": "Italy"
  }
}
```
