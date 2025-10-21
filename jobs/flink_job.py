from pyflink.datastream import StreamExecutionEnvironment
from pyflink.common.serialization import SimpleStringSchema
from pyflink.datastream.connectors.kafka import FlinkKafkaConsumer, FlinkKafkaProducer
from src.processors.weather_processor import WeatherDataProcessor


def main():
    env = StreamExecutionEnvironment.get_execution_environment()

    consumer = FlinkKafkaConsumer(
        topics="weather_raw",
        deserialization_schema=SimpleStringSchema(),
        properties={"bootstrap.servers": "kafka:9092", "group.id": "flink-weather"},
    )

    producer = FlinkKafkaProducer(
        topic="weather_processed",
        serialization_schema=SimpleStringSchema(),
        producer_config={"bootstrap.servers": "kafka:9092"},
    )

    stream = env.add_source(consumer)

    processed = (
        stream
        .filter(WeatherDataProcessor.validate)
        .map(WeatherDataProcessor.process)
        .map(lambda r: WeatherDataProcessor.enrich(r, {"city": "Milan", "country": "Italy"}))
        .map(WeatherDataProcessor.transform)
        .filter(lambda r: r is not None)
    )

    processed.add_sink(producer)
    env.execute("Weather OpenData Stream Processor")


if __name__ == "__main__":
    main()
