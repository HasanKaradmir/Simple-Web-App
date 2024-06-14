pipeline {
    agent any
    environment {
        APP_NAME = "simple-web-app"
        RELEASE = "1.0.0"
        DOCKER_USER = "HasanKarademir"
        DOCKER_PASS = 'dockerhub'
        IMAGE_NAME = "${DOCKER_USER}" + "/" + "${APP_NAME}"
        IMAGE_TAG = "${RELEASE}-${BUILD_NUMBER}"
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
                docker build . --tag ${IMAGE_NAME}:${IMAGE_TAG}
            }
        }
    }
}
