# Local Deployment with Kubernetes

## Setup

### Requirements

Must have Docker installed and running on your machine.

### Install Minikube

[Minikube](https://minikube.sigs.k8s.io/docs/start/) is a tool that allows you to run Kubernetes locally. It creates a single-node Kubernetes cluster on your local machine, which is ideal for development and testing purposes. To install Minikube on Linux, you can use the following commands:

```bash
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
```

By running `minikube dashboard` you can access the Minikube dashboard to monitor the cluster.

An alternative to Minikube is [Kind](https://kind.sigs.k8s.io/), which runs Kubernetes clusters in Docker containers.

### Install `kubectl`

```bash
sudo snap install kubectl --classic
```

Useful commands for `kubectl`

```bash
kubectl get pods

kubectl get services

kubectl delete pods --all

kubectl delete services --all

kubectl delete deployments --all

kubectl logs -f <pod-name>
```

### Start a new Minikube cluster

```bash
minikube start

minikube status

kubectl cluster-info
```

The start command output:

![minikube start](./images/minikube-start.png)

You can stop and delete the cluster with:

```bash
minikube stop
minikube delete
```

### Install Helm and Helm Docs

[Helm](https://helm.sh/) is a package manager for Kubernetes that helps you manage Kubernetes applications. It allows you to define, install, and upgrade complex Kubernetes applications using simple configuration files called Helm Charts.

You can install Helm on Linux using Snap (recommended for easier updates):

```bash
sudo snap install helm --classic

sudo snap install helm-docs
```

### Extra: use k9s

[k9s](https://k9scli.io/) is a terminal-based UI to interact with your Kubernetes clusters. It provides an easy way to navigate and manage your Kubernetes resources.

After installing, you just need to run `k9s` on your terminal. Tips for using k9s:

- `k9s` — open the interactive interface
- Use arrow keys ↑ ↓ to navigate between resources
- `/` — filter by name
- `l` — view logs of the selected pod
- `s` — open a shell in the selected pod
- `:ns` — switch namespace
- `:deploy` — view deployments
- `:svc` — view services
- `esc` — go back to the previous screen
- `:q` — quit k9s

At the top of the screen, k9s shows quick key hints for each context.

# Studies notes

The order and the process of my Kubernetes studies are:

1. Making initial setup with Minikube and kubectl
1. Basic service and deployment configuration example
1. Deploying application with Helm
1. Deploying application with ArgoCD

## Basic service and deployment configuration example

> Reference: [Docker and Kubernetes for Local Deployment Using FastAPI](https://medium.com/@wrefordmessi/docker-and-kubernetes-for-local-deployment-using-fastapi-1c8df431ed95) - How-to with a FastAPI application, deployment and service configuration to expose the app (uses Minikube).

### Pre requisites

The Docker image won't be at Docker Hub, so we must declare `imagePullPolicy: Never` in the deployment configuration and build the image inside the Minikube environment:

```bash
# If minikube has not started
minikube start

eval $(minikube docker-env)

make build-container

# Verify the image is built inside minikube
docker images | grep rafood-api

# Warning: you must return to default environment
eval $(minikube docker-env -u)
```

### Deployment configuration

```yaml
apiVersion: apps/v1            # API group/version for workload resources (Deployment)
kind: Deployment               # Declares a controller that manages Pods via ReplicaSets
metadata:
  name: rafood-api             # Unique name of the Deployment within the namespace
  labels:
    app: rafood-api            # Labels used for organization and selection
spec:
  replicas: 2                  # Desired number of running Pods (horizontal scaling)
  selector:
    matchLabels:
      app: rafood-api          # Selects which Pods belong to this Deployment (must match template.labels)
  template:                    # Pod template that will be replicated
    metadata:
      labels:
        app: rafood-api        # Labels applied to created Pods
    spec:
      containers:
        - name: rafood-api     # Container name inside the Pod
          image: rafood-api:latest   # Container image (using 'latest' is not recommended in production)
          imagePullPolicy: Never     # Never pull image from registry (use local image only)
          ports:
            - containerPort: 8000    # Port exposed by the container (informational for the cluster)
          resources:
            limits:
              memory: "512Mi"        # Maximum memory allowed (exceeding → OOMKilled)
              cpu: "500m"            # Maximum CPU allowed (0.5 core)
            requests:
              memory: "256Mi"        # Minimum memory guaranteed for scheduling
              cpu: "250m"            # Minimum CPU guaranteed (0.25 core)
```

### Service configuration

```yaml
apiVersion: v1                 # Core API group (Service belongs to core/v1)
kind: Service                  # Network abstraction to expose a set of Pods
metadata:
  name: rafood-api-service     # Unique Service name (creates stable internal DNS)
  labels:
    app: rafood-api            # Labels for organization
spec:
  selector:
    app: rafood-api            # Selects Pods with this label to receive traffic
  type: LoadBalancer           # Exposes Service externally via cloud load balancer (uses NodePort internally)
  ports:
    - protocol: TCP            # Transport protocol (default is TCP)
      port: 5000               # Port exposed by the Service inside the cluster
      targetPort: 8000         # Actual container port receiving traffic
      nodePort: 31110          # Fixed port exposed on each Node (default range 30000–32767)
```

### Apply the configurations

> [!NOTE]
> The manifest files were moved to the `kubernetes/sandbox/manifests` directory for better organization because the deployment and service configurations are the same for both Helm and ArgoCD. The `sandbox/manifests` directory is used to document the study notes and examples.

```bash
kubectl apply -f kubernetes/sandbox/manifests/deployment.yml
kubectl apply -f kubernetes/sandbox/manifests/service.yml
```

To monitor the pods, you can use and check logs:

```bash
kubectl get pods
kubectl logs -f <pod-name>
```

Example output of `kubectl get pods`:

```bash
NAME                         READY   STATUS    RESTARTS   AGE
rafood-api-5659bf766-87cfs   1/1     Running   0          25m
rafood-api-5659bf766-bhqqj   1/1     Running   0          25m
```

Or use k9s to monitor the pods and logs in a more interactive way:

![k9s pods logs example](./images/k9s-pods-logs-example.png)

### Access the service

To access the service, you can use the `minikube service` command, which will open the service in your default web browser:

```bash
minikube service rafood-api-service
```

This command will automatically open the URL where your service is exposed, allowing you to interact with your FastAPI application running in the Minikube cluster.

Calling health check on Postman:

![minikube cluster health check](./images/minikube-cluster-healthcheck.png)

### Stopping the cluster

When you're done, you can stop the Minikube cluster:

> [!NOTE]
> The `stop` command will stop the cluster but keep it available for later use. You won't need to apply any configurations again.
> If you want to completely remove the cluster, you can use the `delete` command.

```bash
minikube stop
```

## Deploying application with Helm

> Reference: [Using Helm with Kubernetes: A Guide to Helm Charts and Their Implementation](https://dev.to/alexmercedcoder/using-helm-with-kubernetes-a-guide-to-helm-charts-and-their-implementation-8dg) - Complete guide for using Helm (and extra ArgoCD tutorial)

### Context about Helm

> Helm is a package manager for Kubernetes that helps deploy, configure, and manage applications in a Kubernetes cluster. Instead of manually writing and applying multiple Kubernetes YAML manifests, Helm allows you to package them into reusable Helm Charts, simplifying deployment and maintenance.

| Feature         | Kubernetes YAML Manifests                      | Helm Charts                                                  |
| --------------- | ---------------------------------------------- | ------------------------------------------------------------ |
| Management      | Requires manually applying multiple YAML files | Uses a single Helm command                                   |
| Configuration   | Static YAML definitions                        | Dynamic templating via values.yaml                           |
| Version Control | Difficult to track changes manually            | Built-in versioning & rollback                               |
| Reusability     | Limited; each deployment needs its own YAML    | Reusable and configurable charts                             |
| Dependencies    | Managed manually                               | Handled via `requirements.yaml` (deprecated) or `Chart.yaml` |

### Install and configure Helm

To clean minikube cluster:

```bash
minikube stop

minikube delete

minikube start

# Another way to verify if cluster is running
kubectl get nodes
```

To create a Helm chart for the Rafood API application, you can use the following command:

```bash
helm create rafood-api
```

> [!NOTE]
> The `helm create` command generates a basic Helm chart structure with default templates for deployment, service, and other Kubernetes resources. You can then customize these templates to fit the specific requirements of your application, such as setting the correct image name, ports, and resource limits.

The generated `values.yaml` file contains default values for the Helm chart, which can be overridden when deploying the chart. Below is an example of what the generated `values.yaml` file might look like, with comments explaining each section.

<details>
<summary>Generated Values file</summary>

```yaml
# Default values for rafood-api.
# This is a YAML-formatted file.
# Declare variables to be passed into your templates.

# This will set the replicaset count more information can be found here: https://kubernetes.io/docs/concepts/workloads/controllers/replicaset/
replicaCount: 1

# This sets the container image more information can be found here: https://kubernetes.io/docs/concepts/containers/images/
image:
  repository: nginx
  # This sets the pull policy for images.
  pullPolicy: IfNotPresent
  # Overrides the image tag whose default is the chart appVersion.
  tag: ""

# This is for the secrets for pulling an image from a private repository more information can be found here: https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/
imagePullSecrets: []
# This is to override the chart name.
nameOverride: ""
fullnameOverride: ""

# This section builds out the service account more information can be found here: https://kubernetes.io/docs/concepts/security/service-accounts/
serviceAccount:
  # Specifies whether a service account should be created.
  create: true
  # Automatically mount a ServiceAccount's API credentials?
  automount: true
  # Annotations to add to the service account.
  annotations: {}
  # The name of the service account to use.
  # If not set and create is true, a name is generated using the fullname template.
  name: ""

# This is for setting Kubernetes Annotations to a Pod.
# For more information checkout: https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/
podAnnotations: {}
# This is for setting Kubernetes Labels to a Pod.
# For more information checkout: https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/
podLabels: {}

podSecurityContext: {}
  # fsGroup: 2000

securityContext: {}
  # capabilities:
  #   drop:
  #   - ALL
  # readOnlyRootFilesystem: true
  # runAsNonRoot: true
  # runAsUser: 1000

# This is for setting up a service more information can be found here: https://kubernetes.io/docs/concepts/services-networking/service/
service:
  # This sets the service type more information can be found here: https://kubernetes.io/docs/concepts/services-networking/service/#publishing-services-service-types
  type: ClusterIP
  # This sets the ports more information can be found here: https://kubernetes.io/docs/concepts/services-networking/service/#field-spec-ports
  port: 80

# This block is for setting up the ingress for more information can be found here: https://kubernetes.io/docs/concepts/services-networking/ingress/
ingress:
  enabled: false
  className: ""
  annotations: {}
    # kubernetes.io/ingress.class: nginx
    # kubernetes.io/tls-acme: "true"
  hosts:
    - host: chart-example.local
      paths:
        - path: /
          pathType: ImplementationSpecific
  tls: []
    # - secretName: chart-example-tls
    #   hosts:
    #     - chart-example.local

# -- Expose the service via gateway-api HTTPRoute
# Requires Gateway API resources and suitable controller installed within the cluster
# (see: https://gateway-api.sigs.k8s.io/guides/)
httpRoute:
  # HTTPRoute enabled.
  enabled: false
  # HTTPRoute annotations.
  annotations: {}
  # Which Gateways this Route is attached to.
  parentRefs:
  - name: gateway
    sectionName: http
    # namespace: default
  # Hostnames matching HTTP header.
  hostnames:
  - chart-example.local
  # List of rules and filters applied.
  rules:
  - matches:
    - path:
        type: PathPrefix
        value: /headers
  #   filters:
  #   - type: RequestHeaderModifier
  #     requestHeaderModifier:
  #       set:
  #       - name: My-Overwrite-Header
  #         value: this-is-the-only-value
  #       remove:
  #       - User-Agent
  # - matches:
  #   - path:
  #       type: PathPrefix
  #       value: /echo
  #     headers:
  #     - name: version
  #       value: v2

resources: {}
  # We usually recommend not to specify default resources and to leave this as a conscious
  # choice for the user. This also increases chances charts run on environments with little
  # resources, such as Minikube. If you do want to specify resources, uncomment the following
  # lines, adjust them as necessary, and remove the curly braces after 'resources:'.
  # limits:
  #   cpu: 100m
  #   memory: 128Mi
  # requests:
  #   cpu: 100m
  #   memory: 128Mi

# This is to setup the liveness and readiness probes more information can be found here: https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/
livenessProbe:
  httpGet:
    path: /
    port: http
readinessProbe:
  httpGet:
    path: /
    port: http

# This section is for setting up autoscaling more information can be found here: https://kubernetes.io/docs/concepts/workloads/autoscaling/
autoscaling:
  enabled: false
  minReplicas: 1
  maxReplicas: 100
  targetCPUUtilizationPercentage: 80
  # targetMemoryUtilizationPercentage: 80

# Additional volumes on the output Deployment definition.
volumes: []
  # - name: foo
  #   secret:
  #     secretName: mysecret
  #     optional: false

# Additional volumeMounts on the output Deployment definition.
volumeMounts: []
  # - name: foo
  #   mountPath: "/etc/foo"
  #   readOnly: true

nodeSelector: {}

tolerations: []

affinity: {}
```

</details>

### Basic helm charts by deployment and service configurations

`values.yaml`:

```yaml
replicaCount: 1

image:
  repository: rafood-api
  tag: "latest"
  pullPolicy: IfNotPresent

service:
  type: NodePort
  port: 80
  targetPort: 8000

containerPort: 8000
```

`deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "rafood-api.fullname" . }}
spec:
  replicas: {{ .Values.replicaCount }}

  selector:
    matchLabels:
      app: {{ include "rafood-api.name" . }}

  template:
    metadata:
      labels:
        app: {{ include "rafood-api.name" . }}

    spec:
      containers:
        - name: rafood-api
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
          imagePullPolicy: {{ .Values.image.pullPolicy }}

          ports:
            - containerPort: {{ .Values.containerPort }}
```

`service.yaml`:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: {{ include "rafood-api.fullname" . }}

spec:
  type: {{ .Values.service.type }}

  selector:
    app: {{ include "rafood-api.name" . }}

  ports:
    - port: {{ .Values.service.port }}
      targetPort: {{ .Values.service.targetPort }}
```

> The `Chart.yaml` file contains only metadata for the chart.

### Installing the Helm chart

Before install, make sure that the image is built inside the Minikube environment, verify if templates are rendering correctly and if variables are being applied:

> Helm commands must be at `kubernetes/charts` directory.

```bash
eval $(minikube docker-env)
make build-container

# Validate the rendered templates with the current values
# The output will show the Kubernetes manifests that Helm would apply, allowing you to verify that the variables from `values.yaml` are correctly substituted in the templates.
helm template rafood-api ./rafood-api

helm lint ./rafood-api
```

To install the chart:

```bash
helm install rafood-api ./rafood-api
```

The expected output should be similar to:

```
NAME: rafood-api
LAST DEPLOYED: Mon Mar  2 21:00:22 2026
NAMESPACE: default
STATUS: deployed
REVISION: 1
DESCRIPTION: Install complete
TEST SUITE: None
```

And then... 🪄✨ *magic* 🪄✨

The application is deployed on Minikube cluster! You can check the pods and logs with `kubectl get pods`, `minikube service rafood-api` and `kubectl logs -f <pod-name>` commands or k9s.

### History and rollback

You can check Helm history and rollback to a previous revision if needed:

```bash
helm history rafood-api

helm rollback rafood-api <revision-number>
```

### Generating documentation with helm-docs

Go to `kubernetes/charts/rafood-api` directory and run the command above. A `README.md` file will be generated with the chart metadata and values description. This is useful for documentation and sharing the chart with others:

```bash
helm-docs
```

## Deploying application with ArgoCD

### Context about ArgoCD

> Reference: [ArgoCD Documentation](https://argo-cd.readthedocs.io/en/stable/) and [
> GITOPS? Aprenda a usar na prática com Argo CD e Kubernetes](https://www.youtube.com/watch?v=k1GeGLlqZBU) - YouTube video by @codigofontetv

ArgoCD is a declarative, GitOps continuous delivery tool for Kubernetes. It follows the GitOps pattern of using Git as the source of truth for the desired state of the application. It can be used to deploy and manage applications on Kubernetes clusters.

### Install and configure ArgoCD

To clean minikube cluster:

```bash
minikube stop

minikube delete

minikube start

# Another way to verify if cluster is running
kubectl get nodes
```

Create a new namespace for ArgoCD and install ArgoCD:

```bash
kubectl create namespace argocd

# Installing ArgoCD and all required resources using the official manifest file
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

To check if ArgoCD is installed correctly, you can use the following commands:

```bash
kubectl get pods -n argocd

minikube service list

# To access the minikube dashboard to check "argocd" namespace services
minikube dashboard
```

### Access the ArgoCD UI

To access the ArgoCD UI, you can use the following command:

```bash
kubectl port-forward svc/argocd-server -n argocd 8080:443
```

And then you can access the ArgoCD UI at `http://localhost:8080` using the default credentials:

```bash
echo $(kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d)
```

> [!NOTE] The default login is `admin` and the password is the one obtained from the command above.

To change the password, you can use the following command:

```bash
# Must be validated if it's the correct command to change the password
kubectl patch secret argocd-secret -n argocd -p '{"stringData": {"admin.password": "your-new-password-here"}}'
```

### Deploying the application with ArgoCD

> [!NOTE]
> The application will be deployed to the `default` namespace.
