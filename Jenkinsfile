def packages_to_install = "twine pytest apache-beam[gcp] airflow"

def dataflow_template_staging_command = "python -m src.pipeline.beam " +
                        "--runner DataflowRunner " +
                        "--project or2-msq-fdxg-fact-t1iylu " +
                        "--region europe-west3 " +
                        "--staging_location gs://dataflow_cicd_test/staging " +
                        "--temp_location gs://dataflow_cicd_test/temp " +
                        "--template_location gs://dataflow_cicd_test/templates/test_beam"

def airflow_dag_source_location = "src/dag/test-dag.py"

def airflow_dag_target_bucket = "gs://europe-west3-composer-pytho-c11ac81b-bucket/dags/"

def pypirc_path = "/Users/ivan_usenka/Epam_Work/Fedex/python-cicd/.pypirc"

def python_env = "python3"

def sonar_qube_scanner_env = "SonarQube Scanner 4.6.0"


pipeline {

    agent any

    environment {
        GOOGLE_APPLICATION_CREDENTIALS = credentials("googlesa")
    }

    stages {
        stage('Build Package') {
            steps {
                withPythonEnv("${python_env}") {
                    sh 'python3 -m pip install --upgrade build ${packages_to_install}'
                    sh 'python3 -m build'
                }
            }
        }
        stage('Run Tests') {
            steps {
                withPythonEnv("${python_env}") {
                    sh 'pytest'
                }
            }
        }
        stage('SonarQube Analysis') {
            steps {
                script {
                    scannerHome = tool "${sonar_qube_scanner_env}"
                }
                    withSonarQubeEnv("${sonar_qube_scanner_env}") {
                    sh "${scannerHome}/bin/sonar-scanner"
                }
            }
        }
        stage('Stage Dataflow Template') {
            steps {
                withPythonEnv("${python_env}") {
                    sh "${dataflow_template_staging_command}"
                }
            }
        }
        stage('Upload Airflow DAG') {
            steps {
                withPythonEnv("${python_env}") {
                    sh "gsutil cp ${airflow_dag_source_location} ${airflow_dag_target_bucket}"
                }
            }
        }
        stage('Upload Artifact To Nexus') {
            steps {
                withPythonEnv("${python_env}") {
                    sh "twine upload dist/* -r nexus --config-file ${pypirc_path}"
                }
            }
        }
    }
}