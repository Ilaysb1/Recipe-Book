pipeline {
    agent {
        kubernetes {
            yaml '''
apiVersion: v1
kind: Pod
metadata:
  name: jenkins-agent
spec:
  containers:
  - name: ez-docker-helm-build
    image: ezezeasy/ez-docker-helm-build:1.41
    imagePullPolicy: Always
    securityContext:
      privileged: true
'''
        }
    }
    environment {
        DOCKER_IMAGE = 'ilaysb/final-project-1-flask_app'
    }
    
    stages {
        stage('Build Docker Image') {
            steps {
                container('ez-docker-helm-build') {
                    script {
                        sh "docker build -t ${DOCKER_IMAGE}:latest ."
                    }
                }
            }
        }
        
        stage('Run Unit Test') {
            steps {
                container('ez-docker-helm-build') {
                    script {
                        // Build and run tests using Dockerfile.test
                        sh "docker build -t test-image -f Dockerfile.test ."
                        sh "docker run --rm test-image"
                    }
                }
            }
        }

        stage('Build HELM Package') {
            steps {
                container('ez-docker-helm-build') {
                    script {
                        dir('proj-helm') {
                            sh 'helm package .'
                        }
                    }
                }
            }
        }

        stage('Push Docker Image') {
            when {
                branch 'main'
            }
            steps {
                container('ez-docker-helm-build') {
                    script {
                        // Authenticate with Docker Hub using Docker credentials
                        withCredentials([usernamePassword(credentialsId: 'docker_cred', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                            sh "docker login -u ${DOCKER_USERNAME} -p ${DOCKER_PASSWORD}"
                            sh "docker push ${DOCKER_IMAGE}:latest"
                        }
                    }
                }
            }
        }
    }
}