pipeline {
    agent any
    stages {
        stage("Build") {
            steps {
                sh 'echo "Hello World"'
                sh '''
                    echo "Multiline shell steps work too"
                    ls -lah
                   '''
            }
        }
    }
}

pipeline {
    agent any
    stages {
        stage("Deploy") {
            steps {
                retry(3) {
                    sh './flakey-deploy.sh'
                }

                timeout(time: 3, unit: 'MINUTES') {
                    sh './health-check.sh'
                }
            }
        }
    }
}
