# AI Poet Roulette

<div align="center">

[![Python 3.12.8](https://img.shields.io/badge/python-3.12.8-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![LangChain](https://img.shields.io/badge/LangChain-🦜-green.svg)](https://langchain.com/)
[![Google Gemini](https://img.shields.io/badge/Google-Gemini-orange.svg)](https://ai.google.dev/)


[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Methodology](#-methodology) • [Examples](#-examples)

</div>

---

## 📖 Overview

This project is a multi-agent system that creates high-quality, factually-grounded poetry from various document types. Using a collaborative approach, two AI poets (Google Gemini and Groq Llama) work together to generate verses, while a third judge agent evaluates the results using comprehensive literary criteria.

### ✨ Key Highlights

- **🤝 Multi-Agent Collaboration**: Two AI models work together, alternating verses
- **📚 Factual Grounding**: All poetry is based on actual document content via RAG (Retrieval-Augmented Generation)
- **🖼️ Advanced Image Analysis**: Supports both text extraction AND visual content analysis from images
- **⚖️ Comprehensive Judging**: Third agent evaluates poems on 5 distinct criteria (100-point scale)
- **🎵 Audio Generation**: Optional text-to-speech output for generated poems
- **📄 Multiple Formats**: PDF, DOCX, TXT, and images (PNG, JPG, JPEG)

---

## 🎯 Features

### Document Processing
- ✅ **PDF** - Extract text from academic papers, reports, articles
- ✅ **DOCX/DOC** - Process Word documents
- ✅ **TXT** - Plain text files
- ✅ **Images** - PNG, JPG, JPEG with dual analysis:
  - OCR text extraction
  - AI vision-based visual content analysis

### Multi-Agent System
- **🌟 Google Poet** (Gemini 2.5 Flash) - Generates odd-numbered verses
- **⚡ Groq Poet** (Llama 3.3 70B) - Generates even-numbered verses
- **⚖️ Judge Agent** (Gemini Flash) - Evaluates and scores both poems

### Advanced Capabilities
- 🔍 Semantic search using FAISS vector store
- 🎨 Collaborative verse generation with context awareness
- 📊 Detailed scoring across 5 literary criteria
- 🎧 Audio output generation (MP3 format)
- 💾 JSON and text output formats
- 🖼️ Comprehensive image understanding (text + visual elements)

---

## 🚀 Installation

### Prerequisites

- **Python**: 3.12.8 (recommended)
- **Operating System**: Windows, macOS, or Linux
- **Storage**: ~500MB for models and dependencies
- **Internet**: Required for initial setup and API calls

### Step 1: Clone Repository

```bash
git clone https://github.com/PrioAhmed19/AI-Poet-Roulette.git
cd ai-poem-generator
```

### Step 2: Install External Tools

#### Tesseract OCR (Required for image processing)

##### Windows
1. Download the installer from: https://github.com/UB-Mannheim/tesseract/wiki
2. Run the installer (e.g., `tesseract-ocr-w64-setup-5.3.3.20231005.exe`)
3. **IMPORTANT**: During installation, note the installation path (default: `C:\Program Files\Tesseract-OCR`)
4. Add to System PATH:
   - Right-click "This PC" → Properties → Advanced system settings
   - Click "Environment Variables"
   - Under "System variables", find and select "Path"
   - Click "Edit" → "New"
   - Add: `C:\Program Files\Tesseract-OCR`
   - Click OK on all dialogs
5. **Verify installation**:
   ```cmd
   tesseract --version
   ```

##### macOS
```bash
brew install tesseract
```

##### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr
```

#### FFmpeg (Required for audio generation)

##### Windows
1. Download from: https://www.gyan.dev/ffmpeg/builds/
2. Download "ffmpeg-release-essentials.zip"
3. Extract to `C:\ffmpeg`
4. Add to System PATH:
   - Follow same steps as Tesseract
   - Add: `C:\ffmpeg\bin`
5. **Verify installation**:
   ```cmd
   ffmpeg -version
   ```

##### macOS
```bash
brew install ffmpeg
```

##### Linux (Ubuntu/Debian)
```bash
sudo apt-get install ffmpeg
```

### Step 3: Python Environment Setup

#### Using Setup Scripts (Optional)

**Linux/macOS**:
```bash
chmod +x setup.sh
./setup.sh
```

**Windows**:
```cmd
setup.bat
```

#### Manual Setup (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

### Step 4: Configure API Keys

1. Copy the environment template:
```bash
cp .env.example .env
```

2. Edit `.env` file with your API keys:

```env
# Google Gemini API Key (FREE)
GOOGLE_API_KEY=your_actual_google_key_here

# Groq API Key (FREE)
GROQ_API_KEY=your_actual_groq_key_here
```

#### Getting API Keys

##### Google Gemini API Key (Free Tier)
1. Visit: https://makersuite.google.com/app/apikey
2. Sign in with Google account
3. Click "Create API Key"
4. Copy the key (starts with `AIza...`)
5. Paste into `.env` file

**Free Tier Limits**:
- 60 requests per minute
- 1,500 requests per day
- Sufficient for most use cases

##### Groq API Key (Free Tier)
1. Visit: https://console.groq.com/
2. Sign up / Log in
3. Navigate to "API Keys" section
4. Click "Create API Key"
5. Copy the key (starts with `gsk_...`)
6. Paste into `.env` file

**Free Tier Limits**:
- Very generous (14,400 requests per day)
- Fast inference speeds

### Step 5: Verify Installation

```bash
# Activate environment if not already active
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows

# Run test suite
python test_system.py
```

You should see:
```
✅ All tests passed! System is ready.
```

---

## 💻 Usage

### Basic Usage

```bash
# Generate poem from a document
python main.py path/to/document.pdf
```

## 📁 Project Structure

```
ai-poem-generator/
│
├── main.py                    # CLI application entry point
├── config.py                  # Configuration and API settings
├── document_processor.py      # Document parsing (PDF, DOCX, TXT, images)
├── vector_store_manager.py    # FAISS vector store operations
├── poem_agents.py             # AI agents (Google, Groq, Judge)
├── poem_workflow.py           # LangGraph workflow orchestration
├── audio_generator.py         # Text-to-speech generation
│
├── example_script.py          # Programmatic usage examples
├── test_system.py             # System verification tests
│
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables (create from .env.example)
├── .gitignore                 # Git ignore rules
│
├── setup.sh                   # Linux/macOS setup script
├── setup.bat / windows_setup.txt  # Windows setup script
│
├── readme.md                  # This file
├── quickstart_guide.md        # Quick start instructions
│
├── sample_ai_article.txt      # Sample document for testing
│
├── results/                   # Output directory (auto-created)
│   ├── poems.txt             # Human-readable output
│   └── poem_results.json     # Structured JSON output
│
├── audio_outputs/             # Audio files (auto-created if --audio used)
│   ├── poem_google.mp3       # Google poet's poem
│   ├── poem_groq.mp3         # Groq poet's poem
│   └── judgment.mp3          # Judgment audio
│
├── faiss_index/              # Vector store persistence (auto-created)
│   └── poem_knowledge_base/  # FAISS index files
│
└── venv/                     # Virtual environment (created during setup)
```

### Core Files Explanation

| File | Purpose |
|------|---------|
| `main.py` | Command-line interface and orchestration |
| `config.py` | API keys, model settings, paths configuration |
| `document_processor.py` | Extracts text from PDF, DOCX, TXT, and images |
| `vector_store_manager.py` | Manages FAISS vector database operations |
| `poem_agents.py` | Three AI agents: Google Poet, Groq Poet, Judge |
| `poem_workflow.py` | LangGraph state machine for collaborative generation |
| `audio_generator.py` | Text-to-speech using gTTS |
| `example_script.py` | Code examples for programmatic usage |
| `test_system.py` | Automated tests to verify installation |

---




## 🏗️ Methodology

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    DOCUMENT PROCESSING                       │
│  PDF/DOCX/TXT/Image → Text Extraction → Chunking → Embedding│
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                   FAISS VECTOR STORE                         │
│         Semantic Search & Retrieval (RAG Pipeline)           │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              COLLABORATIVE POEM GENERATION                   │
│                                                              │
│  Round 1: Google Poet → Verse 1 (with fact retrieval)       │
│  Round 2: Groq Poet   → Verse 2 (with context + verse 1)    │
│  Round 3: Google Poet → Verse 3 (with context + verses 1-2) │
│  ...continues until N verses generated                       │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                    JUDGING & EVALUATION                      │
│                                                              │
│  Judge Agent analyzes both poems:                           │
│  • Factual Accuracy (30%)                                   │
│  • Literary Quality (25%)                                   │
│  • Coherence (20%)                                          │
│  • Creativity (15%)                                         │
│  • Rhythm & Sound (10%)                                     │
│                                                              │
│  Output: Scores, Winner, Detailed Justification             │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                   OUTPUT GENERATION                          │
│  • poems.txt (human-readable)                               │
│  • poem_results.json (structured data)                      │
│  • Audio files (optional MP3s)                              │
└─────────────────────────────────────────────────────────────┘
```

### Workflow Details

#### Phase 1: Document Processing
1. **Input Handling**: Accept PDF, DOCX, TXT, or image file
2. **Text Extraction**:
   - For text documents: Direct extraction
   - For images: Dual approach
     - AI Vision API: Analyzes visual content comprehensively
     - OCR (Tesseract): Extracts any embedded text
3. **Chunking**: Split text into semantically meaningful chunks (500 chars with 50-char overlap)
4. **Embedding**: Convert chunks to vector embeddings using HuggingFace model (all-MiniLM-L6-v2)
5. **Storage**: Store in FAISS vector database for fast retrieval

#### Phase 2: Collaborative Generation
Using LangGraph state machine:

```python
State = {
    context: str,              # Original context/theme
    google_verses: List[str],  # Verses from Google Poet
    groq_verses: List[str],    # Verses from Groq Poet
    current_verse_count: int,  # Progress tracker
    total_verses: int,         # Target verse count
    judgment: dict,            # Final evaluation
    phase: str                 # Current workflow phase
}
```

**Generation Loop**:
```
START → Google generates verse 1
     ↓
     → Groq generates verse 2 (sees verse 1)
     ↓
     → Google generates verse 3 (sees verses 1-2)
     ↓
     → Groq generates verse 4 (sees verses 1-3)
     ↓
     ... continues until N verses reached
     ↓
     → JUDGE evaluates both poems
     ↓
     END
```

Each agent:
1. Retrieves 2-4 relevant chunks from vector store
2. Considers all previously generated verses
3. Generates one verse grounded in facts
4. Maintains thematic and rhythmic consistency

#### Phase 3: Judging Framework

The judge agent uses a comprehensive 100-point scale:

| Criterion | Points | Description |
|-----------|--------|-------------|
| **Factual Accuracy** | 30 | Grounded in source material, no hallucinations |
| **Literary Quality** | 25 | Metaphors, imagery, emotional resonance |
| **Coherence** | 20 | Flow, consistency, thematic unity |
| **Creativity** | 15 | Originality, fresh perspective |
| **Rhythm & Sound** | 10 | Musicality, phonetic appeal |

**Judging Process**:
1. Retrieve original facts from vector store
2. Analyze both poems against criteria
3. Assign scores for each criterion
4. Calculate totals and determine winner
5. Generate detailed justification

---


### Command-Line Options

```
python main.py <document> [options]

Positional Arguments:
  document              Path to input document (PDF, DOCX, TXT, or image)

Optional Arguments:
  --verses N            Number of verses to generate (default: 6)
  --context TEXT        Custom theme/context for the poem
  --audio               Generate audio output (MP3 files)
  --output DIR          Output directory (default: results)
  -h, --help           Show help message
```

### Examples

#### Example 1: Basic PDF Processing
```bash
python main.py research_paper.pdf
```

**Output**:
- `results/poems.txt` - Formatted poems and judgment
- `results/poem_results.json` - Structured data

#### Example 2: Image with Custom Context
```bash
python main.py nature_photo.jpg --context "The serenity of mountain landscapes" --verses 8
```

**Features**:
- AI vision analyzes visual elements
- OCR extracts any text in image
- Generates 8 verses on specified theme

#### Example 3: Audio Generation
```bash
python main.py article.docx --audio --verses 10
```

**Output**:
- Text files (as above)
- `audio_outputs/poem_google.mp3` - Google poet's poem
- `audio_outputs/poem_groq.mp3` - Groq poet's poem
- `audio_outputs/judgment.mp3` - Judgment results

#### Example 4: Custom Output Directory
```bash
python main.py story.txt --verses 12 --output my_poems --audio
```

Creates outputs in `my_poems/` directory instead of default `results/`

### Programmatic Usage

```python
from document_processor import DocumentProcessor
from vector_store_manager import VectorStoreManager
from poem_workflow import PoemWorkflow
from audio_generator import AudioGenerator

# 1. Process document
processor = DocumentProcessor()
documents = processor.process_document("article.pdf")

# 2. Setup vector store
vector_store = VectorStoreManager()
vector_store.add_documents(documents)
retriever = vector_store.get_retriever()

# 3. Generate poems
workflow = PoemWorkflow(retriever, num_verses=8)
results = workflow.run("Theme: Innovation in AI")

# 4. Access results
google_poem = results["google_poem"]["verses"]
groq_poem = results["groq_poem"]["verses"]
judgment = results["judgment"]

print(f"Winner: {judgment['winner']}")
print(f"Score: {judgment['total_a']} vs {judgment['total_b']}")

# 5. Generate audio (optional)
audio_gen = AudioGenerator()
audio_path = audio_gen.generate_poem_audio(
    google_poem, 
    "my_poem",
    "Google Poet"
)
```

See `example_script.py` for more comprehensive examples.

---

## 📊 Output Structure

### Directory Layout

```
project_root/
├── results/                    # Default output directory
│   ├── poems.txt              # Human-readable poems
│   └── poem_results.json      # Structured data
├── audio_outputs/             # Audio files (if --audio)
│   ├── poem_google.mp3
│   ├── poem_groq.mp3
│   └── judgment.mp3
└── faiss_index/              # Vector store (persistent)
    └── poem_knowledge_base/
```

### Sample Output

#### poems.txt
```
============================================================
COLLABORATIVE POEM GENERATION RESULTS
============================================================

Source: research_paper.pdf
Context: The evolution of artificial intelligence...

------------------------------------------------------------
POEM A - Google Poet (Gemini)
------------------------------------------------------------
1. In silicon minds where neurons dance and flow
2. Through layers deep where patterns ebb and grow
3. The future speaks in binary sublime
...

------------------------------------------------------------
POEM B - Groq Poet (Llama)
------------------------------------------------------------
1. From data streams emerge the thoughts of steel
2. Intelligence that learns to think and feel
3. A revolution written line by line
...

============================================================
JUDGMENT
============================================================
POEM A SCORES:
Factual Accuracy: 28/30
Literary Quality: 23/25
Coherence: 18/20
Creativity: 13/15
Rhythm & Sound: 9/10
TOTAL: 91/100

POEM B SCORES:
Factual Accuracy: 27/30
Literary Quality: 22/25
Coherence: 19/20
Creativity: 14/15
Rhythm & Sound: 8/10
TOTAL: 90/100

WINNER: Poem A

JUSTIFICATION:
Poem A demonstrates slightly superior factual grounding...
```

#### poem_results.json
```json
{
  "context": "The evolution of artificial intelligence...",
  "google_poem": {
    "agent": "Google Poet (Gemini)",
    "verses": [
      "In silicon minds where neurons dance and flow",
      "Through layers deep where patterns ebb and grow",
      ...
    ]
  },
  "groq_poem": {
    "agent": "Groq Poet (Llama)",
    "verses": [...]
  },
  "judgment": {
    "winner": "Poem A",
    "total_a": 91,
    "total_b": 90,
    "full_judgment": "..."
  },
  "metadata": {
    "source_file": "research_paper.pdf",
    "is_image": false,
    "is_vision_based": false,
    "context_length": 2847,
    "num_verses": 6
  }
}
```

---

## 🔧 Troubleshooting

### Common Issues

#### "tesseract is not recognized" (Windows)
**Problem**: Tesseract not in PATH

**Solution**:
1. Verify installation: `where tesseract`
2. If not found, add to PATH:
   - Find Tesseract directory (usually `C:\Program Files\Tesseract-OCR`)
   - Add to System PATH (see installation instructions)
   - Restart terminal/IDE
3. Verify: `tesseract --version`

#### "ffmpeg not found" (All platforms)
**Problem**: FFmpeg not installed or not in PATH

**Solution**:
- **Windows**: Follow installation instructions above, ensure `ffmpeg.exe` is in PATH
- **macOS**: `brew install ffmpeg`
- **Linux**: `sudo apt-get install ffmpeg`

#### "API key not valid"
**Problem**: Incorrect or missing API keys

**Solution**:
1. Check `.env` file exists in project root
2. Verify keys have no quotes, spaces, or extra characters
3. Test keys in respective dashboards:
   - Google: https://makersuite.google.com/
   - Groq: https://console.groq.com/
4. Ensure keys haven't expired
5. Check API usage limits

#### "Module not found" errors
**Problem**: Missing Python packages

**Solution**:
```bash
# Activate virtual environment
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate  # Windows

# Reinstall dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

#### "Vector store is empty"
**Problem**: No documents processed

**Solution**:
- Ensure document exists and is readable
- Check file permissions
- Verify file format is supported
- Check document actually contains text

#### Image processing fails
**Problem**: OCR or vision analysis not working

**Solution**:
1. Verify Tesseract installed: `tesseract --version`
2. Check Google API key is valid
3. Ensure image file is not corrupted
4. Try different image format (convert to PNG/JPG)

### Performance Tips

1. **Faster Generation**: Use fewer verses (`--verses 4`)
2. **Better Quality**: More verses provide better context (`--verses 12`)
3. **Reduce API Costs**: Process multiple documents in batch
4. **Reuse Vector Store**: FAISS index persists between runs

---


## 🎓 Technical Details

### Technologies Used

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Framework** | LangChain, LangGraph | Workflow orchestration |
| **LLMs** | Google Gemini, Groq Llama | Poem generation |
| **Embeddings** | HuggingFace (all-MiniLM-L6-v2) | Text vectorization |
| **Vector Store** | FAISS | Semantic search |
| **OCR** | Tesseract | Text extraction from images |
| **Vision** | Google Gemini Vision | Image understanding |
| **TTS** | gTTS | Audio generation |
| **Document Processing** | PyPDF2, python-docx, Pillow | Multi-format support |

### Model Information

**Google Gemini 2.5 Flash**:
- Fast, efficient, excellent for creative writing
- Context window: 1M tokens
- Temperature: 0.8 (creative balance)

**Groq Llama 3.3 70B**:
- Extremely fast inference
- Strong reasoning capabilities
- Temperature: 0.8 (creative balance)

**Judge Model (Gemini Flash)**:
- Better reasoning for evaluation
- Temperature: 0.3 (more deterministic)
- Comprehensive analysis capabilities

### Embedding Model

**all-MiniLM-L6-v2**:
- Dimensions: 384
- Speed: ~14,000 sentences/second
- Quality: Good balance of speed and accuracy
- Size: ~90MB

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.


## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙏 Acknowledgments

- **LangChain** for the powerful framework
- **Google** for Gemini API access
- **Groq** for fast inference
- **HuggingFace** for embedding models
- **Meta** for Llama models

---

## 📧 Contact

For questions, issues, or suggestions:
- Open an issue on GitHub
- Email: prioahmedcr@gmail.com

---
