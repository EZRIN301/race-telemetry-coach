# Lab 0 Decision Record — RaceTelemetryCoach

## Working Region
us-east-2

## AWS Identity
CloudShell authentication succeeded through the UMGC StudentAdminAccess role.

## ECR Result
Available. The account can list ECR repositories. Docker images may be stored in Amazon ECR during a later lab.

## EKS Result
Cluster listing is available. No EKS clusters currently exist. EKS creation permission and quota availability remain unverified.

## Bedrock Result
Foundation model listing is available in us-east-2. Bedrock may be used later for race-engineer summaries, embeddings, and telemetry explanations. Model invocation permission must be tested separately with a small controlled request.

## Development Path
1. Build telemetry analysis locally in Python.
2. Containerize the application with Docker.
3. Push the image to ECR.
4. Learn Kubernetes with K3s first.
5. Use Bedrock after budget guardrails are confirmed.
6. Attempt EKS only after the containerized application is working.

## Cost Guardrails
Do not create NAT gateways, EKS clusters, public load balancers, GPU nodes, or long-running EC2 instances during early labs.
