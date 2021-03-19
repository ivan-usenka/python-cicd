pipeline {

    agent any

    environment {
        GOOGLE_APPLICATION_CREDENTIALS = credentials("googlesa")
    }

    def staging_command = "python -m src.pipeline.beam
                            --runner DataflowRunner
                            --project or2-msq-fdxg-fact-t1iylu
                            --region europe-west3
                            --staging_location gs://dataflow_cicd_test/staging
                            --temp_location gs://dataflow_cicd_test/temp
                            --template_location gs://dataflow_cicd_test/templates/test_beam"

    stages {
        stage('Build Package') {
            steps {
                withPythonEnv('python3') {
                    sh 'python3 -m pip install --upgrade build twine pytest apache-beam[gcp]'
                    sh 'python3 -m build'
                }
            }
        }
        stage('Run Tests') {
            steps {
                withPythonEnv('python3') {
                    sh 'pytest'
                }
            }
        }
        stage('SonarQube Analysis') {
            steps {
                script {
                    // requires SonarQube Scanner 2.8+
                    scannerHome = tool 'SonarQube Scanner 4.6.0'
                }
                    withSonarQubeEnv('SonarQube Scanner 4.6.0') {
                    sh "${scannerHome}/bin/sonar-scanner"
                }
            }
        }
        stage('Stage Dataflow Template') {
            steps {
                withPythonEnv('python3') {
                    sh "${staging_command}"
                }
            }
        }
        stage('Upload Airflow DAG') {
            steps {
                withPythonEnv('python3') {
                    sh 'gsutil cp src/dag/test-dag.py gs://europe-west3-composer-pytho-c11ac81b-bucket/dag-test/'
                }
            }
        }
        stage('Upload Artifact To Nexus') {
            steps {
                withPythonEnv('python3') {
                    sh 'twine upload dist/* -r nexus --config-file /Users/ivan_usenka/Epam_Work/Fedex/python-cicd/.pypirc'
                }
            }
        }
    }
}