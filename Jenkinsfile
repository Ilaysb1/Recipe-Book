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
            // label 'jenkins-agent'
            // yaml 'jenkins-agent.yaml'
            // defaultContainer 'ez-docker-helm-build'
        }
    }
    stages {
        stage('Build Docker Image') {
            // when {
            //     branch 'main'
            // }
            steps {
                container('ez-docker-helm-build') {
                    script {
                        // Build Docker image
                        sh 'docker build -t ilaysb/final-project-1-flask_app:latest:${BRANCH_NAME} .'
                    }
                }
            }
        }
        
        stage('Run Unit Test') {
            // when { 
            //     not {
            //         branch 'main'
            //     }
            }
            steps {
                script {
                    // Run unit test (replace with your testing command)
                    sh 'pytest'
                }
            }
        }

        stage('Build HELM Package') {
            steps {
                script {
                    // Change to the directory containing your Helm chart
                    dir('.') {
                        // Package application into a HELM chart
                        sh 'helm package .'
                    }
                }
            }
        }
    }
}
