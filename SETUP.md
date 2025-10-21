# Setup Guide

This guide provides step-by-step instructions to set up and run the Flink OpenData Weather Pipeline.

## Prerequisites

Before starting, ensure you have:
- **Python 3.9+** installed (required for PyFlink 1.20+)
- **Docker** and **Docker Compose** installed
- **Poetry** or **pip** for Python dependency management

## Quick Start

### 1. Install Dependencies

**Using Poetry (recommended):**
```bash
poetry install
```

**Using pip:**
```bash
pip install -r requirements.txt
```

### 2. Start Infrastructure

Start Kafka, Zookeeper, and Flink containers:
```bash
docker-compose up -d
```

Verify services are running:
```bash
docker-compose ps
```

Expected output:
```
NAME                  IMAGE                          STATUS
flink_jobmanager      apache/flink:1.20             Up
flink_taskmanager     apache/flink:1.20             Up
kafka                 wurstmeister/kafka:2.13-2.8.1 Up
zookeeper             wurstmeister/zookeeper:3.4.6  Up
```

### 3. Run the Producer

In a new terminal, start the Kafka producer:
```bash
poetry run python main/producer.py
```

You should see messages like:
```
Sent data to Kafka topic weather_raw: {...}
```

### 4. Run the Flink Job

In another terminal, submit the Flink job:
```bash
poetry run python jobs/flink_job.py
```

### 5. Monitor (Optional)

Run the example consumer to see processed data:
```bash
poetry run python examples/consumer_example.py
```

## Verification

### Check Flink Dashboard
Visit http://localhost:8081 to see:
- Running jobs
- Task execution
- Metrics

### Check Kafka Topics
```bash
docker exec -it kafka kafka-topics.sh --list --bootstrap-server localhost:9092
```

Expected topics:
- `weather_raw`
- `weather_processed`

## Troubleshooting

### Python Version Issues
If you see errors about Python version, ensure you're using Python 3.9+:
```bash
python --version
```

### Kafka Connection Refused
Ensure Docker containers are running:
```bash
docker-compose ps
docker-compose logs kafka
```

### PyFlink Import Errors
Install apache-flink:
```bash
pip install apache-flink>=1.20.0
```

### Port Already in Use
If ports 8081, 9092, or 2181 are in use, stop conflicting services or modify ports in `docker-compose.yml`.

## Stopping the Pipeline

Stop all containers:
```bash
docker-compose down
```

Remove volumes (optional, deletes data):
```bash
docker-compose down -v
```

## Next Steps

- Customize weather location in `main/producer.py`
- Modify processing logic in `src/processors/weather_processor.py`
- Add new transformations to the Flink job
- Explore the Pydantic schemas in `src/schemas/weather.py`
