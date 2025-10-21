# Flink Configuration

This directory contains Apache Flink configuration files used by the Docker Compose setup.

## Files

### flink-conf.yaml
Main Flink configuration file that defines:
- **JobManager** settings (RPC address, memory, ports)
- **TaskManager** settings (slots, memory, network)
- **State backend** configuration (checkpoints, savepoints)
- **Web UI** settings (REST API port)

### log4j-console.properties
Logging configuration for Flink components.
- Logs are written to console output
- Default log level: INFO
- Can be viewed with: `docker logs flink_jobmanager` or `docker logs flink_taskmanager`

## Key Configuration Parameters

| Parameter | Value | Description |
|-----------|-------|-------------|
| `jobmanager.rpc.address` | job_manager | Hostname of JobManager |
| `jobmanager.rpc.port` | 6123 | RPC port for JobManager |
| `rest.port` | 8081 | Web UI port |
| `taskmanager.numberOfTaskSlots` | 2 | Parallel tasks per TaskManager |
| `parallelism.default` | 1 | Default job parallelism |

## Customization

To modify Flink settings:
1. Edit the configuration files in this directory
2. Restart the Docker containers: `docker-compose restart job_manager task_manager`

## Documentation

For complete configuration options, see:
- [Flink Configuration](https://nightlies.apache.org/flink/flink-docs-stable/docs/deployment/config/)
