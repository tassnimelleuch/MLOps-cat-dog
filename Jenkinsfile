pipeline {
    agent any
    
    environment {
        PYTHONPATH = "${WORKSPACE}"
    }
    
    stages {
        stage('Checkout Code') {
            steps {
                echo "📥 Checking out code from GitHub..."
                checkout scm
            }
        }
        
        stage('Setup Python Environment') {
            steps {
                echo "🐍 Setting up Python environment..."
                sh '''
                    python3 --version
                    pip3 --version
                    pip3 install --upgrade pip
                '''
            }
        }
        
        stage('Install Dependencies') {
            steps {
                echo "📦 Installing Python dependencies..."
                sh 'pip3 install -r requirements.txt'
                // Install kaggle CLI
                sh 'pip3 install kaggle'
            }
        }
        
        stage('Setup Kaggle Credentials') {
            steps {
                echo "🔑 Setting up Kaggle credentials..."
                // Method 1: Using Jenkins credentials binding
                withCredentials([file(credentialsId: 'kaggle-api-key', variable: 'KAGGLE_JSON')]) {
                    sh '''
                        mkdir -p ~/.kaggle
                        cp $KAGGLE_JSON ~/.kaggle/kaggle.json
                        chmod 600 ~/.kaggle/kaggle.json
                    '''
                }
            }
        }
        
        stage('Download Dataset') {
            steps {
                echo "📥 Downloading dataset from Kaggle..."
                sh 'python3 -m src.data.download_data'
            }
        }
        
        stage('Data Validation') {
            steps {
                echo "🔍 Validating dataset..."
                sh 'python3 -m src.data.data_validation'
            }
        }
        
        stage('Train Model') {
            steps {
                echo "🤖 Training cat/dog model..."
                sh 'python3 -m src.models.train_model'
            }
        }
        
        stage('Test Model') {
            steps {
                echo "🧪 Testing model performance..."
                sh 'python3 -m src.models.test_model'
            }
        }
        
        stage('Save Artifacts') {
            steps {
                echo "💾 Saving model artifacts..."
                archiveArtifacts artifacts: 'models/*.h5, models/*.png, models/*.json, logs/*', fingerprint: true
            }
        }
    }
    
    post {
        always {
            echo "🚀 Pipeline execution completed!"
            // Cleanup
            sh '''
                find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
                rm -rf ~/.kaggle/kaggle.json  # Remove credentials
            '''
        }
        success {
            echo "✅ Pipeline succeeded! Model trained and saved."
        }
        failure {
            echo "❌ Pipeline failed! Check the logs above."
        }
    }
}