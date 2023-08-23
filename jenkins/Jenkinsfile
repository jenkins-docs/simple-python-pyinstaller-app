node {
    stage('Build') {
        docker.image('python:2-alpine').inside {
            sh 'python -m py_compile sources/add2vals.py sources/calc.py'
            sh 'mkdir -p dist'
            sh 'mv sources/add2vals.pyc dist/'
        }
    }

    stage('Test') {
        docker.image('qnib/pytest').inside {
            sh 'py.test --verbose --junit-xml test-reports/results.xml sources/test_calc.py'
        }
        step([$class: 'JUnitResultArchiver', testResults: 'test-reports/results.xml'])
    }

    stage('Manual Approval') {
        userInput = input(
            message: 'Lanjutkan ke tahap Deploy? (Klik "Proceed" untuk melanjutkan or "Abort" untuk mengakhiri)',
            submitterParameter: 'proceed'
        )
    }
    stage('Deploy') {
        docker.image('python:2-alpine').inside {
            archiveArtifacts artifacts: 'dist/*', allowEmptyArchive: false
        }
    }
}
