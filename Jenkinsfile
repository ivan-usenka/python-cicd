pipeline {
    agent any
    stages {
        stage('build') {
            steps {
                withPythonEnv('python3') {
                    sh 'python3 -m pip install --upgrade build twine pytest'
                    sh 'python3 -m build'
                }
            }
        }
        stage('tests') {
                    steps {
                        withPythonEnv('python3') {
                            sh 'pytest'
                        }
                    }
                }
        stage('upload-to-nexus') {
                    steps {
                        withPythonEnv('python3') {
                            sh 'twine upload dist/* -r nexus --config-file /Users/ivan_usenka/Epam_Work/Fedex/python-cicd/.pypirc'
                        }
                    }
                }
    }
}