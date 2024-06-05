pipeline {
    agent {
        kubernetes {
            label 'jenkins/jenkins-jenkins-agent'
            yamlfile 'jenkins-agent.yaml'
            defaultContainer 'ez-docker-helm-build'
        }
    }
    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    // Build Docker image
                    sh 'docker build -t ilaysb/final-project-1-flask_app:latest:${BRANCH_NAME} .'
                }
            }
    }
        
        stage('Run Unit Test') {
            steps {
                script {
                    // Run unit test (replace with your testing command)
                    sh '<your_testing_command>'
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
