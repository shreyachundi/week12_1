pipeline {
    agent any

    stages {

        stage('Run Selenium Tests with pytest') {
            steps {
                echo "Running Selenium Tests using pytest"

                // Install Python dependencies
                sh 'python3 -m pip install -r requirements.txt'

                // Start Flask application in background
                sh 'python3 app.py &'

                // Wait for Flask application to start
                sh 'sleep 5'

                // Run Selenium tests
                sh 'python3 -m pytest -v'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "Build Docker Image"

                sh "docker build -t week12_1app:v1 ."
            }
        }

        stage('Docker Login') {
            steps {
                  sh 'docker login -u shreyachundi -p Karthikeya@011'
                }
            }

        stage('Push Docker Image to Docker Hub') {
            steps {
                echo "Push Docker Image to Docker Hub"

                sh "docker tag week12a_1pp:v1 shreyachundi/week8_docker:another_12_image"

                sh "docker push shreyachundi/week8_docker:another_12_image"
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                echo "Deploying application to Kubernetes"

                sh 'kubectl apply -f deployment.yaml --validate=false'

                sh 'kubectl apply -f service.yaml'
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully!'
        }

        failure {
            echo 'Pipeline failed. Please check the logs.'
        }
    }
}