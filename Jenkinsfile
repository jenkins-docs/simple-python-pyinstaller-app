pipeline {
    agent none
    stages {
        stage('Build') {
            agent {
                docker {
                    image ''
                }
            }
            steps {
                sh ''
            }
        }
        stage('Test') { 
            agent {
                docker {
                    image '' 
                }
            }
            steps {
                sh '' 
            }
            post {
                always {
                    junit '' 
                }
            }
        }
    }
}
