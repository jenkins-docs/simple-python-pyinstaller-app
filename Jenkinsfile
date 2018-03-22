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
        stage('Tests') {
            agent {
                docker {
                    image 'qnib/pytest'
                }
            }
            steps {
                sh 'pip install flask'
                sh 'py.test --verbose --junit-xml test-reports/results.xml sources/test_webapp.py || true'
            }
            post {
                always {
                    junit 'test-reports/results.xml'
                }
            }
        }
    }
}