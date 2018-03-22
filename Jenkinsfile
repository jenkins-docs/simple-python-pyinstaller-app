pipeline{
    agent none
    stages {
        stage('Build') {
            agent {
                docker {
                    image 'python:2-alpine'
                }
            }
            steps {
                sh 'pip install flask'
                sh 'python -m py_compile sources/webapp.py'
            }
        }
    }
}