pipeline {
    agent none
    stages {
        stage('Build') {
            agent {
                dockerContainer {
                    image 'jenkins/jnlp-agent-python3:latest'
                }
            }
            steps {
                sh 'python -m py_compile sources/add2vals.py sources/calc.py'
            }
        }
    }
}
