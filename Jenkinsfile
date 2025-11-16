pipeline {
    agent any

    environment {
        // 1. ALTERE: Substitua pelo seu usuário Docker Hub (ex: usuario_docker/rpdjango-test-build)
        IMAGE_NAME = 'mablemb/rpdjango-test-build' 
        // 2. ID da credencial que você criou no Jenkins
        DOCKER_CREDENTIAL_ID = 'docker-hub-credentials' 
    }

    stages {
        stage('Checkout Code') {
            steps {
                echo 'Getting code from SCM...'
            }
        }
        
        stage('Build Docker Image') {
            steps {
                echo 'Building Docker Image...'
                // A tag usa o ID da build do Jenkins para garantir que seja única
                sh "docker build --pull -t ${IMAGE_NAME}:${BUILD_ID} ."
            }
        }

        stage('Run Unit Tests') {
            steps {
                echo 'Running Django Unit Tests...'
                sh "docker run --rm ${IMAGE_NAME}:${BUILD_ID} python manage.py test"
            }
        }
        
        stage('Push Image to Registry') {
            steps {
                echo 'Tagging and Pushing Image to Registry...'
                // Este bloco 'withCredentials' injeta as credenciais do Jenkins
                withCredentials([usernamePassword(credentialsId: "${DOCKER_CREDENTIAL_ID}", usernameVariable: 'USER', passwordVariable: 'PASS')]) {
                    // 1. Autentica no Docker Hub (ou outro registro) usando o usuário e a senha injetados
                    sh "echo \$PASS | docker login -u \$USER --password-stdin"
                    
                    // 2. Envia a imagem para o Docker Hub
                    sh "docker push ${IMAGE_NAME}:${BUILD_ID}"
                    
                    // 3. Opcional: Envia a imagem com a tag 'latest' também
                    sh "docker tag ${IMAGE_NAME}:${BUILD_ID} ${IMAGE_NAME}:latest"
                    sh "docker push ${IMAGE_NAME}:latest"
                    
                    // 4. Boa prática: Limpa a sessão de login
                    sh "docker logout" 
                }
            }
        }

        stage('Deploy (Placeholder)') {
            steps {
                echo 'Next: Deploy to staging/production server.'
            }
        }

        stage('Merge main into homol') {
            when {
                expression { return env.BRANCH_NAME == 'main' }
            }
            steps {
                echo 'Merging main into homol...'
                sh '''
                    git config user.name "jenkins"
                    git config user.email "jenkins@local"

                    git fetch origin
                    git checkout homol
                    git merge --no-ff origin/main -m "Merge main into homol from Jenkins build ${BUILD_NUMBER}"
                    git push origin homol
                '''
            }
        }
    }
}