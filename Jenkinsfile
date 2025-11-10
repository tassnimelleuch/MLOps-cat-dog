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
            }
        }
        
        stage('Setup Kaggle Credentials') {
            steps {
                echo "🔑 Setting up Kaggle credentials..."
                sh '''
                    mkdir -p ~/.kaggle
                    echo "Kaggle setup - will be configured manually"
                '''
            }
        }
        
        stage('Download Dataset') {
            steps {
                echo "📥 Downloading dataset from Kaggle..."
                sh 'python3 -m src.data.download_data'
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
                archiveArtifacts artifacts: 'models/*.h5, models/*.png, models/*.json', fingerprint: true
            }
        }
    }
    
    post {
        always {
            echo "🚀 Pipeline execution completed!"
            sh 'find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true'
        }
        success {
            echo "✅ Pipeline succeeded! Model trained and saved."
        }
        failure {
            echo "❌ Pipeline failed! Check the logs above."
        }
    }
}