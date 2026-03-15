# Project Wiki: FastAPI React Auth CRUD

Welcome to the project wiki! This document provides an in-depth overview of the application's architecture, the tools involved, and how you can deploy and run it both locally and in a production-like environment.

## 1. Application Flow Diagram

The following diagram illustrates how a user request (such as a login or CRUD action) flows through the system's microservices.

```mermaid
sequenceDiagram
    participant User as User / Browser
    participant Frontend as React Frontend
    participant Auth as Auth Service (FastAPI)
    participant Item as Item Service (FastAPI)

    User->>Frontend: Accesses Application & Attempts Login
    Frontend->>Auth: POST /login (Credentials)
    
    alt Invalid Credentials
        Auth-->>Frontend: 401 Unauthorized
        Frontend-->>User: Display Error
    else Valid Credentials
        Auth-->>Frontend: 200 OK + JWT Access Token
        Frontend-->>User: Render Dashboard
    end

    User->>Frontend: Creates/Reads Items
    Frontend->>Item: HTTP Request (GET/POST/PUT/DELETE) + Auth Header (JWT)
    
    alt Invalid Token
        Item-->>Frontend: 401 Unauthorized
    else Valid Token
        Item-->>Frontend: 200/201 Success Response (JSON)
        Frontend-->>User: Display Data
    end
```

## 2. Tools & Tech Stack Diagram

This diagram visualizes the tools and technologies used to build, manage, and deploy the application.

```mermaid
block-beta
    columns 1
    
    block:T1
      columns 3
      User["User Client (Web Browser)"]
    end
    
    space
    
    block:T2
        columns 1
        App["Frontend Application"]
        React["React (UI Library)"]
        Vite["Vite (Bundler / Dev Server)"]
        Redux["Redux (State Management)"]
    end
    
    space
    
    block:T3
        columns 2
        AuthAPI["Auth Service"]
        ItemAPI["Item Service"]
        PyA["Python + FastAPI"]
        PyI["Python + FastAPI"]
        Pass["Passlib (OAuth2 / JWT)"]
        Pyd["Pydantic (Validation)"]
    end
    
    space
    
    block:T4
        columns 3
        DevOps["CI/CD & Deployment Strategy"]
        Docker["Docker (Containerization)"]
        K8s["Kubernetes (Orchestration)"]
        Jenkins["Jenkins (CI Pipeline)"]
    end

    T1 --> T2
    T2 --> T3
    T3 --> T4

    classDef tech fill:#f9f9f9,stroke:#333,stroke-width:2px;
    class React,Vite,Redux,PyA,PyI,Pass,Pyd,Docker,K8s,Jenkins tech;
```

---

## 3. Tool Directory Mapping

This diagram maps the primary tools and technologies explicitly to the directory structure where they are configured and utilized.

```mermaid
graph TD
    classDef dir fill:#e1f5fe,stroke:#03a9f4,stroke-width:2px,color:#000
    classDef tool fill:#f9f9f9,stroke:#333,stroke-width:1px,color:#333

    Root["📂 fastapi-react-auth-crud"]:::dir

    subgraph Frontend["Frontend Layer"]
        FE_Dir["📁 /frontend"]:::dir
        React["⚛️ React"]:::tool
        Redux["📦 Redux Toolkit"]:::tool
        TW["🎨 Tailwind CSS"]:::tool
        Vite["⚡ Vite"]:::tool
    end

    subgraph Backend["Backend Layer"]
        Services_Dir["📁 /services"]:::dir
        Auth_Dir["📁 /auth-service"]:::dir
        Item_Dir["📁 /item-service"]:::dir
        
        FA1["🚀 FastAPI"]:::tool
        FA2["🚀 FastAPI"]:::tool
        Sec["🛡️ Passlib & JWT"]:::tool
        Uvi1["▶️ Uvicorn"]:::tool
        Uvi2["▶️ Uvicorn"]:::tool
    end

    subgraph DevOps["DevOps & Infra"]
        K8s_Dir["📁 /k8s"]:::dir
        K8s["☸️ Kubernetes Manifests"]:::tool
        Docker_File["📄 docker-compose.yml"]:::dir
        Docker["🐳 Docker Compose"]:::tool
        Jenkins_File["📜 Jenkinsfile"]:::dir
        Jenkins["👨‍🍳 Jenkins Pipeline"]:::tool
    end

    Root --> Frontend
    Root --> Backend
    Root --> DevOps

    Frontend --- FE_Dir
    FE_Dir --> React
    FE_Dir --> Redux
    FE_Dir --> TW
    FE_Dir --> Vite

    Backend --- Services_Dir
    Services_Dir --> Auth_Dir
    Services_Dir --> Item_Dir

    Auth_Dir --> FA1
    Auth_Dir --> Sec
    Auth_Dir --> Uvi1

    Item_Dir --> FA2
    Item_Dir --> Uvi2
    
    DevOps --- K8s_Dir
    DevOps --- Docker_File
    DevOps --- Jenkins_File
    
    K8s_Dir --> K8s
    Docker_File --> Docker
    Jenkins_File --> Jenkins
```

---

## 4. How to Deploy and Run the Application

There are multiple ways to run and deploy this application depending on your needs. For development, `docker-compose` is highly recommended. For production equivalents, we provide Kubernetes manifests.

### Option A: Local Development (Docker Compose)

The easiest way to run the entire stack is using Docker Compose. Make sure [Docker](https://docs.docker.com/get-docker/) is running on your machine.

**Steps:**
1. Open a terminal in the root directory of the project.
2. Build and start the containers:
   ```bash
   docker-compose up --build
   ```
3. Wait for the containers to initialize.
4. The services are now available at:
   - **Frontend UI:** `http://localhost:5173`
   - **Auth Service:** `http://localhost:8001`
     - **Swagger UI (Docs):** `http://localhost:8001/docs`
   - **Item Service:** `http://localhost:8002`
     - **Swagger UI (Docs):** `http://localhost:8002/docs`

To stop the containers, press `Ctrl+C` or run:
```bash
docker-compose down
```

### Option B: Kubernetes Deployment (Minikube / Cluster)

The `/k8s` directory contains standard Kubernetes resources (Deployments, Services, and optionally an Ingress). Ensure you have a cluster running (e.g., Minikube).

**Steps:**
1. Ensure your Kubernetes cluster is running:
   ```bash
   minikube start
   ```
2. Build the Docker images inside your Kubernetes environment (if using Minikube):
   ```bash
   eval $(minikube docker-env)
   docker build -t frontend:latest ./frontend
   docker build -t auth-service:latest ./services/auth-service
   docker build -t item-service:latest ./services/item-service
   ```
3. Apply the Kubernetes configuration files:
   ```bash
   kubectl apply -f k8s/deployments.yaml
   kubectl apply -f k8s/services.yaml
   kubectl apply -f k8s/ingress.yaml
   ```
4. Check the status of your pods to ensure they are `Running`:
   ```bash
   kubectl get pods
   ```
5. You can port-forward the services or access them via the Ingress (if configured and supported by your cluster environment).

### Option C: Continuous Integration (Jenkins)

The project includes a `Jenkinsfile`. If you have a Jenkins server set up:
1. Create a new Pipeline project pointing to this repository.
2. The pipeline handles:
   - Defining parallel stages for Frontend and Backend API builds.
   - Pushing Docker images.
   - Setting up deployment to environments (configurable inside the script).
