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
                withDockerRegistry(credentialsId: "dockerhub", url: "") {
                    sh "docker push duckymomo20012/cryptohub:latest"
                }
            }
        }
        stage ("Deploy app to container") {
            steps {
                sh "docker run --name web-server --rm -dp 80:80 crypto:latest"
            }
        }
    }
}
