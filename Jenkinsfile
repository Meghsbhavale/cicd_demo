pipeline {
    agent any

    environment {
        REGISTRY = "mgk8501"
        IMAGE = "flask-demo"
        SONARQUBE = "sonarqube"
    }

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/Meghsbhavale/cicd_demo.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh """
                python3 -m venv env
                source env/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                pip install pytest
                
                """
            }
        }

        stage('Run Unit Tests') {
            steps {
                sh """
                source env/bin/activate
                pytest --junitxml=results.xml
                """
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('sonarqube') {
                    sh """
                    sonar-scanner \
                      -Dsonar.projectKey=flask-demo \
                      -Dsonar.sources=. \
                      -Dsonar.python.coverage.reportPaths=coverage.xml
                    """
                }
            }
        }

        stage("Quality Gate") {
            steps {
                timeout(time: 2, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        stage('Docker Build') {
            steps {
                sh "docker build -t ${REGISTRY}/${IMAGE}:latest ."
            }
        }

        stage('Security Scan (Trivy)') {
            steps {
                sh """
                trivy image --exit-code 1 ${REGISTRY}/${IMAGE}:latest || true
                """
            }
        }

        stage('Docker Push') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub_login', usernameVariable: 'USER', passwordVariable: 'PASS')]) {
                    sh """
                    echo "$PASS" | docker login -u "$USER" --password-stdin
                    docker push ${REGISTRY}/${IMAGE}:latest
                    """
                }
            }
        }

        stage('Approve Deploy') {
            steps {
                input "Approve deployment to Kubernetes?"
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh "kubectl apply -f k8s/deployment.yaml"
            }
        }
    }
}
