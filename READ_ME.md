## Assignment 3.1: Docker compose deployment

### Prerequisites
- Docker Desktop installed and running

### Deploy
```bash
docker compose up --build
```

### Access
- Application: http://localhost:8080
- Auth endpoints: http://localhost:8080/auth/
- Shortener endpoints: http://localhost:8080/

### Stop
```bash
docker compose down
```

Data persists across restarts via the `postgres_data` Docker volume.

## Assignment 3.2: Kubernetes deployment

### Prerequisites
- Docker images pushed to Docker Hub
- Access to the K8s cluster (SSH to 145.100.130.87)

### Push Docker images
```bash
docker build -t winst10/auth-service:latest ./auth_service
docker build -t winst10/shortening-service:latest ./shortening_service
docker push winst10/auth-service:latest
docker push winst10/shortening-service:latest
```

### Deploy to cluster
```bash
# SSH to control plane
ssh student087@145.100.130.87

# Apply all manifests
kubectl apply -f k8/

# Verify deployment
kubectl get pods -n url-shortener
kubectl get svc -n url-shortener
```

### Access
- Application: http://145.100.130.87:30080 (or any node IP)

## Testing

```bash
# Install test dependencies
pip install -r requirements.txt
# Run tests (requires services running on localhost:8080)
python test_app.py
```

## Architecture

```
┌─────────────┐     ┌─────────────────┐     ┌──────────────┐
│   Client    │────▶│  Nginx Proxy    │────▶│ Auth Service │
│             │     │   (port 8080)   │     │  (port 8001) │
└─────────────┘     │                 │     └──────┬───────┘
                    │                 │            │
                    │                 │     ┌──────▼───────┐
                    │                 │────▶│  Shortener   │
                    │                 │     │  (port 8000) │
                    └─────────────────┘     └──────┬───────┘
                                                   │
                                            ┌──────▼───────┐
                                            │  PostgreSQL  │
                                            │  (port 5432) │
                                            └──────────────┘