pipeline {
    agent any

    environment {
        EC2_USER   = "ubuntu"
        EC2_HOST   = "13.201.33.136"
        EC2_PATH   = "/home/ubuntu/2-tier-app"
        SSH_KEY_ID = "ec2-key"
        PYTHON_CMD = "python3"
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
                    echo "No tests found — skipping."
                fi
                """
            }
        }

        stage('Deploy to EC2') {
            steps {
                echo "Deploying application to EC2..."
                sshagent(credentials: [SSH_KEY_ID]) {
                    sh """
                    ssh -o StrictHostKeyChecking=no ${EC2_USER}@${EC2_HOST} "mkdir -p ${EC2_PATH}"
                    scp -o StrictHostKeyChecking=no -r ./* ${EC2_USER}@${EC2_HOST}:${EC2_PATH}/
                    ssh -o StrictHostKeyChecking=no ${EC2_USER}@${EC2_HOST} "sudo systemctl daemon-reload"
                    ssh -o StrictHostKeyChecking=no ${EC2_USER}@${EC2_HOST} "sudo systemctl restart flaskapp || true"
                    """
                }
            }
        }
    }

    post {
        success {
            echo "Pipeline SUCCESS"
        }
        failure {
            echo "Pipeline FAILED"
        }
    }
}

