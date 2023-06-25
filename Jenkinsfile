node {
    stage('Build') {
        docker {
            image 'python:2-alpine'
            stage('Build') {
                sh 'python -m py_compile sources/add2vals.py sources/calc.py'
            }
        }
    }
    
    stage('Test') {
        docker {
            image 'qnib/pytest'
            stage('Test') {
                sh 'py.test --verbose --junit-xml test-reports/results.xml sources/test_calc.py'
            }
            post {
                always {
                    junit 'test-reports/results.xml'
                }
            }
        }
    }
    
    stage('Deliver') {
        docker {
            image 'cdrx/pyinstaller-linux:python2'
            stage('Deliver') {
                sh 'pyinstaller --onefile sources/add2vals.py'
            }
            post {
                success {
                    archiveArtifacts 'dist/add2vals'
                }
            }
        }
    }
}
