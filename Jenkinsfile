node {
    stage('Prepare Docker') {
        docker.image('docker:stable').inside('--privileged -v /var/run/docker.sock:/var/run/docker.sock') {
        }
    }

    stage('Build') {
        docker.image('python:2-alpine').inside('-v /var/run/docker.sock:/var/run/docker.sock') {
            sh 'python -m py_compile sources/add2vals.py sources/calc.py'
        }
    }

    stage('Test') {
        docker.image('qnib/pytest').inside('-v /var/run/docker.sock:/var/run/docker.sock') {
            sh 'py.test --verbose --junit-xml test-reports/results.xml sources/test_calc.py'
        }
    }

    stage('Deliver') {
        docker.image('cdrx/pyinstaller-linux:python2').inside('-v /var/run/docker.sock:/var/run/docker.sock') {
            sh 'pyinstaller --onefile sources/add2vals.py'
        }
        post {
            success {
                archiveArtifacts 'dist/add2vals'
            }
        }
    }
        post {
            always {
                junit 'test-reports/results.xml'
            }
        }
}
