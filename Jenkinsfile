pipeline {

    agent any

    environment {
        GOOGLE_APPLICATION_CREDENTIALS = credentials("googlesa")
    }

    stages {
        stage('build') {
            steps {
                withPythonEnv('python3') {
                    sh 'python3 -m pip install --upgrade build twine pytest apache-beam[gcp]'
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
        stage('stage-template') {
            steps {
                withPythonEnv('python3') {
                    sh 'python -m src.pipeline.beam --runner DataflowRunner --project or2-msq-fdxg-fact-t1iylu --region europe-west3 --staging_location gs://dataflow_cicd_test/staging --temp_location gs://dataflow_cicd_test/temp --template_location gs://dataflow_cicd_test/templates/test_beam'
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