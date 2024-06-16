pipeline {
    agent {
        kubernetes{
            label "recipes-project-agent"
            idleMinutes 5
            yamlFile 'build-pod.yaml'
            defaultContainer 'ez-docker-helm-build'
        }
    }

    
    environment {
        DOCKER_IMAGE = 'ilaysb/final-project-1-flask_app'
        GITHUB_REPO = 'Ilaysb1/Recipe-Book'
        GITHUB_API_URL = 'https://api.github.com'
        GITHUB_TOKEN = credentials('github_token')
    }
    
    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage("Build docker image"){
                    steps {
                        script {
                            dockerImage = docker.build("${DOCKER_IMAGE}:latest", "--no-cache .")
                            dockerImage2 = docker.build("${DOCKER_IMAGE}:${env.BUILD_NUMBER}", "--no-cache .")

                        }
                    }
                }

        stage('Push Docker image') {
                    when {
                        branch 'main'
                    }
                    steps {
                        script {
                            docker.withRegistry('https://registry.hub.docker.com', 'docker_cred') {
                                dockerImage.push("latest")
                                dockerImage2.push("${BUILD_NUMBER}")
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
                withCredentials([string(credentialsId: 'github_token', variable: 'GITHUB_TOKEN')]) {
                    script {
                        def branchName = env.BRANCH_NAME
                        def pullRequestTitle = "Merge ${branchName} into main"
                        def pullRequestBody = "Automatically generated merge request for branch ${branchName}"

                        sh """
                            curl -X POST -H "Authorization: token ${GITHUB_TOKEN}" \
                            -d '{ "title": "${pullRequestTitle}", "body": "${pullRequestBody}", "head": "${branchName}", "base": "main" }' \
                            ${GITHUB_API_URL}/repos/${GITHUB_REPO}/pulls
                        """
                    }
                }
            }
        }
    }
}
