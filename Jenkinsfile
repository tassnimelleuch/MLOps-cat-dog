pipeline {
    agent any
    
    environment {
        PYTHONPATH = "${WORKSPACE}"
        MODEL_NAME = "cat_dog_classifier"
        DATASET_NAME = "tongpython/cat-and-dog"
        PATH = "/var/lib/jenkins/.local/bin:${env.PATH}"
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
        // STAGE 2: DEPENDENCIES
        // =====================
        stage('Install Dependencies') {
            steps {
                echo "🐍 Setting up Python environment..."
                sh '''
                    echo "=== PYTHON INFO ==="
                    python3 --version
                    pip3 --version
                    echo "=== INSTALLING DEPENDENCIES ==="
                    pip3 install --upgrade pip
                    pip3 install -r requirements.txt
                    
                    echo "=== INSTALLING KAGGLE CLI ==="
                    pip3 install kaggle --user
                    echo "=== VERIFY KAGGLE INSTALLATION ==="
                    which kaggle || echo "Kaggle not in PATH"
                    ls -la /var/lib/jenkins/.local/bin/kaggle || echo "Kaggle binary not found"
                    echo "=== VERIFY PACKAGES ==="
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
                        
                        echo "=== TEST KAGGLE CLI ==="
                        which kaggle && kaggle --version || echo "Kaggle CLI test failed"
                        
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
                    
                    kaggle --version || echo "Kaggle CLI not available"
                    python3 src/data/download_data.py
                    
                    echo "=== VERIFY DOWNLOAD ==="
                    find data/ -type f 2>/dev/null | head -10 || echo "No data files found"
                    
                    if [ ! -d "data/training_set/training_set" ]; then
                        echo "❌ ERROR: Training data directory not found!"
                        find data/ -type d 2>/dev/null
                        exit 1
                    fi
                    
                    TRAINING_IMAGES=$(find data/training_set/training_set -name "*.jpg" | wc -l)
                    echo "Found $TRAINING_IMAGES training images"
                    
                    if [ "$TRAINING_IMAGES" -eq 0 ]; then
                        echo "❌ ERROR: No training images found!"
                        exit 1
                    fi
                '''
            }
        }
        
        // =====================
        // STAGE 5: TRAIN MODEL
        // =====================
        stage('Train Model') {
            when {
                branch 'main'  // ✅ Only run training when on main branch
            }
            steps {
                echo "🤖 Training cat/dog model (only runs on main branch)..."
                sh '''
                    echo "=== TRAINING SCRIPT CHECK ==="
                    find . -name "*train*" -name "*.py" | head -5
                    
                    echo "=== DATA VERIFICATION BEFORE TRAINING ==="
                    ls -la data/training_set/training_set/ || echo "Training data missing"
                    find data/training_set/training_set/ -name "*.jpg" | head -5
                    
                    echo "=== STARTING TRAINING ==="
                    python3 src/models/train_model.py
                    
                    echo "=== CHECK MODEL OUTPUT ==="
                    ls -la models/ 2>/dev/null || echo "No models directory"
                    find models/ -name "*.h5" -o -name "*.pkl" -o -name "*.json" 2>/dev/null | head -10
                '''
            }
        }
        
        // =====================
        // STAGE 6: SAVE RESULTS
        // =====================
        stage('Save Artifacts') {
            when {
                branch 'main'  // ✅ Only archive artifacts on main branch
            }
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
    }
    
    post {
        always {
            echo "🚀 Pipeline execution completed!"
            sh '''
                echo "=== CLEANUP ==="
                du -sh . || echo "Size check failed"
                rm -f ~/.kaggle/kaggle.json 2>/dev/null || true
                ls -la
            '''
        }
        success {
            echo "✅ Pipeline succeeded!"
        }
        failure {
            echo "❌ Pipeline failed! Check logs above."
        }
    }
    
    options {
        timeout(time: 2, unit: 'HOURS')
        retry(1)
    }
}
