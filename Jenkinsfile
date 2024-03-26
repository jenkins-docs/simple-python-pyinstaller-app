pipeline {
    agent {
        docker { image 'python:2-alpine' }
    }
    stages {
        stage('Build') { 
            steps {
                sh 'python -m py_compile sources/add2vals.py sources/calc.py' 
                stash(name: 'compiled-results', includes: 'sources/*.py*') 
            }
        }
    }
}
stage('Deliver') {
    agent {
        docker {
            image 'cdrx/pyinstaller-linux:python2'
        }
    }
    steps {
        sh '/root/.pyenv/shims/pyinstaller --onefile sources/add2vals.py'
    }
    post {
        success {
            archiveArtifacts 'dist/add2vals'
        }
    }
}
