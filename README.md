# FlixConvert

FlixConvert is a sleek and powerful web application designed to convert
**PDF → Word (DOCX)** and **Images → PDF** with a Netflix-inspired
cinematic interface.\
It combines **privacy-first file conversion** with **smooth
animations**, **mobile-ready UI**, and **buttery scrolling experience**.

------------------------------------------------------------------------

## 📸 Website Screenshots

### Landing Page

![Landing Page](Screenshot_20250817_173131.png)

### PDF to DOCX Converter

![PDF to DOCX Converter](Screenshot_20250817_173135.png)

### How It Works & FAQ

![How It Works](a0085e56-2865-44c5-a517-7da6d2e1cdee.png)

------------------------------------------------------------------------

## 🚀 Features

-   **Privacy-Friendly** → Files are processed securely and never stored
    permanently.\
-   **Netflix Vibes** → Smooth gradients, frosted cards, and cinematic
    feel.\
-   **Flexible Layouts** → Convert PDFs and arrange images in
    rows/columns.\
-   **Mobile Ready** → Fully responsive with drag & drop reorder
    support.

------------------------------------------------------------------------

## ⚙️ How It Works

1.  Upload your PDF or images directly from your computer (drag & drop
    supported).\
2.  Select layout, formatting, page orientation, and custom options.\
3.  Click **Convert** → in seconds your output file is ready for
    download.

------------------------------------------------------------------------

## 🛠 DevOps Pipeline

Our **end-to-end CI/CD pipeline** ensures smooth and automated delivery:

### 1️⃣ Source Code Management

-   Hosted on **GitHub** with branching strategy (`main`, `dev`,
    `feature/*`).\
-   Pull requests undergo mandatory **code reviews**.

### 2️⃣ CI/CD with GitHub Actions

-   On every push/pull request:
    -   **Linting & Testing**: Python/Node.js code is checked with
        linters & unit tests.\
    -   **Docker Build**: Application containerized with multi-stage
        Dockerfile.\
    -   **Image Push**: Built image pushed to Docker Hub.

### 3️⃣ Containerization

-   **Dockerfile** optimized with multi-stage builds to reduce image
    size.\
-   Used **.dockerignore** to exclude unnecessary files.

### 4️⃣ Kubernetes Deployment

-   **Deployment.yaml** → Defines replicas & rolling updates.\
-   **Service.yaml** → Exposes app inside cluster.\
-   **Ingress.yaml** → Provides external access with NGINX ingress
    controller.\
-   **ConfigMap & Secrets** → Manage environment configs securely.\
-   **Persistent Volumes (PVCs)** for file handling (uploads & converted
    files).

### 5️⃣ Monitoring & Logging

-   **Prometheus + Grafana** → Metrics and dashboards.\
-   **ELK Stack (Elasticsearch, Logstash, Kibana)** → Centralized logs.

### 6️⃣ Cloud Hosting

-   Runs on **AWS EKS (Elastic Kubernetes Service)**.\
-   Auto-scaled with **Horizontal Pod Autoscaler (HPA)**.\
-   File storage backed by **AWS S3** for durability.

### 7️⃣ Security

-   HTTPS enforced with **Let's Encrypt TLS Certificates**.\
-   Secrets managed via **Kubernetes Secrets** + **AWS Secret
    Manager**.\
-   Image scanning with **Trivy**.

------------------------------------------------------------------------

## 📦 Tech Stack

-   **Frontend**: React + TailwindCSS\
-   **Backend**: FastAPI (Python)\
-   **Containerization**: Docker\
-   **Orchestration**: Kubernetes (EKS)\
-   **CI/CD**: GitHub Actions\
-   **Monitoring**: Prometheus, Grafana, ELK\
-   **Storage**: AWS S3 + PVC

------------------------------------------------------------------------

## 📞 Contact Information

-   **Email**: 0412mukul@gmail.com\
-   **Phone**: +91-9810495144\
-   **Address**: 993/p-sf, Sector-10, Gurugram, Haryana 122001

------------------------------------------------------------------------

© 2025 FlixConvert
