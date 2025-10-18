# Quick Start Guide

Get your AI Poem Generator up and running in 5 minutes!

## Prerequisites

✅ Python 3.12.8 installed  
✅ pip package manager  
✅ Internet connection for API calls

## Step 1: Clone and Setup (2 minutes)

```bash
# Clone or download the project
cd ai-poem-generator

# Run setup script
# Linux/macOS:
chmod +x setup.sh
./setup.sh

# Windows:
setup.bat
```

## Step 2: Get API Keys (2 minutes)

### Google API Key (FREE)
1. Visit: https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Copy the key

### Groq API Key (FREE)
1. Visit: https://console.groq.com/
2. Sign up / Log in
3. Go to API Keys section
4. Create new key and copy it

### AstraDB Credentials (FREE TIER)
1. Visit: https://astra.datastax.com/
2. Create account and new database
3. Get Application Token and Database ID from settings

## Step 3: Configure (30 seconds)

Edit the `.env` file:

```env
GOOGLE_API_KEY=your_actual_google_key_here
GROQ_API_KEY=your_actual_groq_key_here
ASTRA_DB_APPLICATION_TOKEN=AstraCS:...
ASTRA_DB_ID=your-database-id
```

## Step 4: Test Installation (30 seconds)

```bash
# Activate environment
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate.bat  # Windows

# Run tests
python test_system.py
```

You should see all tests passing! ✅

## Step 5: Generate Your First Poem! (1 minute)

```bash
# The test script creates a sample file for you
python main.py sample_ai_article.txt
```

Output:
- Console: See poems and judgment in real-time
- Files: `results/poems.txt` and `results/poem_results.json`

### With Audio Output

```bash
python main.py sample_ai_article.txt --audio
```

Audio files saved to: `audio_outputs/`

## Common Commands

```bash
# Basic usage
python main.py document.pdf

# With custom options
python main.py document.pdf --verses 10 --audio

# Custom context/theme
python main.py image.jpg --context "Nature and beauty" --audio

# Specify output directory
python main.py article.docx --output my_poems --verses 8
```

## Supported File Types

- ✅ PDF (`.pdf`)
- ✅ Word Documents (`.docx`, `.doc`)
- ✅ Text Files (`.txt`)
- ✅ Images (`.png`, `.jpg`, `.jpeg`) - Requires Tesseract OCR

## Example Workflow

```bash
# 1. Process a research paper
python main.py research.pdf --verses 12 --audio

# 2. Check results
cat results/poems.txt

# 3. Listen to audio
# Open audio_outputs/poem_google.mp3
# Open audio_outputs/poem_groq.mp3
# Open audio_outputs/judgment.mp3

# 4. Review JSON for structured data
cat results/poem_results.json
```

## Troubleshooting

### "Module not found" errors
```bash
pip install -r requirements.txt
```

### "API key not valid"
- Check your `.env` file
- Make sure keys are correct (no quotes, no extra spaces)
- Verify keys are active in respective dashboards

### "Tesseract not found" (for images)
```bash
# Ubuntu/Debian
sudo apt-get install tesseract-ocr

# macOS
brew install tesseract

# Windows
# Download from: https://github.com/UB-Mannheim/tesseract/wiki
```

### "AstraDB connection failed"
- Verify database is active in AstraDB console
- Check token hasn't expired
- Ensure database ID is correct

## What Happens When You Run?

1. **Document Processing**: Extracts text from your file
2. **Vector Store**: Stores chunks in AstraDB for retrieval
3. **Poem Generation**: 
   - Google Poet generates verse 1
   - Groq Poet generates verse 2
   - Alternates until complete
4. **Judging**: Judge agent evaluates both poems
5. **Output**: Results saved as text, JSON, and audio

## Understanding the Output

### Judgment Criteria (100 points total)

| Criterion | Weight | What It Measures |
|-----------|--------|------------------|
| Factual Accuracy | 30% | Grounded in source material |
| Literary Quality | 25% | Metaphors, imagery, devices |
| Coherence | 20% | Flow and connection |
| Creativity | 15% | Originality |
| Rhythm & Sound | 10% | Musicality |

### Example Output Structure

```
results/
├── poems.txt           # Human-readable poems and judgment
├── poem_results.json   # Structured data with scores
└── [if --audio]
    ├── poem_google.mp3
    ├── poem_groq.mp3
    └── judgment.mp3
```

## Advanced Usage

### Programmatic Use

```python
from document_processor import DocumentProcessor
from vector_store_manager import VectorStoreManager
from poem_workflow import PoemWorkflow

# Process document
processor = DocumentProcessor()
documents = processor.process_document("article.pdf")

# Setup vector store
vector_store = VectorStoreManager()
vector_store.add_documents(documents)
retriever = vector_store.get_retriever()

# Generate poems
workflow = PoemWorkflow(retriever, num_verses=8)
results = workflow.run("The wonders of space exploration")

# Access results
print(results["google_poem"]["verses"])
print(results["judgment"]["winner"])
```

See `example_usage.py` for more examples!

## Performance Tips

1. **Faster Generation**: Reduce `--verses` count
2. **Better Quality**: Increase verses for more context
3. **Batch Processing**: Process multiple documents sequentially
4. **Reuse Vector Store**: Documents persist in AstraDB

## Next Steps

- 📖 Read full `README.md` for detailed documentation
- 🔬 Try `example_usage.py` for more use cases
- 🎨 Experiment with different document types
- 🎵 Generate audio versions of your favorite poems

## Getting Help

1. Run tests: `python test_system.py`
2. Check logs in console output
3. Verify all API keys in `.env`
4. Review `README.md` troubleshooting section

## Have Fun! 🎭

You're all set to generate amazing factually-grounded poems with AI collaboration!

Try different documents, themes, and settings to see what creative results you get.

---

**Quick Reference Card**

```bash
# Setup
./setup.sh                    # Initial setup

# Activate
source venv/bin/activate      # Start working

# Generate
python main.py doc.pdf        # Basic
python main.py doc.pdf --audio # With audio
python main.py doc.pdf --verses 10 # More verses

# Test
python test_system.py         # Verify setup

# Examples
python example_usage.py       # See examples
```
