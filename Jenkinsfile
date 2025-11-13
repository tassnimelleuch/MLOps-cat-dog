pipeline {
    agent any
    
    environment {
        PYTHONPATH = "${WORKSPACE}"
        VENV_PATH = "${WORKSPACE}/venv"
        MODEL_NAME = "cat_dog_classifier"
        DATASET_NAME = "tongpython/cat-and-dog"
    }
    
    stages {
        stage('Checkout Code') {
            steps {
                echo "📥 Checking out code from GitHub..."
                checkout scm
                sh 'ls -la'
            }
        }
        
        stage('Setup Python Environment') {
            steps {
                echo "🐍 Setting up Python environment..."
                sh '''
                    python3 --version
                    pip3 --version
                    python3 -m venv $VENV_PATH
                    . $VENV_PATH/bin/activate
                    pip install --upgrade pip
                    echo "Virtual environment created at: $VENV_PATH"
                '''
            }
        }
        
        stage('Install Dependencies') {
            steps {
                echo "📦 Installing Python dependencies..."
                sh '''
                    . $VENV_PATH/bin/activate
                    echo "Installing from requirements.txt..."
                    pip install -r requirements.txt
                    echo "Installed packages:"
                    pip list | grep -E "(kaggle|tensorflow|keras|pandas|numpy)"
                '''
            }
        }
        
        stage('Setup Kaggle Credentials') {
            steps {
                echo "🔑 Setting up Kaggle credentials..."
                withCredentials([file(credentialsId: 'kaggle-api-key', variable: 'KAGGLE_JSON')]) {
                    sh '''
                        echo "Setting up Kaggle configuration from secret file..."
                        mkdir -p ~/.kaggle
                        cp $KAGGLE_JSON ~/.kaggle/kaggle.json
                        chmod 600 ~/.kaggle/kaggle.json
                        echo "✅ Kaggle credentials configured successfully"
                        echo "Kaggle directory contents:"
                        ls -la ~/.kaggle/
                    '''
                }
            }
        }
        
        stage('Download Dataset') {
            steps {
                echo "📥 Downloading dataset from Kaggle..."
                sh '''
                    . $VENV_PATH/bin/activate
                    echo "Current directory: $(pwd)"
                    echo "Running dataset download..."
                    python src/data/download_data.py
                    echo "✅ Dataset download completed"
                    echo "Data directory structure:"
                    find data/ -type d | sort | head -10
                '''
            }
        }
        
        stage('Data Validation') {
            steps {
                echo "🔍 Validating dataset..."
                sh '''
                    . $VENV_PATH/bin/activate
                    echo "Running data validation..."
                    if [ -f "src/data/data_validation.py" ]; then
                        python src/data/data_validation.py
                    else
                        echo "Data validation script not found, running basic checks..."
                        echo "Total images found:"
                        find data/ -name "*.jpg" | wc -l
                        echo "Sample files:"
                        find data/ -name "*.jpg" | head -5
                    fi
                '''
            }
        }
        
        stage('Train Model') {
            steps {
                echo "🤖 Training cat/dog model..."
                sh '''
                    . $VENV_PATH/bin/activate
                    echo "Starting model training..."
                    python src/models/train_model.py
                    echo "✅ Training completed"
                    echo "Generated model files:"
                    ls -la models/ 2>/dev/null || echo "No models directory found"
                '''
            }
        }
        
        stage('Evaluate Model') {
            steps {
                echo "📊 Evaluating model performance..."
                sh '''
                    . $VENV_PATH/bin/activate
                    echo "Running model evaluation..."
                    if [ -f "src/models/evaluate_model.py" ]; then
                        python src/models/evaluate_model.py
                    else
                        echo "Evaluation script not found, checking model files..."
                        find models/ -name "*.h5" -o -name "*.pkl" 2>/dev/null | head -5
                    fi
                '''
            }
        }
        
        stage('Save Artifacts') {
            steps {
                echo "💾 Saving model artifacts..."
                sh '''
                    echo "Final workspace structure:"
                    find . -maxdepth 2 -type d | sort
                    echo "Models to archive:"
                    find models/ -type f 2>/dev/null | head -10 || echo "No models found"
                '''
                archiveArtifacts artifacts: 'models/*.h5, models/*.pkl, models/*.json, logs/**, reports/**', fingerprint: true
                archiveArtifacts artifacts: '**/*.png, **/training_history.csv', allowEmptyArchive: true
            }
        }
    }
    
    post {
        always {
            echo "🚀 Pipeline execution completed!"
            sh '''
                echo "=== CLEANUP ==="
                echo "Removing temporary files..."
                find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
                find . -name "*.pyc" -delete 2>/dev/null || true
                echo "Securely removing Kaggle credentials..."
                rm -f ~/.kaggle/kaggle.json 2>/dev/null || true
                echo "✅ Cleanup completed"
            '''
        }
        success {
            echo "✅ Pipeline succeeded! Model trained and saved."
        }
        failure {
            echo "❌ Pipeline failed! Check the logs above."
        }
    }
    
    options {
        timeout(time: 2, unit: 'HOURS')
        retry(2)
        buildDiscarder(logRotator(numToKeepStr: '5'))
    }
}