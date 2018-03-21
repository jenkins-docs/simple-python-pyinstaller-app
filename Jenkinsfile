pipeline{
    agent any
    stages {
            stage('env') {
                steps {
                    sh 'printenv'
                }
            }

        stage('Build') {
            agent {
                docker {
                    image 'python:3-alpine'
                }
            }
            steps {
                sh 'python -m py_compile sources/add2vals.py sources/calc.py'
            }
        }
        stage('Test') {

            parallel {
                stage('on centos') {
                    agent {
                        docker {
                            image 'qnib/pytest'
                        }
                    }
                    steps {
                        sh 'py.test --verbose --junit-xml test-reports/results.xml sources/test_calc.py || true'
                    }
                    post {
                        always {
                            junit 'test-reports/results.xml'
                        }
                    }
                }
                stage('on debian') {
                    agent {
                        docker {
                            image 'qnib/pytest'
                        }
                    }
                    steps {
                        sh 'py.test --verbose --junit-xml test-reports/results.xml sources/test_calc2.py || true'
                    }
                    post {
                        always {
                            junit 'test-reports/results.xml'
                        }

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
                sh 'pyinstaller --onefile sources/add2vals.py'
                input message: "Build stage finished.(click to preceded)"

            }
            post {
                success {
                    archiveArtifacts 'dist/add2vals'
                    githubNotify description: 'This is a shorted example',  status: 'SUCCESS'
                }

            }
        }
    }


}