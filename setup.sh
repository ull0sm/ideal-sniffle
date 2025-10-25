#!/bin/bash

# Setup script for Boeing India Career Chatbot

echo "🚀 Setting up Boeing India Career Chatbot..."

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $python_version"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p .streamlit chroma_db data logs

# Copy configuration files if they don't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env with your credentials"
else
    echo "✓ .env file already exists"
fi

if [ ! -f ".streamlit/secrets.toml" ]; then
    echo "📝 Creating Streamlit secrets file from template..."
    cp .streamlit/secrets.toml.example .streamlit/secrets.toml
    echo "⚠️  Please edit .streamlit/secrets.toml with your credentials"
else
    echo "✓ Streamlit secrets file already exists"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env with your credentials (Google OAuth, API keys, etc.)"
echo "2. Edit .streamlit/secrets.toml with your credentials"
echo "3. Run the application: streamlit run app.py"
echo ""
echo "For Docker deployment:"
echo "  docker-compose up -d"
echo ""
