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
    stages {
        stage('Build Docker Image') {
            steps {
                container('ez-docker-helm-build') {
                    script {
                        sh 'docker build -t ilaysb/final-project-1-flask_app:latest .'
                    }
                }
            }
        }
        
        stage('Run Unit Test') {
            steps {
                script {
                    sh 'pytest'
                }
            }
        }

        stage('Build HELM Package') {
            steps {
                script {
                    dir('.') {
                        sh 'helm package .'
                    }
                }
            }
        }
    }
}
