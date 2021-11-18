pipeline {
    agent none //1
    stages {
        stage('Build') { //2
            agent {
                docker {
                    image 'python:2-alpine' //3
                }
            }
            steps {
                sh 'python -m py_compile sources/add2vals.py sources/calc.py' //4
            }
        }
    }
}

