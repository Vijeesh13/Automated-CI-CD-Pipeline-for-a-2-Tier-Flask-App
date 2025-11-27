pipeline {
  agent any

  environment {
    APP_DIR = "/home/ubuntu/2-tier-app"
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
        sh '''
          set -e
          ${PYTHON_CMD} -m pip install --upgrade pip --user
          ${PYTHON_CMD} -m pip install --user -r requirements.txt
        '''
      }
    }

    stage('Run Tests') {
      steps {
        echo "Running tests..."
        sh '''
          if [ -d "tests" ]; then
            ${PYTHON_CMD} -m pip install --user pytest
            ${PYTHON_CMD} -m pytest || true
          else
            echo "No tests found, skipping."
          fi
        '''
      }
    }

    stage('Deploy to EC2') {
      steps {
        echo "Deploying application..."
        sh '''
          mkdir -p ${APP_DIR}
          cp -r . ${APP_DIR}/
          if systemctl status flaskapp >/dev/null 2>&1; then
            systemctl restart flaskapp || true
          else
            echo "No flaskapp service found."
          fi
        '''
      }
    }

  }

  post {
    success { echo "Pipeline SUCCESS" }
    failure { echo "Pipeline FAILED" }
  }
}

