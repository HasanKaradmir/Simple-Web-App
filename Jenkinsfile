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
        stage('Setup') {
            steps {
                script {
                    // Python ortamını kur ve gerekli paketleri yükle
                    sh 'python3 -m venv venv'
                    sh '. venv/bin/activate && pip install pylint flake8 ruff'
                    // Pylint ve Flake8 konfigürasyon dosyalarını oluştur
                    writeFile file: '.pylintrc', text: '''
[MESSAGES CONTROL]
disable=C0114,C0115,C0116
[BASIC]
good-names=i,j,k,ex,Run,_
                    '''
                    writeFile file: '.flake8', text: '''
[flake8]
ignore = E203, E266, E501, W503, F403, F401
max-line-length = 88
exclude = 
    .git,
    __pycache__,
    old,
    build,
    dist
                    '''
                }
            }
        }
        stage('Linting') {
            steps {
                script {
                    // pylint ile kod kalitesini kontrol et
                    sh 'ls'
                    sh '. venv/bin/activate && ruff check *.py'
                    // sh '. venv/bin/activate && pylint **/*.py'
                    // flake8 ile kod kalitesini kontrol et
                    // sh '. venv/bin/activate && flake8 .'
                }
            }
        }
        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} -f ./build/Dockerfile ."
                sh "docker build -t ${IMAGE_NAME}:latest -f ./build/Dockerfile ."
            }
        }
        stage('Analyze Image') {
            steps {
                // Install Docker Scout
                sh 'curl -sSfL https://raw.githubusercontent.com/docker/scout-cli/main/install.sh | sh -s -- -b .'
                // Analyze and fail on critical or high vulnerabilities
                sh "./docker-scout cves ${IMAGE_NAME}:latest --exit-code --only-severity critical"
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
        stage('Build Helm Package') {
            steps {
                sh """
                #!/bin/bash
                # Version Stage
                sed -i \'s/version: [0-9]\\+\\.[0-9]\\+\\.[0-9]\\+/version: ${IMAGE_TAG}/\' ./k8s/simple-webapp-helm/Chart.yaml
                helm package ./k8s/simple-webapp-helm
                helm push simple-webapp-helm-${IMAGE_TAG}.tgz oci://registry-1.docker.io/hasankarademir
                """
            }
        }
    }
    post {
        always {
            sh 'docker rmi -f $(docker images -aq) || true'
        }
        success {
            emailext body: 'Başarılı!!', subject: 'Success Simple Web App Pipeline', to: 'info@hasankaradmir.com'
        }
        unsuccessful {
            emailext body: 'Başarısız!!', subject: 'Failed Simple Web App Pipeline', to: 'info@hasankaradmir.com'
        }
    }
}
