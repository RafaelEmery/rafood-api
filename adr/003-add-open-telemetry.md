# Add Open Telemetry

## Context

There's a lack of observability in rafood-api, making it difficult to monitor performance, trace requests, and diagnose issues effectively.

Implementing Open Telemetry will provide a standardized way to collect and export telemetry data, enhancing our ability to observe and analyze the system's behavior.

## Decision

We are proposing to integrate Open Telemetry into the rafood-api codebase.

This will involve instrumenting the code to collect telemetry data such as traces, metrics, and logs, and exporting this data to a backend for analysis and visualization.

Goals:

- OpenTelemetry related libs for Python and FastAPI (`prometheus-fastapi-instrumentator`) :white_check_mark:
- Prometheus for metrics collection :white_check_mark:
- Grafana for visualization :white_check_mark:
- Loki for log aggregation (*extra*)
- Database monitoring on Grafana (*extra*) :white_check_mark:

## Consequences

- Better observability into the system's performance and behavior.
- Improved ability to trace requests and diagnose issues.
- Enhanced monitoring capabilities through metrics and logs.

## References

- [Part 1 - Building a Powerful Observability Stack for FastAPI with Prometheus, Grafana, and Loki](https://dimasyotama.medium.com/building-a-powerful-observability-stack-for-fastapi-with-prometheus-grafana-loki-426822422fd6)
- [Part 2 - Elevating FastAPI Observability: Integrating Grafana Tempo for Distributed Tracing](https://dimasyotama.medium.com/elevating-fastapi-observability-integrating-grafana-tempo-for-distributed-tracing-7a9c72dedac4)
- [Getting Started: Monitoring a FastAPI App with Grafana and Prometheus](https://dev.to/ken_mwaura1/getting-started-monitoring-a-fastapi-app-with-grafana-and-prometheus-a-step-by-step-guide-3fbn) - Good reference for Prometheus and Grafana setup
- [FastAPI Observability Lab with Prometheus and Grafana: Complete Guide](https://pub.towardsai.net/fastapi-observability-lab-with-prometheus-and-grafana-complete-guide-f12da15a15fd) - Complete guide for FastAPI observability with Prometheus and Grafana
- [Docker Container Monitoring with cAdvisor, Prometheus, and Grafana using Docker Compose](https://medium.com/@sohammohite/docker-container-monitoring-with-cadvisor-prometheus-and-grafana-using-docker-compose-b47ec78efbc) - Reference for using cAdvisor with Prometheus and Grafana and dashboard example

______________________________________________________________________

More details at [docs/monitoring.md](../docs/monitoring.md)
