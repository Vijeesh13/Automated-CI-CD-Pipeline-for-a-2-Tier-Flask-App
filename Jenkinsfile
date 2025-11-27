pipeline {
    agent any

    environment {
        EC2_USER     = "ubuntu"
        EC2_HOST     = "13.201.33.136"
        EC2_PATH     = "/home/ubuntu/2-tier-app"
        SSH_KEY_ID   = "ec2-key"
        PYTHON_CMD   = "python3"
    }

    stages {

        stage('Checkout') {
            steps {
                echo "Checking out repository..."
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                echo "Installing Python dependencies..."
                sh """
                    ${PYTHON_CMD} -m pip install --upgrade pip --user
                    ${PYTHON_CMD} -m pip install --user -r requirements.txt
                """
            }
        }

        stage('Run Tests') {
            steps {
                echo "Running tests..."
                sh """
                    if [ -d tests ]; then
                        ${PYTHON_CMD} -m pip install --user pytest
                        ${PYTHON_CMD} -m pytest || true
                    else
                        echo "No tests found — skippin

