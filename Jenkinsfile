pipeline {
    agent any

    environment {
        // Set your JIRA credentials securely in Jenkins credentials store
        NAV_JIRA_USER = credentials('ATLASSIAN_CLOUD_USER')     // Replace with your Jenkins credential ID for username
        NAV_JIRA_PW = credentials('ATLASSIAN_CLOUD_APIKEY')      // Replace with your Jenkins credential ID for token
    }

    stages {
        stage('Checkout Code') {
            steps {
                git 'https://github.com/latha-414/jira.git'
            }
        }

        stage('Run JIRA Update Script') {
            steps {
                script {
                    def buildStatus = currentBuild.currentResult == 'SUCCESS' ? 'SUCCESS' : 'FAILED'
                    sh """
                        echo "Running JIRA update script with status: ${buildStatus}"
                        python3 update_jira.py ${buildStatus}
                    """
                }
            }
        }
    }

    post {
        failure {
            echo "Build failed. JIRA update script may not run transition."
        }
    }
}
