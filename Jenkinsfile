pipeline {
    agent any

    environment {
        AUTH_IMAGE = 'auth-service'
        ITEM_IMAGE = 'item-service'
        FRONTEND_IMAGE = 'frontend'
        REGISTRY = 'registry.example.com' # Replace with actual registry
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Auth Service') {
            steps {
                dir('services/auth-service') {
                    sh 'docker build -t ${AUTH_IMAGE}:latest .'
                }
            }
        }

        stage('Build Item Service') {
            steps {
                dir('services/item-service') {
                    sh 'docker build -t ${ITEM_IMAGE}:latest .'
                }
            }
        }

        stage('Build Frontend') {
            steps {
                dir('frontend') {
                    sh 'docker build -t ${FRONTEND_IMAGE}:latest .'
                }
            }
        }

        stage('Push Images') {
            steps {
                echo "Mocking push to registry..."
                // sh "docker tag ${AUTH_IMAGE}:latest ${REGISTRY}/${AUTH_IMAGE}:latest"
                // sh "docker push ${REGISTRY}/${AUTH_IMAGE}:latest"
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh 'kubectl apply -f k8s/'
            }
        }
    }
}
