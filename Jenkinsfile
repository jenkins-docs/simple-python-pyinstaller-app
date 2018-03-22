pipeline{
    agent none
    stages {
        stage('Build') {
            agent {
                docker {
                    image 'python:2-alpine'
                }
            }
            steps {
                sh 'pip install flask'
                sh 'python -m py_compile sources/webapp.py'
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
                        sh 'ls -la'
                        sh 'pip install flask'
                        sh 'py.test --verbose --junit-xml test-reports/results.xml sources/test_webapp.py || true'
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
                        sh 'pip install flask'
                        sh 'py.test --verbose --junit-xml test-reports/results.xml sources/test_webapp.py || true'
                    }
                    post {
                        always {
                            junit 'test-reports/results.xml'
                        }

                    }
                }

            }
        }
        stage('Create Artifacts') {
            agent {
                docker {
                    image 'cdrx/pyinstaller-linux:python2'
                }
            }
            steps {
                sh 'pip install flask'
                sh 'pyinstaller --paths=/usr/lib64/python2.7/site-packages/ --onefile sources/webapp.py'
                stash includes: 'dist/webapp', name: 'exec_files'

            }
            post {
                success {
                    archiveArtifacts 'dist/webapp'
                }

            }
        }
        }
    }