// Jenkinsfile (Declarative Pipeline)
pipeline {
    
    agent any 

    parameters {
        booleanParam(name:'executeTests', 'defaultValue': true, description: 'uncheck to skip tests.')
    }
    
    stages {
        stage('build') {
            steps {
                echo 'Building app...'
                sh 'python --version'
            }
        }
        stage('deploy') {
            steps {
                echo 'Deploying app...'
                sh 'python --version'
            }
        }
    }
}