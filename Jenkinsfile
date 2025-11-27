pipeline {
    agent any

    stages {
        stage('Clone Repo') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/Vijeesh13/Automated-CI-CD-Pipeline-for-a-2-Tier-Flask-App.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                sudo apt update -y
                pip3 install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh 'pytest || true'
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                # Example Deployment (Modify based on your setup)
                sudo systemctl restart flaskapp
                '''
            }
        }
    }
}

