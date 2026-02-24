# Local Deployment with Kubernetes

## Setup

#### Requirements

Must have Docker installed and running on your machine.

#### Install Minikube

[Minikube](https://minikube.sigs.k8s.io/docs/start/) is a tool that allows you to run Kubernetes locally. It creates a single-node Kubernetes cluster on your local machine, which is ideal for development and testing purposes. To install Minikube on Linux, you can use the following commands:

```bash
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
```

An alternative to Minikube is [Kind](https://kind.sigs.k8s.io/), which runs Kubernetes clusters in Docker containers.

#### Install `kubectl`

```bash
sudo snap install kubectl --classic
```

#### Start a new Minikube cluster

```bash
minikube start
kubectl cluster-info
```

The start command output:

![minikube start](./images/minikube-start.png)

You can stop and delete the cluster with:

```bash
minikube stop
minikube delete
```
