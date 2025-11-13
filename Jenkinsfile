pipeline {
    agent any
    
    environment {
        PYTHONPATH = "${WORKSPACE}"
        MODEL_NAME = "cat_dog_classifier"
        DATASET_NAME = "tongpython/cat-and-dog"
    }
    
    stages {
        // =====================
        // STAGE 1: BASIC SETUP
        // =====================
        stage('Checkout Code') {
            steps {
                echo "📥 Checking out code from GitHub..."
                checkout scm
                sh '''
                    echo "=== WORKSPACE STRUCTURE ==="
                    pwd
                    ls -la
                    echo "=== SOURCE CODE CHECK ==="
                    find . -name "*.py" | head -10
                    echo "=== DOWNLOAD SCRIPT CHECK ==="
                    ls -la src/data/ || echo "src/data/ not found"
                '''
            }
        }
        
        // =====================
        // STAGE 2: ENVIRONMENT
        // =====================
        stage('Setup Environment') {
            steps {
                echo "🐍 Setting up Python environment..."
                sh '''
                    echo "=== PYTHON INFO ==="
                    python3 --version
                    pip3 --version
                    echo "=== INSTALLING DEPENDENCIES ==="
                    pip3 install --upgrade pip
                    pip3 install -r requirements.txt
                    echo "=== VERIFY INSTALLATION ==="
                    pip3 list | grep -E "(kaggle|tensorflow|numpy)"
                '''
            }
        }
        
        // =====================
        // STAGE 3: KAGGLE SETUP
        // =====================
        stage('Setup Kaggle Credentials') {
            steps {
                echo "🔑 Setting up Kaggle credentials..."
                withCredentials([file(credentialsId: 'kaggle-api-key', variable: 'KAGGLE_JSON')]) {
                    sh '''
                        echo "=== KAGGLE SETUP ==="
                        mkdir -p ~/.kaggle
                        cp $KAGGLE_JSON ~/.kaggle/kaggle.json
                        chmod 600 ~/.kaggle/kaggle.json
                        echo "✅ Kaggle credentials configured"
                        echo "=== TEST KAGGLE IMPORT ==="
                        python3 -c "import kaggle; print('✅ Kaggle import successful')"
                    '''
                }
            }
        }
        
        // =====================
        // STAGE 4: DOWNLOAD DATA
        // =====================
        stage('Download Dataset') {
            steps {
                echo "📥 Downloading dataset from Kaggle..."
                sh '''
                    echo "=== DOWNLOAD SCRIPT EXECUTION ==="
                    echo "Current directory: $(pwd)"
                    echo "Looking for download script..."
                    find . -name "download_data.py" -type f
                    echo "=== RUNNING DOWNLOAD ==="
                    python3 src/data/download_data.py
                    echo "=== VERIFY DOWNLOAD ==="
                    find data/ -type d 2>/dev/null | head -5 || echo "No data directory found"
                '''
            }
        }
        
        // =====================
        // STAGE 5: TRAIN MODEL
        // =====================
        stage('Train Model') {
            steps {
                echo "🤖 Training cat/dog model..."
                sh '''
                    echo "=== TRAINING SCRIPT CHECK ==="
                    find . -name "*train*" -name "*.py" | head -5
                    echo "=== STARTING TRAINING ==="
                    python3 src/models/train_model.py
                    echo "=== CHECK MODEL OUTPUT ==="
                    ls -la models/ 2>/dev/null || echo "No models directory"
                '''
            }
        }
        
        // =====================
        // STAGE 6: SAVE RESULTS
        // =====================
        stage('Save Artifacts') {
            steps {
                echo "💾 Saving model artifacts..."
                sh '''
                    echo "=== FINAL WORKSPACE ==="
                    find . -maxdepth 2 -type d | sort
                    echo "=== ARTIFACTS TO SAVE ==="
                    find models/ -type f 2>/dev/null | head -10 || echo "No models found"
                '''
                archiveArtifacts artifacts: 'models/*.h5, models/*.pkl, models/*.json', fingerprint: true, allowEmptyArchive: true
            }
        }
        
        // =========================================================================
        // COMMENTED STAGES - UNCOMMENT AS NEEDED
        // =========================================================================
        
        /*
        stage('Data Validation') {
            steps {
                echo "🔍 Validating dataset..."
                sh '''
                    echo "Running data validation..."
                    if [ -f "src/data/data_validation.py" ]; then
                        python3 src/data/data_validation.py
                    else
                        echo "Data validation script not found"
                    fi
                '''
            }
        }
        */
        
        /*
        stage('Evaluate Model') {
            steps {
                echo "📊 Evaluating model performance..."
                sh '''
                    echo "Running model evaluation..."
                    if [ -f "src/models/evaluate_model.py" ]; then
                        python3 src/models/evaluate_model.py
                    else
                        echo "Evaluation script not found"
                    fi
                '''
            }
        }
        */
        
        /*
        stage('Generate Reports') {
            steps {
                echo "📈 Generating training reports..."
                sh '''
                    mkdir -p reports
                    echo "Training completed $(date)" > reports/training_report.txt
                '''
                archiveArtifacts artifacts: 'reports/**', fingerprint: true
            }
        }
        */
    }
    
    post {
        always {
            echo "🚀 Pipeline execution completed!"
            sh '''
                echo "=== CLEANUP ==="
                echo "Workspace size:"
                du -sh . || echo "Size check failed"
                echo "Removing credentials..."
                rm -f ~/.kaggle/kaggle.json 2>/dev/null || true
            '''
        }
        success {
            echo "✅ Pipeline succeeded!"
        }
        failure {
            echo "❌ Pipeline failed! Check stage where it failed above."
        }
    }
    
    options {
        timeout(time: 2, unit: 'HOURS')
        retry(1)
    }
}