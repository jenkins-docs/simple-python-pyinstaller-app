node {
    stage('Build') {
        docker.image('docker:stable').inside('-v /var/run/docker.sock:/var/run/docker.sock') {
            sh 'docker run --rm -v $(pwd):/app -w /app python:2-alpine python -m py_compile sources/add2vals.py sources/calc.py'
        }
    }
    
    stage('Test') {
        docker.image('docker:stable').inside('-v /var/run/docker.sock:/var/run/docker.sock') {
            sh 'docker run --rm -v $(pwd):/app -w /app qnib/pytest py.test --verbose --junit-xml test-reports/results.xml sources/test_calc.py'
        }
        post {
            always {
                junit 'test-reports/results.xml'
            }
        }
    }
    
    stage('Deliver') {
        docker.image('docker:stable').inside('-v /var/run/docker.sock:/var/run/docker.sock') {
            sh 'docker run --rm -v $(pwd):/app -w /app cdrx/pyinstaller-linux:python2 pyinstaller --onefile sources/add2vals.py'
        }
        post {
            success {
                archiveArtifacts 'dist/add2vals'
            }
        }
    }
}
