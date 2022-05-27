pipeline {
    agent none
    stages {
        stage('Build') {
            agent {
                docker {
                    image 'python:3-alpine'
                }
            }
            steps {
                sh 'python3 -m py_compile MA5680/cat/AutoConfirmCat.py MA5680/cat/findLoid.py MA5680/cat/deleportcat.py'
            }
        }
        stage('Test') {
            agent {
                docker {
                    image 'qnib/pytest'
                }
            }
            steps {
                sh 'py.test --verbose --junit-xml test-reports/results.xml MA5680/cat/AutoConfirmCat.py MA5680/cat/findLoid.py MA5680/cat/deleportcat.py'
            }
            post {
                always {
                    junit 'test-reports/results.xml'
                }
            }
        }
        stage('Deliver') {
            agent {
                docker {
                    image 'cdrx/pyinstaller-linux:python3'
                }
            }
            steps {
                sh 'pyinstaller --onefile MA5680/cat/deleportcat.py'
            }
            post {
                success {
                    archiveArtifacts 'dist/deleportcat'
                }
            }
        }
    }
}