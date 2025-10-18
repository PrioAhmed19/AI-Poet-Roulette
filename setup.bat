#!/bin/bash

# Setup script for AI Poem Generator
# Compatible with Python 3.12.8

echo "🚀 Setting up AI Poem Generator..."
echo "=================================="

# Check Python version
echo "📌 Checking Python version..."
python_version=$(python --version 2>&1 | awk '{print $2}')
echo "   Found Python: $python_version"

if [[ ! "$python_version" =~ ^3\.12\. ]]; then
    echo "⚠️  Warning: This project is designed for Python 3.12.8"
    echo "   Your version: $python_version"
    read -p "   Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Create virtual environment
echo ""
echo "🐍 Creating virtual environment..."
python -m venv venv

# Activate virtual environment
echo "✅ Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Check for Tesseract
echo ""
echo "🔍 Checking for Tesseract OCR..."
if command -v tesseract &> /dev/null; then
    tesseract_version=$(tesseract --version 2>&1 | head -n 1)
    echo "✅ $tesseract_version"
else
    echo "❌ Tesseract not found!"
    echo "   Install with:"
    echo "   - Ubuntu/Debian: sudo apt-get install tesseract-ocr"
    echo "   - macOS: brew install tesseract"
    echo "   - Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki"
fi

# Check for ffmpeg
echo ""
echo "🔍 Checking for ffmpeg..."
if command -v ffmpeg &> /dev/null; then
    ffmpeg_version=$(ffmpeg -version 2>&1 | head -n 1)
    echo "✅ $ffmpeg_version"
else
    echo "❌ ffmpeg not found!"
    echo "   Install with:"
    echo "   - Ubuntu/Debian: sudo apt-get install ffmpeg"
    echo "   - macOS: brew install ffmpeg"
    echo "   - Windows: Download from https://ffmpeg.org/download.html"
fi

# Setup environment variables
echo ""
echo "🔐 Setting up environment variables..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✅ Created .env file from template"
    echo "⚠️  IMPORTANT: Edit .env and add your API keys!"
    echo ""
    echo "   Required keys:"
    echo "   1. GOOGLE_API_KEY (https://makersuite.google.com/app/apikey)"
    echo "   2. GROQ_API_KEY (https://console.groq.com/)"

else
    echo "✅ .env file already exists"
fi

# Create output directories
echo ""
echo "📁 Creating output directories..."
mkdir -p results
mkdir -p audio_outputs
echo "✅ Directories created"

# Download embedding model
echo ""
echo "🤖 Downloading embedding model (this may take a moment)..."
python -c "from langchain_huggingface import HuggingFaceEmbeddings; HuggingFaceEmbeddings(model_name='all-MiniLM-L6-v2')"
echo "✅ Embedding model ready"

echo ""
echo "=================================="
echo "✨ Setup completed successfully!"
echo "=================================="
echo ""
echo "Next steps:"
echo "1. Edit .env and add your API keys"
echo "2. Run: source venv/bin/activate"
echo "3. Test: python main.py --help"
echo "4. Generate: python main.py your_document.pdf --audio"
echo ""
