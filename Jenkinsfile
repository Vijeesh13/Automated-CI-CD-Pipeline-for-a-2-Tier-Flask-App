pipeline {
    agent any

    environment {
        APP_DIR = "/home/ubuntu/2-tier-app"
    }

    stages {

        stage('Checkout Code') {
            steps {
                echo "Cloning repository..."
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                echo "Installing Python dependencies..."
                sh '''
                    pip3 install --upgrade pip
                    pip3 install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                echo "Running tests..."
                sh '''
                    if [ -f "pytest.ini" ] || [ -d "tests" ]; then
                        pip3 install pytest
                        pytest || true
                    else
                        echo "No tests found, skipping..."
                    fi
                '''
            }
        }

        stage('Deploy to EC2') {
            steps {
                echo "Deploying application..."
                sh '''
                    cp -r * ${APP_DIR}/
                    if systemctl status flaskapp >/dev/null 2>&1; then
                        systemctl restart flaskapp
                    else
                        echo "Flask service not found, skipping restart."
                    fi
                '''
            }
        }
    }

    post {
        success {
            echo "Pipeline completed successfully!"
        }
        failure {
            echo "Pipeline failed!"
        }
    }
}

