pipeline {
    agent any

    stages {
        stage ("Build Docker Image and Tag") {
            steps {
                sh "docker build --tag crypto:latest ."
                sh "docker tag crypto:latest duckymomo20012/cryptohub:latest"
            }
        }
        stage ("Publish to Docker Hub") {
            steps {
                sh "docker push duckymomo20012/cryptohub:latest"
            }
        }
    }
}
