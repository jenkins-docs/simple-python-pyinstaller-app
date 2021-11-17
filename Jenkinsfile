pipeline {
    agent none //1
    stages {
        stage('Build') { //2
            agent {
                docker {
                    image 'python:2-alpine' //3
                }
            }
         stage('Test') {
            agent {
                docker {
                    image 'qnib/pytest'
                }
            }
            steps {
                sh 'py.test --verbose --junit-xml test-reports/results.xml sources/test_calc.py'
            }
            post {
                always {
                    junit 'test-reports/results.xml'
                }
            }
        }
    }
}

