# Simple Web Application (https://simple-webapp.hasankaradmir.com/)

Bu proje, Python kullanılarak geliştirilmiş basit bir web uygulamasını içermektedir. Proje, Docker kullanarak containerize edilmiştir ve RKE2 üzerinde çalışan bir Kubernetes cluster'ına deploy edilmiştir. Jenkins ile CI/CD pipeline'ı oluşturulmuş ve ArgoCD ile continuous deployment sağlanmıştır.

## İçindekiler
- [Kurulum](#kurulum)
- [Docker Kullanımı](#docker-kullanımı)
- [Kubernetes Deploy](#kubernetes-deploy)
- [CI/CD Pipeline](#cicd-pipeline)
- [ArgoCD Kullanımı](#argocd-kullanımı)
- [İletişim](#iletişim)

## Kurulum

### Gerekli Bağımlılıklar

- Python 3.12
- Docker
- Kubernetes (RKE2)
- Jenkins
- ArgoCD (opsiyonel)

### Proje Dosyaları

- `main.py` : Web uygulamasının ana kodu
- `Dockerfile` : Docker imajını oluşturmak için kullanılan dosya
- `Jenkinsfile` : CI/CD pipeline tanımı
- `k8s` : Kubernetes manifest dosyaları ve Helm chartları

## Docker Kullanımı

### Docker İmajı Oluşturma

Docker imajını oluşturmak için aşağıdaki adımları izleyin:

1. Docker imajını oluşturun:
    ```sh
    docker build -t simple-web-app:latest -f ./build/Dockerfile .
    ```

2. Docker imajını çalıştırın:
    ```sh
    docker run -p 8000:8000 simple-web-app:latest
    ```

## Kubernetes Deploy

Kubernetes cluster'ınızı RKE2 ile kurduktan sonra, web uygulamasını deploy etmek için aşağıdaki adımları izleyin:

1. Kubernetes manifest dosyalarını kullanarak deploy edin:
    ```sh
    kubectl apply -f ./k8s/manifests/*
    ```

2. Helm chart kullanarak deploy edin:
    ```sh
    helm install simple-web-app ./k8s/simple-webapp-helm
    ```

## CI/CD Pipeline

CI/CD pipeline'ı Jenkins kullanarak kurmak için aşağıdaki adımları izleyin:

1. Jenkins'i sanal makinenize kurun.
2. `Jenkinsfile` dosyasını kullanarak pipeline'ı oluşturun.

Pipeline adımları:
- Workspace temizleme
- Git deposundan kod çekme
- Docker imajı oluşturma
- Docker imajinın güvenlik taramasının yapılması
- Docker imajını DockerHub'a push etme
- Helm package oluşturma ve push etme

```groovy
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
                // Analyze and fail on critical vulnerabilities
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
                sed -i \'s/version: [0-9]\\+\\.[0-9]\\+\\.[0-9]\\+/version: ${IMAGE_TAG}/\' ./k8s/simple-webapp-helm/Chart.yaml
                helm package simple-webapp-helm
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
```
## ArgoCD Kullanımı
ArgoCD'yi kullanarak continuous deployment sağlamak için aşağıdaki adımları izleyin:

1. ArgoCD'yi Kubernetes cluster'ınıza kurun.
2. ArgoCD konfigürasyon dosyalarını aşağıdaki gibi oluşturun ve deploy edin.
3. Uygulamanızın kodunu push ettiğinizde ArgoCD otomatik olarak deploy işlemini gerçekleştirecektir.

```yaml
project: default
source:
  repoURL: registry-1.docker.io/hasankarademir
  targetRevision: ' 1.0.0-20'
  chart: simple-webapp-helm
destination:
  server: 'https://kubernetes.default.svc'
  namespace: simple-webapp
syncPolicy:
  automated: {}
```

## İletişim
Herhangi bir sorunuz veya geri bildiriminiz için info@hasankaradmir.com adresinden iletişime geçebilirsiniz.