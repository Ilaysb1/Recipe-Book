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
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }
        
        stage('Build and Push Docker Image') {
            when {
                branch 'main'
            }
            steps {
                container('ez-docker-helm-build') {
                    script {
                        // Build Docker image and tag it with the build number
                        sh "docker build -t ${DOCKER_IMAGE}:${env.BUILD_NUMBER} ."
                        // Push Docker image to Docker Hub with the build number tag
                        withCredentials([usernamePassword(credentialsId: 'docker_cred', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                            sh "docker login -u ${DOCKER_USERNAME} -p ${DOCKER_PASSWORD}"
                            sh "docker push ${DOCKER_IMAGE}:${env.BUILD_NUMBER}"
                        }
                        // Tag the image as 'latest' and push it
                        sh "docker tag ${DOCKER_IMAGE}:${env.BUILD_NUMBER} ${DOCKER_IMAGE}:latest"
                        sh "docker push ${DOCKER_IMAGE}:latest"
                    }
                }
            }
        }
        
        stage('Run Unit Test') {
            when {
                not {
                    branch 'main'
                }
            }
            steps {
                container('ez-docker-helm-build') {
                    script {
                        // Your unit test execution step here
                        sh "docker build -t test-image -f Dockerfile.test ."
                        sh "docker run --rm test-image"
                    }
                }
            }
        }

        stage('Merge Request') {
            when {
                not {
                    branch 'main'
                }
            }
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'github_cred', usernameVariable: 'GITHUB_USER', passwordVariable: 'GITHUB_PASSWORD')]) {
                        sh """
                        curl -X POST -u ${GITHUB_USER}:${GITHUB_PASSWORD} -d '{
                                "title": "Merge feature to main",
                                "head": "feature-finalproj-1",
                                "base": "main"
                            }' \
                            'https://api.github.com/repos/Ilaysb1/Recipe-Book/pulls'
                        """
                    }
                }
            }
        }
        
                stage('Trigger next update pipline') {
            when {
                branch 'main'
            }
            steps {
                build job: 'update', parameters: [string(name: 'DOCKERTAG', value: env.BUILD_NUMBER)]
            }
        }
    }
    
    post {
        success {
            script {
                if (env.BRANCH_NAME == 'main') {
                    // Add main branch specific actions here
                    // These actions will be executed after the merge request is approved
                }
            }
        }
    }
}
