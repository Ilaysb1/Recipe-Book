pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = 'ilaysb/final-project-1-flask_app'
    }
    
    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    // Your Docker image build step here
                    sh "docker build -t ${DOCKER_IMAGE}:latest ."
                }
            }
        }
        
        stage('Run Unit Test') {
            steps {
                script {
                    // Your unit test execution step here
                    sh "pytest"
                }
            }
        }

        stage('Build HELM Package') {
            steps {
                script {
                    // Your HELM package build step here
                    dir('proj-helm') {
                        sh 'helm package .'
                    }
                }
            }
        }

        stage('Docker Push') {
            when {
                branch 'main'
            }
            steps {
                script {
                    // Your Docker image push step here
                    withCredentials([usernamePassword(credentialsId: 'docker_cred', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                        sh "docker login -u ${DOCKER_USERNAME} -p ${DOCKER_PASSWORD}"
                        sh "docker push ${DOCKER_IMAGE}:latest"
                    }
                }
            }
        }

        stage('HELM Push') {
            when{
                branch 'main'
            }
            steps {
                script {
                    // Your HELM package push step here
                    // Assuming you have a Docker registry set up for HELM charts
                    // Push the HELM package to the Docker registry
                    sh "helm push proj-helm-0.1.0.tgz docker.io/ilaysb/helm-charts"
                }
            }
        }
    }
    
    post {
        success {
            script {
                if (env.BRANCH_NAME == 'feature-finalproj-1') {
                    // Create a pull request to the main branch
                    // Using GitHub API or Jenkins pull request builder plugin
                    // Example: createPullRequest('main', 'feature-finalproj-1')
                }
            }
        }
    }
}
