node {
    stage('Build') {
        steps {
            script {
                docker.image('python:2-alpine').inside {
                    sh 'python -m py_compile sources/add2vals.py sources/calc.py'
                    sh 'mkdir -p dist'
                    sh 'mv sources/add2vals.pyc dist/'
                }
            }
        }
    }

    stage('Test') {
        steps {
            script {
                docker.image('qnib/pytest').inside {
                    sh 'py.test --verbose --junit-xml test-reports/results.xml sources/test_calc.py'
                }
            }
        }
    }

    stage('Deploy') {
        steps {
            script {
                docker.image('python:2-alpine').inside {
                    input message: 'Sudah selesai menggunakan Python App? (Klik "Proceed" untuk mengakhiri)'
                }
            }
        }
        post {
            success {
                archiveArtifacts 'dist/'
            }
        }
    }
}
