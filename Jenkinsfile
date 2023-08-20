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
            message: 'Sudah selesai menggunakan Python App? (Klik "Proceed" untuk mengakhiri)',
            submitterParameter: 'proceed'
        )
    }
    stage('Deploy') {
        script {
            if (userInput == 'proceed') {
                docker.image('python:2-alpine').inside {
                    archiveArtifacts artifacts: 'dist/*', allowEmptyArchive: true
                }
            }
        }
    }
}
