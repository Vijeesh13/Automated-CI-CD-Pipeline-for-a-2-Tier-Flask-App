stage('Deploy to EC2') {
    steps {
        echo "Deploying to EC2 instance..."

        sshagent(credentials: ["${SSH_KEY_ID}"]) {
            sh """
                ssh -o StrictHostKeyChecking=no ${EC2_USER}@${EC2_HOST} "sudo mkdir -p ${EC2_PATH} && sudo chown -R ubuntu:ubuntu ${EC2_PATH}"

                rsync -avz --exclude='.git' -e "ssh -o StrictHostKeyChecking=no" ./ ${EC2_USER}@${EC2_HOST}:${EC2_PATH}

                ssh -o StrictHostKeyChecking=no ${EC2_USER}@${EC2_HOST} "
                    cd ${EC2_PATH}
                    sudo python3 -m pip install -r requirements.txt

                    # Kill old app
                    sudo pkill -f app.py || true

                    # Start new app
                    nohup python3 app.py > app.log 2>&1 &
                "
            """
        }
    }
}

