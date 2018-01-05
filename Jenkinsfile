pipeline {
  agent {
    docker {
      image 'python:2-alpine'
    }
    
  }
  stages {
    stage('build') {
      steps {
        sh 'echo "hi"'
      }
    }
  }
}