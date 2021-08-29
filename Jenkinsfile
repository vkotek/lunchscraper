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
        }
    }
}