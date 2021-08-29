Jenkinsfile (Declarative Pipeline)
pipeline {
    agent { 
        any
    }
    stages {
        stage('build') {
            steps {
                echo 'Building app...'
                sh 'python --version'
            }
        }
    }
}