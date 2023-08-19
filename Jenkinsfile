node {
    stage('Prepare Docker') {
        docker.image('docker:stable').inside('--privileged') {
        }
    }

    stage('Build') {
        docker.image('python:2-alpine').inside() {
            sh 'pwd'
            sh 'ls -la'
            sh 'python -m py_compile sources/add2vals.py sources/calc.py'
        }
    }

    stage('Test') {
        docker.image('qnib/pytest').inside() {
            sh 'py.test --verbose --junit-xml test-reports/results.xml sources/test_calc.py'
        }
    }
}
