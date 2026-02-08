# Add Local Deployment With Kubernetes

## Context

Currently, the API is only available by running it locally. We'll never deploy this application to production, but it would be useful to have a way to deploy it locally in a more realistic environment. This would help with testing and development, allowing us to simulate a production-like setup without needing to run everything on a single machine.

## Decision

Add a local deployment option using Kubernetes. This will involve creating Kubernetes manifests or Helm charts that define the necessary resources (pods, services, etc.) to run the API in a local Kubernetes cluster, such as Minikube or Kind.

> [!NOTE]
> It's important to note that this local deployment is intended for development and testing purposes only. It will not be used for production deployments.
> The local deployment must have database connectivity to the existing local PostgreSQL instance used by the API or any other service running locally.

## Consequences

By implementing local deployment with Kubernetes, developers will be able to test the API in an environment that closely resembles production. This will facilitate better testing of features and bug fixes, as well as improve the overall development workflow. However, it may introduce some complexity in terms of setup and maintenance of the Kubernetes configurations.

## References

- [Docker and Kubernetes for Local Deployment Using FastAPI](https://medium.com/@wrefordmessi/docker-and-kubernetes-for-local-deployment-using-fastapi-1c8df431ed95) - How-to with a FastAPI application, deployment and service configuration to expose the app (uses Minikube).
- [K8s-fastapi](https://github.com/coolchigi/K8s-fastapi) - Deployment instructions on README file (uses Minikube).
- [Running Kubernetes Locally with Docker Desktop and Kind: A Developer's Guide](https://medium.com/@fahmidhathurab7/running-kubernetes-locally-with-docker-desktop-and-kind-a-developers-guide-531ae1b7b5f5) - Detailed guide on setting up a local Kubernetes cluster using Docker Desktop and Kind (more specific alternative to Minikube).
- [Deploying a REST API on a Local K8 Cluster](https://medium.com/@tineshkumar_16453/deploying-a-rest-api-on-a-local-k8-cluster-159acc9ad0ee) - More robust example of deploying a REST API to a local Kubernetes cluster, including database connectivity, secrets, service and ingress configuration.
- [FastAPI Kubernetes Deployment](https://medium.com/@lorencattoaugusto/fastapi-kubernetes-deployment-d96c3c0310fe) - Complete guide including deployment, service, secrets, database connectivity, HPA and stress testing in pt-BR (uses kind). *That's a good one.*
- [Deploy an App from Scratch to Kubernetes Before Your Next Break Ends](https://8thlight.com/insights/deploy-an-app-from-scratch-to-kubernetes-before-your-next-break-ends) - Simple example of deploying and deleting application to a local Kubernetes cluster.
