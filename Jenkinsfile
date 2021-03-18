pipeline {
    agent any
    stages {
        stage('build') {
            steps {
                sh 'python3 -m pip install twine'
                sh 'python3 -m build'
            }
        }
        stage('upload-to-nexus') {
                    steps {
                        sh 'twine upload dist/* -r nexus --config-file /Users/ivan_usenka/Epam Work/Fedex/python-cicd/.pypirc'
                    }
                }
    }
}