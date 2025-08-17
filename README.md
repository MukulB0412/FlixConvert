# FlixConvert 🚀
A lightweight, web-based document converter built with Flask and Docker, containerized and orchestrated on Kubernetes (Minikube).

## Features ✨
- Convert PDF ↔ Word (DOCX) seamlessly
- Web UI built with Flask + Bootstrap
- Containerized with Docker (multi-stage build)
- Deployment-ready on Kubernetes with Ingress + Services
- Local DNS (.local) support on Arch Linux

## Screenshots 🖼️
![Homepage](docs/screenshots/home.png)
![PDF to DOCX](docs/screenshots/pdf-to-docx.png)
![Features](docs/screenshots/features.png)

## Tech Stack ⚙️
- **Backend**: Python (Flask)
- **Frontend**: HTML, Bootstrap
- **Containerization**: Docker (multi-stage)
- **Orchestration**: Kubernetes (Minikube, Ingress, Services)
- **Storage**: PVC for file persistence

## Setup 🚀

### 1. Clone repo
```bash
git clone https://github.com/your-username/flixconvert.git
cd flixconvert
```

### 2. Run with Docker
```bash
docker build -t flixconvert .
docker run -p 5000:5000 flixconvert
```

### 3. Deploy on Kubernetes (Minikube)
```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/ingress.yaml
```

### 4. Add local DNS entry (Arch Linux fix)
Edit `/etc/nsswitch.conf` and change hosts line:
```
hosts: files dns mymachines myhostname
```
Then update `/etc/hosts`:
```
192.168.58.2   flixconvert.local
```

Access app → `http://flixconvert.local` 🎉

## Troubleshooting 🛠️
- `flixconvert.local not found` → check `/etc/nsswitch.conf` order
- Ingress not working → verify `minikube addons enable ingress`
- Debug → `kubectl describe ingress flixconvert-ingress -n flixconvert`

## License 📄
MIT License.
