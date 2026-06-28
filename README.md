# Distributed Systems - Voting App (Kubernetes)

## Project Description

This project is a simple voting/polling web application.

It consists of three main components:

- **Frontend**: Vite/React-based user interface
- **Backend**: FastAPI REST API service
- **Database**: PostgreSQL for persistent data storage

The entire system is containerized and deployed using **Kubernetes (Docker Desktop Cluster)**

---

## Architecture

The system follows a microservice-based architecture:

            Frontend (Vite / React)
                        | HTTP (REST API)
                        V
                Backend (Fast API)
                        | SQL
                        V
            PostgreSQL Database (PVC)

###  Components
- **Frontend**
    - Provides UI for creating and voting on polls
    - Communicates with backend via REST API
    - Exposed via Kubernetes NodePort

- **Backend**
    - FastAPI-based REST service
    - Handles business logic and API endpoints
    - Connects to PostgreSQL using Kubernetes service DNS (`postgres`)

- **PostgreSQL**
    - Persistent database instance
    - Uses a PersistentVolumeClaim (PVC)
    - Data survives pod restarts

---

## Prerequisites

Make sure the following tools are installed:

- Docker Desktop (with Kubernetes enabled)
- kubectl CLI
- Git

### Important Kubernetes Context

Ensure Docker Desktop Kubernetes is active:

```bash
    kubectl config current-context
```

Expected output:

```bash
    docker-desktop
```

If not, switch context:

```bash
    kubectl config use-context docker-desktop
```

### Docker Images Requirement

Before deploying to Kubernetes, the required images must exist locally:
- voting-backend:latest
- voting-frontend:latest

Build them if necessary:

```bash
    docker build -t voting-backend:latest ./backend
    docker build -t voting-frontend:latest ./frontend
```

These images are used directly by Kubernetes (local image runtime via Docker Desktop)

---

## Running the Application (Kubernetes)

### 1. Clone the repository

```bash
    git clone <repository-url>
    cd verteilte-Systeme-SoSe-2026
```

### 2. Deploy everything to Kubernetes

All services are deployed using Kubernetes manifests:

```bash
    kubectl apply -f k8s/
```

This will create:
- PostgreSQL Deployment + Service + PVC
- Backend Deployment + Service
- Frontend Deployment + Service (NodePort)

### 3. Check deployment status

```bash
    kubectl get pods
    kubectl get services
```

All pods should be in `Running` state.

## Accessing the Application

### Frontend

`http://localhost:30080`

### Backend (optional via port-forward)

```bash
    kubectl port-forward service/backend 8000:8000
```

Then access:
`http://localhost:8000/docs`

## Functionality

Once deployed, the application supports:
- Creating polls
- Viewing polls
- Voting on polls
All data is persisted in PostgreSQL

## Database & Persistence

PostgreSQL uses:
- PersistentVolumeClaim (`postgres-pvc`)
- Persistent storage across pod restarts
No local database installation is required.

## Configuration

Backend configuration is handled via Kubernetes ConfigMap:

- `DATABASE_URL` -> PostgreSQL connection string
- `CORS_ORIGINS` -> allowed frontend origins

Example:
```bash
    postgresql://postgres:postgres@postgres:5432/voting
```

## Cors Configuration

The backend allows frontend access via:
```bash
    http://localhost:5173
    http://localhost:30080
```

## Containerization

Each service is containerized:
- **Backend**: Python + FastAPI (Dockerfile in `/backend`)
- **Frontend**: React + Vite (Dockerfile in `/frontend`)
- **Database**: Official PostgreSQL image
Images are built locally or preloaded into Docker Desktop Kubernetes

## Redeployment / Updates

If changes are made to Kubernetes manifests:
```bash
    kubectl apply -f k8s/
    kubectl rollout restart deployment backend
    kubectl rollout restart deployment frontend
```

## Notes

- Backend connects to PostgreSQL via Kubernetes DNS (`postgres`)
- No external database setup is required
- Fully containerized distributed system
- `kubectl port-forward` can be used for debugging