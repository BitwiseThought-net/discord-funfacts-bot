pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                // Jenkins automatically clones the repo here
                checkout scm
            }
        }

        stage('Deploy to Host') {
            steps {
                script {
                    // This runs on the host because of your /var/run/docker.sock mapping
                    // '--build' ensures it picks up new code changes
                    //sh 'docker compose up -d --build'
                    //sh 'cd /deploy/discord-terminal-bot && docker compose up -d --build'
                    sh 'cd /deploy/discord-terminal-bot && commands/build.sh'
                }
            }
        }
    }

    post {
        success {
            echo 'Deployment successful!'
        }
        failure {
            echo 'Deployment failed. Check the logs.'
        }
    }
}
