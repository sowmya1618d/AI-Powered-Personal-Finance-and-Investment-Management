#!/bin/bash
# Installation and Setup Script for AI Personal Finance Application
# Run this script to set up the entire project

echo "🚀 AI Personal Finance Manager - Setup Script"
echo "=============================================="

# Check if running on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "⚠️ This script is optimized for macOS. Please adjust for your OS."
fi

# 1. Install MySQL (if not already installed)
echo ""
echo "📦 Step 1: Setting up MySQL..."

# Check if MySQL is installed
if ! command -v mysql &> /dev/null; then
    echo "Installing MySQL via Homebrew..."
    brew install mysql
    brew services start mysql
else
    echo "✅ MySQL already installed"
fi

# 2. Create database and user
echo ""
echo "🗄️ Step 2: Creating database..."

mysql -u root << 'EOF'
CREATE DATABASE IF NOT EXISTS finance_db;
CREATE USER IF NOT EXISTS 'finance_user'@'localhost' IDENTIFIED BY 'secure_password';
GRANT ALL PRIVILEGES ON finance_db.* TO 'finance_user'@'localhost';
FLUSH PRIVILEGES;
EOF

echo "✅ Database created"

# 3. Create Python virtual environment
echo ""
echo "🐍 Step 3: Setting up Python environment..."

if [ ! -d "venv" ]; then
    python3 -m venv venv
    source venv/bin/activate
else
    source venv/bin/activate
fi

# 4. Install Python dependencies
echo ""
echo "📚 Step 4: Installing Python packages..."
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

echo "✅ Dependencies installed"

# 5. Setup environment variables
echo ""
echo "⚙️ Step 5: Configuring environment..."

if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "⚠️ Please update .env file with your credentials"
fi

# 6. Initialize database
echo ""
echo "🗄️ Step 6: Initializing database tables..."

python database/init_db.py

echo "✅ Database initialized"

# 7. Create necessary directories
echo ""
echo "📁 Step 7: Creating data directories..."

mkdir -p ml_models/saved_models
mkdir -p reports
mkdir -p logs

echo "✅ Directories created"

echo ""
echo "✅ Setup Complete!"
echo ""
echo "🚀 To start the application:"
echo "   1. Backend (in one terminal):"
echo "      source venv/bin/activate"
echo "      python -m uvicorn backend.main:app --reload --port 8000"
echo ""
echo "   2. Frontend (in another terminal):"
echo "      source venv/bin/activate"
echo "      streamlit run app.py"
echo ""
echo "   3. Access the app at: http://localhost:8501"
echo ""
