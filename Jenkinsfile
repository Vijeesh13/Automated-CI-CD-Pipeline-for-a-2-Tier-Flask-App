pipeline {
    agent any

    environment {
        EC2_USER    = "ubuntu"
        EC2_HOST    = "15.206.157.50"
        EC2_PATH    = "/home/ubuntu/Automated-CI-CD-Pipeline-for-a-2-Tier-Flask-App"
        SSH_KEY_ID  = "new-key"
        PYTHON_CMD  = "python3"
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
                echo "Deploying to EC2 instance..."

                sshagent(credentials: ["${SSH_KEY_ID}"]) {
                    sh """
                        # Create directory if not exists
                        ssh -o StrictHostKeyChecking=no ${EC2_USER}@${EC2_HOST} "mkdir -p ${EC2_PATH}"

                        # Copy project files
                        rsync -avz -e "ssh -o StrictHostKeyChecking=no" ./ ${EC2_USER}@${EC2_HOST}:${EC2_PATH}

                        # Install dependencies on EC2 & restart app
                        ssh -o StrictHostKeyChecking=no ${EC2_USER}@${EC2_HOST} "
                            cd ${EC2_PATH}
                            sudo python3 -m pip install --upgrade pip
                            sudo python3 -m pip install -r requirements.txt

                            # Kill old process
                            sudo pkill -f app.py || true

                            # Run app in background
                            nohup python3 app.py > app.log 2>&1 &
                        "
                    """
                }
            }
        }
    }
}

