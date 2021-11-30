pipeline {
    agent none 
    stages {

        stage('FindHTTPCalls') {
            agent {
                docker {
                    image 'alpine:3.14'  
                }
            }
            environment {
                HTTPCALLS = """${sh(
                        returnStdout: true,
                        script: 'find ./sources -path "*.py" -exec grep -H -e "http://" {} \\;'
                    )}"""
            }
            steps {
                script {
                    if (env.HTTPCALLS?.trim()) {
                        currentBuild.result = 'ABORTED'
                        error("Aborting the build for http calls.")
                    }
                    
                }
            }
        }

        stage('Build') { 
            agent {
                docker {
                    image 'python:2-alpine' 
                }
            }
            steps {
                sh 'python -m py_compile sources/add2vals.py sources/calc.py' 
                stash(name: 'compiled-results', includes: 'sources/*.py*') 
            }
        }


        stage('Test') {
            agent {
                docker {
                    image 'qnib/pytest'
                }
            }
            steps {
                sh 'py.test --junit-xml test-reports/results.xml sources/test_calc.py'
            }
            post {
                always {
                    junit 'test-reports/results.xml'
                }
            }
        }


        stage('Deliver') {
            agent any
            environment {
                VOLUME = '$(pwd)/sources:/src'
                IMAGE = 'cdrx/pyinstaller-linux:python2'
            }
            steps {
                dir(path: env.BUILD_ID) {
                    unstash(name: 'compiled-results')
                    sh "docker run --rm -v ${VOLUME} ${IMAGE} 'pyinstaller -F add2vals.py'"
                }
            }
            post {
                success {
                    archiveArtifacts "${env.BUILD_ID}/sources/dist/add2vals"
                    sh "docker run --rm -v ${VOLUME} ${IMAGE} 'rm -rf build dist'"
                }
            }
        }


    }

}