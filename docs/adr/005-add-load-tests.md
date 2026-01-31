# Add Load Tests

## Context

Load Tests are essential to ensure that our application can handle expected user loads and perform well under stress. By implementing load tests, we can identify potential bottlenecks, optimize performance, and ensure a smooth user experience even during peak usage times.

## Decision

Test different user and simultaneous connections scenarios using [Locust](https://locust.io/) as the load testing tool. The tests will simulate various levels of traffic to evaluate the application's performance, scalability, and reliability under different conditions.

Every API endpoints (e.g. restaurants, categories, products) will have its own task sets to simulate real-world usage patterns. The task sets will be defined at a specific directory and used at base `locustfile.py` on `locust/`.

The monitoring profile proposed at [add-open-telemetry](003-add-open-telemetry.md) ADR using Prometheus and Grafana can be used as a reference to analyze the results and identify performance bottlenecks during the load tests.

## Consequences

- Better understanding of application performance under load.
- Identification of performance bottlenecks.
- Improved application scalability and reliability.
- Enhanced user experience during high traffic periods.

## References

- [Locust Documentation](https://docs.locust.io/en/stable/)
