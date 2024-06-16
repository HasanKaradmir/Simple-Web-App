pipeline {
    agent any
    environment {
        APP_NAME = 'simple-web-app'
        RELEASE = '1.0.0'
        DOCKER_USER = 'hasankarademir'
        DOCKER_PASS = 'dockerhub'
        IMAGE_NAME = "${DOCKER_USER}" + '/' + "${APP_NAME}"
        IMAGE_TAG = "${RELEASE}-${BUILD_NUMBER}"

        DOCKER_HUB = credentials('dockerhub')
    }
    stages {
        stage('Clean Workspace') {
            steps {
                cleanWs()
            }
        }
        stage('Git Checkout') {
            steps {
                git changelog: false, credentialsId: 'github_cred', poll: false, url: 'https://github.com/HasanKaradmir/Simple-Web-App.git'
            }
        }
        stage('Docker Build') {
            steps {
                sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} -f ./build/Dockerfile ."
                sh "docker build -t ${IMAGE_NAME}:latest -f ./build/Dockerfile ."
            }
        }
        stage('Push Docker Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub', passwordVariable: 'passwordVariable', usernameVariable: 'usernameVariable')]) {
                    sh "echo ${passwordVariable} | docker login -u ${usernameVariable} --password-stdin"
                    sh "docker push ${IMAGE_NAME}:${IMAGE_TAG}"
                    sh "docker push ${IMAGE_NAME}:latest"
                }
            }
        }
        stage('Analyze image') {
            steps {
                // Install Docker Scout
                sh 'curl -sSfL https://raw.githubusercontent.com/docker/scout-cli/main/install.sh | sh -s -- -b /bin'
                sh 'hostname && whoami'

                // Analyze and fail on critical or high vulnerabilities
                sh "docker-scout cves ${IMAGE_NAME}:latest --exit-code --only-severity critical,high"
            }
        }
    }
}
