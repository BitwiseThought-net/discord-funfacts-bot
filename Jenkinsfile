pipeline {
    agent any
//    environment {
//        REPO_URL = "${env.GIT_URL.replaceFirst(/^.*\/([^\/]+?).git$/, '$1')}"
//        REPO_NAME = "${env.REPO_URL.tokenize('/').last().split("\\.")[0]}"
//    }
    stages {
        stage('Setup Variables') {
            steps {
                script {
                    // Explicitly assign to the env object so withCredentials can see it
                    env.REPO_NAME = env.GIT_URL.tokenize('/').last().split("\\.")[0]
                }
            }
        }
/*
        stage('Test') {
            steps {
                script {
                    // Run tests and output results to a file named 'results.xml'
                    // We use || true so the pipeline doesn't crash before archiving the results if tests fail
                    sh 'pip install pytest pytest-cov && pytest --junitxml=results.xml --cov=lib --cov-report=xml:coverage.xml || true'
                }
            }
            post {
                always {
                    // This is the "magic" step that fills the Blue Ocean Tests tab
                    junit 'results.xml'
            
                    // This archives the coverage data (requires Cobertura or Code Coverage plugin)
                    archiveArtifacts artifacts: 'coverage.xml', fingerprint: true
                }
            }
        }
*/

        stage('Deploy') {
            steps {
                // This "binds" your secret file to a temporary variable (envFile)
                withCredentials([file(credentialsId: "${env.REPO_NAME}-env", variable: 'envFile')]) {
                    script {
                        sh "[ -f '${envFile}' ] && cp '${envFile}' .env"
                        sh "cp ${envFile} .env"
                        
                        sh '''if [ -f docker-compose.yml ]; then
                                docker compose up -d --build
                              else
                                exit 0
                              fi
                        '''
                        
                        // 3. Clean up the .env file after deployment (optional but safer)
                        sh "[ -f .env ] && rm .env"
                    }
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
