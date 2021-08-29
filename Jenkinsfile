pipeline {
    agent any
    parameters {
        booleanParam(name:'skipTests', 'defaultValue': false, description: 'FUCK IT, WE WILL DO IT LIVE!!')
    }
    stages {
        stage('build') {
            steps {
                echo 'Building app...'
                sh 'python --version'
            }
        }
        stage('test') {
            when {
                expression {
                    params.skipTests == false
                }
            }
            steps {
                echo 'Testing app...'
            }
        }
        stage('deploy') {
            steps {
                echo 'Deploying app...'
            }
        }
    }
    post {
        success {
            echo 'Successfuly deployed.'
            telegramSend "Successfuly deployed ${JOB_NAME} build #${BUILD_NUMBER} \
            branch ${BRANCH_NAME}. For more details see ${BUILD_URL}"
        }
    }
}
