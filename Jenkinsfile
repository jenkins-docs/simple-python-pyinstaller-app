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
        stage('Deploy') {
            when {
                branch 'kjug'
            }
            agent { label 'master' }
            steps {
                input message: 'Are you sure to deploy?'
                unstash 'exec_files'
                sh 'scp -r -o StrictHostKeyChecking=no dist/webapp root@172.17.0.3:/var/'
            }
        }
        stage('Smoke Test') {
            when {
                branch 'kjug'
            }
            agent { label 'master' }
            steps {
                sh 'ssh -o StrictHostKeyChecking=no root@172.17.0.3 ls -la /var/webapp'
            }
        }
        }
    }