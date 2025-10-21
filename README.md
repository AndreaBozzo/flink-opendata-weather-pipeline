# Flink OpenData Weather Pipeline

A real-time data pipeline for processing weather data from Open-Meteo API using Apache Flink and Apache Kafka.

## Overview

This project demonstrates a streaming data pipeline that:
- Fetches weather data from the [Open-Meteo API](https://open-meteo.com/) for Milan, Italy
- Streams raw data through Apache Kafka
- Processes data using Apache Flink with validation, enrichment, and transformation
- Outputs processed data to a separate Kafka topic

## Architecture

```
Open-Meteo API → Kafka Producer → Kafka (weather_raw)
                                        ↓
                                   Flink Job
                                   - Validate
                                   - Process
                                   - Enrich
                                   - Transform
                                        ↓
                                Kafka (weather_processed)
```

## Components

### Infrastructure
- **Apache Kafka**: Message broker for streaming data
- **Apache Zookeeper**: Coordination service for Kafka
- **Apache Flink**: Stream processing framework

### Application
- **Producer** (`main/producer.py`): Fetches weather data every 5 minutes and publishes to Kafka
- **Flink Job** (`jobs/flink_job.py`): Consumes, processes, and publishes weather data
- **Weather Processor** (`src/processors/weather_processor.py`): Processing logic for validation, enrichment, and transformation

## Prerequisites

- Python 3.8 or higher
- Docker and Docker Compose
- Poetry (for dependency management)

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd flink-opendata-weather-pipeline
```

### 2. Install dependencies

Using Poetry:
```bash
poetry install
```

Or with pip:
```bash
pip install -r requirements.txt
```

### 3. Start infrastructure

Start Kafka, Zookeeper, and Flink using Docker Compose:

```bash
docker-compose up -d
```

Verify services are running:
- Flink Dashboard: http://localhost:8081
- Kafka: localhost:9092
- Zookeeper: localhost:2181

## Usage

### Run the Producer

The producer fetches weather data from Open-Meteo API and sends it to Kafka:

```bash
poetry run python main/producer.py
```

### Run the Flink Job

Submit the Flink job to the cluster:

```bash
poetry run python jobs/flink_job.py
```

Or submit via Flink CLI:

```bash
docker exec -it flink_jobmanager flink run -py jobs/flink_job.py
```

## Data Flow

### Input Data (from Open-Meteo API)
```json
{
  "current_weather": {
    "temperature": 15.5,
    "windspeed": 10.2,
    "time": "2024-10-21T14:00",
    "weathercode": 2
  },
  "latitude": 45.4642,
  "longitude": 9.19
}
```

### Processed Output
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

## Processing Pipeline

1. **Validation**: Ensures required fields (temperature, windspeed, time, weathercode) are present
2. **Processing**: Adds UTC timestamp for when data was processed
3. **Enrichment**: Adds geographic metadata (city, country, coordinates)
4. **Transformation**: Normalizes data structure and adds computed fields (e.g., `is_heatwave` flag for temperatures > 30°C)

## Configuration

### Weather Location
To change the location for weather data, edit the coordinates in `main/producer.py`:

```python
API_URL = (
    "https://api.open-meteo.com/v1/forecast?"
    "latitude=YOUR_LAT&longitude=YOUR_LON&current_weather=true"
)
```

### Kafka Topics
- **Input Topic**: `weather_raw`
- **Output Topic**: `weather_processed`

### Fetch Interval
The producer fetches data every 5 minutes by default. Adjust in `main/producer.py`:

```python
time.sleep(300)  # 300 seconds = 5 minutes
```

## Development

### Project Structure

```
flink-opendata-weather-pipeline/
├── docker-compose.yml          # Infrastructure orchestration
├── pyproject.toml             # Poetry dependencies
├── jobs/
│   └── flink_job.py          # Main Flink streaming job
├── main/
│   └── producer.py           # Kafka producer
└── src/
    ├── processors/
    │   └── weather_processor.py  # Processing logic
    └── schemas/
        └── weather.py        # Pydantic data schemas
```

### Code Quality

The project uses:
- **Black**: Code formatting
- **Flake8**: Linting
- **mypy**: Type checking
- **isort**: Import sorting

Run code quality checks:

```bash
poetry run black .
poetry run flake8 .
poetry run mypy .
poetry run isort .
```

## Monitoring

Access the Flink Dashboard at http://localhost:8081 to monitor:
- Running jobs
- Task execution
- Throughput metrics
- Checkpoint status

## Troubleshooting

### Kafka Connection Issues
Ensure Docker containers are running:
```bash
docker-compose ps
```

Check Kafka logs:
```bash
docker-compose logs kafka
```

### Flink Job Failures
Check Flink JobManager logs:
```bash
docker-compose logs job_manager
```

Check Flink TaskManager logs:
```bash
docker-compose logs task_manager
```

## License

MIT

## Author

Andrea Bozzo (andreabozzo92@gmail.com)

## Acknowledgments

- Weather data provided by [Open-Meteo](https://open-meteo.com/)
- Built with [Apache Flink](https://flink.apache.org/) and [Apache Kafka](https://kafka.apache.org/)
