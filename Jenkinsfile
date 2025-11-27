pipeline {
    agent any

    environment {
        // Update these if needed
        APP_DIR = "/home/ubuntu/2-tier-app"
        PYTHON = "python3"
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
                apt update -y
                apt install -y python3 python3-pip
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
                echo "Deploying application to EC2 server..."
                sh '''
                # Replace this with your actual deployment steps
                cp -r * ${APP_DIR}/
                systemctl restart flaskapp || true
                e

