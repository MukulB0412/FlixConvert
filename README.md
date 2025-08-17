# FlixConvert DevOps Pipeline (EKS)

This pack contains a **working CI/CD pipeline** to build your Flask app image and deploy it to **Amazon EKS** via GitHub Actions.

## Repo Layout
- `Dockerfile` – production-ready image with Gunicorn.
- `docker-compose.yml` – local dev.
- `k8s/` – Kubernetes manifests (Namespace, Secret, Deployment, Service, Ingress, HPA).
- `.github/workflows/cicd-eks.yml` – CI/CD to ECR → EKS.

## Local dev
```bash
docker compose up --build
# open http://localhost:8080
```

## Prereqs (one-time)
1. **Create EKS Cluster** and install NGINX Ingress Controller.
2. **Create ECR repo** (e.g., `flixconvert`).
3. **Set GitHub Secrets** in your repo:
   - `AWS_REGION` (e.g., ap-south-1)
   - `AWS_ROLE_ARN` (OIDC role with ECR push + EKS access) **or** `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` and update workflow to use them.
   - `ECR_REPOSITORY` (e.g., flixconvert)
   - `EKS_CLUSTER_NAME` (your cluster)
   - Optional: update `k8s/ingress.yaml` `host` to your domain.
   - Rotating runtime secret:
     - Update `k8s/secret.yaml` or manage via `kubectl create secret ...`

## First deploy (manual)
```bash
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/secret.yaml
# The workflow will replace image tag + apply the rest on push to main
```

## How CI/CD works
- On push to `main`, GitHub Actions:
  1. Builds Docker image from `Dockerfile`.
  2. Pushes to ECR (`${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPOSITORY}:<git-sha>`).
  3. Replaces the image reference in `k8s/deployment.yaml`.
  4. Applies manifests to your EKS cluster.
  5. Waits for rollout success.

## Notes
- The app reads `SECRET_KEY` from env; configured via K8s Secret.
- Ingress allows large uploads (`proxy-body-size: 500m`). Adjust if needed.
- HPA scales based on CPU > 70%.
