pipeline {
  agent none
  stages {
    stage('Build') {
      parallel {
        stage('Build-add2vals') {
          agent {
            docker {
              image 'python:2-alpine'
            }

          }
          steps {
            sh 'python -m py_compile sources/add2vals.py sources/calc.py'
          }
        }
        stage('Build-logfilemonitor') {
          agent {
            docker {
              image 'python:2-alpine'
            }

          }
          steps {
            sh 'python -m py_compile sources/LogfileMonitor.py'
          }
        }
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
      parallel {
        stage('Deliver-add2vals') {
          agent {
            docker {
              image 'richardx/pyinstaller-linux:python2'
            }

          }
          post {
            success {
              archiveArtifacts 'dist/add2vals'

            }

          }
          steps {
            sh 'pyinstaller --onefile sources/add2vals.py'
          }
        }
        stage('Delivery-logfilemonitor') {
          agent {
            docker {
              image 'richardx/pyinstaller-linux:python2'
            }

          }
          steps {
            sh 'pyinstaller --onefile sources/LogfileMonitor.py'
          }
        }
      }
    }
  }
}