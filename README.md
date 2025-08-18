
# Flixconvert - PDF ↔ Word Converter (DevOps Project)

## Overview
Flixconvert is a web application that allows users to convert PDF files to Word documents and vice versa. 
We built it while learning DevOps concepts, and this README explains the entire journey from **A → Z**.

---

## 1. Idea & App
- Goal: Create a website to **convert PDF ↔ Word**.
- Tech Stack:
  - Frontend: Simple HTML/JavaScript upload page.
  - Backend: Python (FastAPI/Flask).
  - Libraries: python-docx, pdf2docx, etc.
- Flow: User uploads a file → backend converts → download link returned.

---

## 2. Local Development
- Wrote FastAPI routes:
  - `/upload` → Accept file.
  - `/convert` → Perform conversion.
  - `/download/{id}` → Download converted file.
- Ran locally using:
  ```bash
  uvicorn main:app --reload
  ```

---

## 3. Dockerization
- Created a **Dockerfile** with multi-stage builds.
- Installed dependencies inside container.
- Commands used:
  ```bash
  docker build -t flixconvert .
  docker run -p 8000:8000 flixconvert
  ```

---

## 4. Docker Compose (Optional)
- Defined `docker-compose.yml` to run multiple services together:
  - App container (flixconvert).
  - Redis/MinIO for jobs & storage (future scaling).

---

## 5. Kubernetes Deployment
- Wrote manifests inside `k8s/` folder:
  - `deployment.yaml` → Runs pods.
  - `service.yaml` → Exposes pods.
  - `ingress.yaml` → Configures routing.
  - `configmap.yaml` / `secret.yaml` → For configs.
- Applied with:
  ```bash
  kubectl apply -f k8s/ -n flixconvert
  ```

---

## 6. Ingress Setup
- Installed **NGINX Ingress Controller** in the cluster.
- Created Ingress for host `flix.local` → backend service.
- Faced validation errors, debugged cluster networking.

---

## 7. GitHub & CI/CD
- Pushed repo to **GitHub**.
- Set up **GitHub Actions** workflow:
  - On push → Build Docker image → Push to GHCR.
  - Planned Trivy scanning for vulnerabilities.
- Future: Deploy via ArgoCD.

---

## 8. Documentation
- Added screenshots + pipeline explanation in README.md.
- Attempted making README downloadable as PDF.

---

## 9. Issues Faced
- SSH push blocked on college WiFi → worked on hotspot.
- Python venv confusion (3.11 vs 3.13).
- Kubernetes Ingress validation issue.

---

## Current Status ✅
- App works locally + Docker.
- Kubernetes manifests created.
- GitHub repo + CI/CD pipeline drafted.
- Ingress partially working.

---

## Next Steps 🚀
1. Finish CI/CD pipeline (GitHub Actions → Deploy to cluster).
2. Add monitoring/logging (Prometheus + Grafana).
3. Fix ingress & use a domain (local `/etc/hosts`).
4. Extend app with worker queues + MinIO storage.

---

## Credits
This project was built as part of DevOps learning journey.
