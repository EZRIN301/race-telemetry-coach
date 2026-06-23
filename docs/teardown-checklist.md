# RaceTelemetryCoach Teardown Checklist

Before ending a lab session:
- [ ] Terminate all EC2 instances.
- [ ] Delete unused EBS volumes and snapshots.
- [ ] Release unattached Elastic IP addresses.
- [ ] Delete NAT gateways after deleting dependent routes.
- [ ] Delete public and private load balancers.
- [ ] Delete EKS node groups before deleting the EKS cluster.
- [ ] Delete Kubernetes LoadBalancer services and ingress resources.
- [ ] Delete ECR images and repositories created for the project.
- [ ] Delete test S3 objects and buckets after preserving required evidence.
- [ ] Delete unneeded CloudWatch log groups.
- [ ] Update tracker/resource-tracker.csv.
- [ ] Confirm no active resources remain in us-east-2.
