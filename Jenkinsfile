pipeline {
    agent none
    stages {

        // stage('clean workspace'){
        //     agent none
        //     steps{
        //         sh 'rm -rf $WORKSPACE/*'
        //     }
            
        // }
        stage('Build') {

            agent {
                docker {
                    image 'python:3-alpine'
                }
            }
            steps {

                sh 'python -m py_compile  MA5680/cat/deleportcat.py MA5680/cat/findLoid.py MA5680/cat/AutoConfirmCat.py'
            }
        }
        stage('Test') {
            agent {
                docker {
                    image 'devtestdemisto/netmiko:1.0.0.24037-e74ad3d315bbe6837b8870052fd708ce'
                }
            }
            steps {
                sh 'pip install -i https://pypi.douban.com/simple   pytest '
                sh 'cd MA5680/cat/ && python -m pytest --verbose --junit-xml test-reports/results.xml AutoConfirmCat.py findLoid.py deleportcat.py'
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