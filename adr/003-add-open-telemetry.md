# Add Open Telemetry

## Context

There's a lack of observability in rafood-api, making it difficult to monitor performance, trace requests, and diagnose issues effectively.

Implementing Open Telemetry will provide a standardized way to collect and export telemetry data, enhancing our ability to observe and analyze the system's behavior.

## Decision

We are proposing to integrate Open Telemetry into the rafood-api codebase.

This will involve instrumenting the code to collect telemetry data such as traces, metrics, and logs, and exporting this data to a backend for analysis and visualization.

Tools used:

- OpenTelemetry SDKs for instrumentation
- Prometheus for metrics collection
- Grafana for visualization
- Loki for log aggregation (*extra*)
- Database monitoring on Grafana (*extra*)

## Consequences

- Better observability into the system's performance and behavior.
- Improved ability to trace requests and diagnose issues.
- Enhanced monitoring capabilities through metrics and logs.

## References

- [Part 1 - Building a Powerful Observability Stack for FastAPI with Prometheus, Grafana, and Loki](https://dimasyotama.medium.com/building-a-powerful-observability-stack-for-fastapi-with-prometheus-grafana-loki-426822422fd6)
- [Part 2 - Elevating FastAPI Observability: Integrating Grafana Tempo for Distributed Tracing](https://dimasyotama.medium.com/elevating-fastapi-observability-integrating-grafana-tempo-for-distributed-tracing-7a9c72dedac4)
- [Getting Started: Monitoring a FastAPI App with Grafana and Prometheus](https://dev.to/ken_mwaura1/getting-started-monitoring-a-fastapi-app-with-grafana-and-prometheus-a-step-by-step-guide-3fbn) - Good reference for Prometheus and Grafana setup
- [FastAPI Observability Lab with Prometheus and Grafana: Complete Guide](https://pub.towardsai.net/fastapi-observability-lab-with-prometheus-and-grafana-complete-guide-f12da15a15fd) - Complete guide for FastAPI observability with Prometheus and Grafana

# Results

## Tips

- To validate prometheus is scraping the metrics from the API, access `http://localhost:9090/targets` after starting the containers with `make start` and check if the API target is listed as "UP".
- To access Grafana, go to `http://localhost:3000` (credentials on `.env`).
