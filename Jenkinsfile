pipeline {
    agent any
    stages {

        stage('Build') {
            steps {
                echo 'Building'
            }
        }
    
        stage('Test') {
            steps {
                echo 'Testing'
            }
        }
        stage('Deploy - Staging') {
            steps {
                sh './deploy staging'
                sh './run-smoke-tests'
            }
        }
        stage('Deploy - Production') {
            steps {
                sh './deploy production'
            }
        }   
     }
}
