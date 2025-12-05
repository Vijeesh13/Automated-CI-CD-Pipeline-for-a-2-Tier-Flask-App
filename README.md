## Architecture

                           ┌─────────────────────────┐
                           │       User Browser      │
                           │ (HTTP requests on 5000) │
                           └─────────────┬───────────┘
                                         │
                                         ▼
                           ┌─────────────────────────┐
                           │   Flask App Container   │
                           │  (Service: flask)       │
                           │  Image: flask-app       │
                           ├─────────────────────────┤
                           │  Flask + Gunicorn/dev   │
                           │  Reads env variables:   │
                           │   - MYSQL_HOST          │
                           │   - MYSQL_USER          │
                           │   - MYSQL_PASSWORD      │
                           │   - MYSQL_DB            │
                           └─────────────┬───────────┘
                                         │
                              SQL over Docker network
                                         │
                                         ▼
                           ┌─────────────────────────┐
                           │   MySQL DB Container    │
                           │ (Service: mysql)        │
                           ├─────────────────────────┤
                           │  Database: devops       │
                           │  Table: messages        │
                           │  Data persisted via     │
                           │  mysql-data volume      │
                           └─────────────┬───────────┘
                                         │
                                         ▼
                           ┌─────────────────────────┐
                           │     Docker Host / EC2   │
                           │  - Docker Engine        │
                           │  - docker-compose       │
                           │  - Jenkins Agent        │
                           └─────────────────────────┘


⭐ Project Overview

Application tier: Python Flask web app that lets users submit and view messages.

Database tier: MySQL database that stores messages in a persistent volume.

Orchestration: Docker Compose manages both containers and their shared network.

CI/CD: Jenkins pipeline automates cloning the repo, building the Docker image, and deploying the stack via Docker Compose.

This project is ideal as a DevOps portfolio piece to demonstrate your understanding of containerization and deployment automation.

🎯 Objectives

Build a simple two-tier web application (Flask + MySQL).

Containerize both tiers using Docker.

Use Docker Compose to manage multi-container deployment.

Implement a Jenkins pipeline that:

Clones the repository from GitHub

Builds the Flask app Docker image

Runs docker compose to deploy the full stack

🧩 Features

Application (Flask):

Renders a web page where users can submit messages.

Stores messages in a MySQL database.

Reads database configuration from environment variables for flexibility.

Initializes the messages table automatically if it doesn’t exist.

Database (MySQL):

Runs as a dedicated container.

Initializes a devops database (configurable).

Uses a named Docker volume to persist data across container restarts.

Includes a health check to ensure the database is ready before the app starts.

CI/CD Pipeline (Jenkins):

Declarative Jenkinsfile stored in the repo.

Clones code from GitHub on each run.

Builds a fresh Docker image for the Flask app.

Runs docker compose down and docker compose up -d --build to redeploy.

🛠 Tech Stack

Backend: Python, Flask

Database: MySQL

Containerization: Docker, Docker Compose

CI/CD: Jenkins pipeline

Version Control: GitHub

📂 Project Structure

You can describe the structure like this (no need to list every file):

app.py – Main Flask application (routes, DB connection, DB initialization).

templates/ – HTML templates for the frontend (e.g. index.html).

docker-compose.yml – Multi-container definition (Flask + MySQL, networks, volumes, healthchecks).

dockerfile – Docker image definition for the Flask app.

Jenkinsfile – Jenkins pipeline stages for build and deployment.

requirements.txt – Python dependencies for the Flask app.

2-tier Output.png – Screenshot/output of the running application (optional for README).

🏗 Architecture
Application Architecture

The Flask container exposes port 5000 and connects to the MySQL container over a private Docker network.

MySQL data is stored in a named volume (mysql-data) to ensure persistence.

Environment variables (MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB) are used to configure the database connection inside the Flask container.

You can embed the ASCII diagram from earlier here under this section.

⚙️ How It Works (End-to-End Flow)

Developer writes or updates code in the Flask app and pushes changes to the GitHub repository.

Jenkins is configured with a pipeline that uses the Jenkinsfile stored in this repo.

When the pipeline runs, Jenkins:

Clones the latest version of the repository.

Builds the Docker image for the Flask application (flask-app:latest).

Runs docker compose down to stop any existing containers.

Runs docker compose up -d --build to start the updated Flask and MySQL containers.

Docker Compose:

Starts the MySQL container and waits until its health check passes.

Starts the Flask container, injecting the database settings via environment variables.

Users can then access the Flask application via the server’s IP on port 5000, submit messages, and see them stored in MySQL.

🔑 Environment & Configuration

Database connection settings are provided via environment variables in docker-compose.yml, including:

MYSQL_HOST – MySQL service name (usually mysql in the Docker network).

MYSQL_USER – Database user (e.g. root).

MYSQL_PASSWORD – Password for the user.

MYSQL_DB – Target database name (e.g. devops).

The Flask app reads these values using os.environ.get(...) and configures flask_mysqldb accordingly.

🚀 Running the Stack (High-Level Steps)

You don’t have to paste exact commands if you don’t want; this high-level description is enough for a portfolio README:

Set up Docker and Docker Compose on the host machine or EC2 instance.

Clone this repository onto the host.

Build the Flask image and start the stack using Docker Compose.

Open a browser and navigate to http://<server-ip>:5000 to access the app.

If using Jenkins:

Install Jenkins on the same host (or with access to Docker).

Configure a Pipeline job that uses this repository and the provided Jenkinsfile.

Run the job (or configure webhooks/poll SCM) to trigger automated deployments on every code change.

🔁 CI/CD Pipeline (Jenkinsfile Summary)

The Jenkinsfile defines a simple 3-stage pipeline:

Clone Code

Pulls the latest code from the main branch of this GitHub repository.

Build Docker Image

Builds the Docker image for the Flask application (flask-app:latest) using the project dockerfile.

Deploy with Docker Compose

Runs docker compose down to stop existing containers (if any).

Runs docker compose up -d --build to bring up the latest version of the Flask and MySQL containers.

This approach makes the Jenkins agent itself the deployment server, simplifying the setup.
