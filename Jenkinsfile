def packages_to_install = "twine pytest apache-beam[gcp]"

def dataflow_template_staging_command = "python -m src.pipeline.beam " +
                        "--runner DataflowRunner " +
                        "--project or2-msq-fdxg-fact-t1iylu " +
                        "--region europe-west3 " +
                        "--staging_location gs://dataflow_cicd_test/staging " +
                        "--temp_location gs://dataflow_cicd_test/temp " +
                        "--template_location gs://dataflow_cicd_test/templates/test_beam"

def airflow_dag_source_location = "src/dag/test-dag.py"

def airflow_dag_target_bucket = "gs://test_dag_upload/"

def pypirc_path = "/Users/ivan_usenka/Epam_Work/Fedex/python-cicd/.pypirc"


pipeline {

    agent any

    environment {
        GOOGLE_APPLICATION_CREDENTIALS = credentials("googlesa")
    }

    stages {
        stage('Build Package') {
            steps {
                withPythonEnv('python3') {
                    sh 'python3 -m pip install --upgrade build ${packages_to_install}'
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
                    sh "${dataflow_template_staging_command}"
                }
            }
        }
        stage('Upload Airflow DAG') {
            steps {
                withPythonEnv('python3') {
                    sh 'gsutil cp ${airflow_dag_source_location} ${airflow_dag_target_bucket}'
                }
            }
        }
        stage('Upload Artifact To Nexus') {
            steps {
                withPythonEnv('python3') {
                    sh 'twine upload dist/* -r nexus --config-file ${pypirc_path}'
                }
            }
        }
    }
}