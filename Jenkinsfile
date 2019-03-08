pipeline {
  agent none
  stages {
    stage('Build') {
      agent {
        docker {
          image 'python:2-alpine'
        }

      }
      steps {
        sh 'python -m py_compile sources/add2vals.py sources/calc.py sources/LogfileMonitor.py'
      }
    }
    stage('Test') {
      agent {
        docker {
          image 'richardx/pytest'
        }

      }
      post {
        always {
          junit 'test-reports/results.xml'

        }

      }
      steps {
        sh 'py.test --verbose --junit-xml test-reports/results.xml sources/test_calc.py'
      }
    }
    stage('Deliver') {
      agent {
        docker {
          image 'richardx/pyinstaller-linux:python2'
        }

      }
      post {
        success {
          archiveArtifacts 'dist/add2vals dist/LogfileMonitor'

        }

      }
      steps {
        sh 'pyinstaller --onefile sources/add2vals.py'
        sh 'pyinstaller --onefile sources/LogfileMonitor.py'
      }
    }
  }
}
