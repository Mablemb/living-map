pipeline {
    agent any

    environment {
        // Define um nome para a imagem temporária
        IMAGE_NAME = 'rpdjango-test-build'
    }

    stages {
        stage('Checkout Code') {
            steps {
                echo 'Getting code from SCM...'
                // O Jenkins já faz o checkout, mas este stage é bom para clareza
            }
        }
        
        stage('Build Docker Image') {
            steps {
                echo 'Building Docker Image...'
                // Constrói a imagem usando a pasta do código que o Jenkins baixou
                // O --pull garante que a base (python:3.11-slim) esteja atualizada
                sh "docker build --pull -t ${IMAGE_NAME}:${BUILD_ID} ."
            }
        }

        stage('Run Unit Tests') {
            steps {
                echo 'Running Django Unit Tests...'
                // Roda os testes dentro de um container temporário
                // --rm: remove o container após a execução
                // O --volume é crucial para que os relatórios de teste possam ser acessados pelo Jenkins
                sh "docker run --rm ${IMAGE_NAME}:${BUILD_ID} python manage.py test"
            }
        }
    }
}