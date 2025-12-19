# Monitoring Guide

## Overview

Uses Prometheus and Grafana for monitoring the API performance and health.

## Setup and access

Start the containers using Docker Compose:

```bash
make start
```

This will start the API along with Prometheus and Grafana services.

### Prometheus

Access Prometheus at `http://localhost:9090` and by default, it scrapes metrics from the API at `http://api:8000/metrics`.

To check targets, go to `http://localhost:9090/targets`.

### Grafana

Access Grafana at `http://localhost:3000` and the credentials are set in the `.env` file:

- Username: `GRAFANA_ADMIN_USER`
- Password: `GRAFANA_ADMIN_PASSWORD`
