# AI Collaborative Poem Generator with Multi-Agent Judging

A multi-agent system that generates factually-grounded literary poems from documents using two AI agents (Google Gemini and Groq Llama), then judges the results with a third agent.

## Features

- 📄 **Document Processing**: Supports PDF, DOCX, TXT, and images (with OCR)
- 🤖 **Multi-Agent Collaboration**: Two AI poets alternate creating verses
- 🎯 **Factual Grounding**: All verses are based on document content via RAG
- ⚖️ **Comprehensive Judging**: Third agent evaluates poems on 5 criteria
- 🎵 **Audio Output**: Optional text-to-speech generation
- 💾 **Vector Store**: AstraDB for semantic search and retrieval

## Architecture

### Part 1: Collaborative Poem Generation
1. **Google Poet** (Gemini 1.5 Flash): Generates odd-numbered verses
2. **Groq Poet** (Llama 3.3 70B): Generates even-numbered verses
3. Both agents retrieve factual context from the document vector store
4. Verses alternate, with each agent seeing previous lines for coherence

### Part 2: Judging Framework
The **Judge Agent** (Gemini 1.5 Pro) evaluates poems using:

| Criterion | Weight | Description |
|-----------|--------|-------------|
| **Factual Accuracy** | 30% | Grounded in source material, no unsupported claims |
| **Literary Quality** | 25% | Metaphors, imagery, literary devices, emotional resonance |
| **Coherence** | 20% | Natural flow, consistent theme, logical progression |
| **Creativity** | 15% | Originality, unique perspective, avoids clichés |
| **Rhythm & Sound** | 10% | Musicality, meter, phonetic appeal |

**Total Score**: 100 points

## Installation

### Prerequisites
- Python 3.12.8
- Tesseract OCR (for image processing)
- ffmpeg (for audio processing)

### Install Tesseract OCR

**Ubuntu/Debian:**
```bash
sudo apt-get install tesseract-ocr
```

**macOS:**
```bash
brew install tesseract
```

**Windows:**
Download from: https://github.com/UB-Mannheim/tesseract/wiki

### Install ffmpeg

**Ubuntu/Debian:**
```bash
sudo apt-get install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
Download from: https://ffmpeg.org/download.html

### Python Setup

1. **Clone the repository:**
```bash
git clone <repository-url>
cd ai-poem-generator
```

2. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables:**
```bash
cp .env.example .env
# Edit .env with your API keys
```

### Get API Keys

1. **Google API Key** (Free):
   - Visit: https://makersuite.google.com/app/apikey
   - Create new API key
   - Add to `.env` as `GOOGLE_API_KEY`

2. **Groq API Key** (Free):
   - Visit: https://console.groq.com/
   - Sign up and get API key
   - Add to `.env` as `GROQ_API_KEY`


## Usage

### Basic Usage

```bash
python main.py path/to/document.pdf
```

### With Custom Options

```bash
python main.py document.pdf --verses 8 --audio --context "Nature and seasons"
```

### Command-Line Arguments

```
positional arguments:
  document              Path to document (PDF, DOCX, TXT, or image)

optional arguments:
  -h, --help           Show help message
  --verses N           Number of verses to generate (default: 6)
  --context TEXT       Custom context/theme (optional)
  --audio              Generate audio output
  --output DIR         Output directory (default: results)
```

## Examples

### Example 1: Generate poem from PDF
```bash
python main.py research_paper.pdf --verses 10 --audio
```

### Example 2: Custom theme from image
```bash
python main.py nature_photo.jpg --context "The beauty of natural landscapes" --audio
```

### Example 3: Process DOCX with specific output
```bash
python main.py story.docx --verses 8 --output my_poems
```

## Output

The system generates:

1. **poems.txt**: Full text of both poems and judgment
2. **poem_results.json**: Structured JSON with all results
3. **Audio files** (if --audio flag used):
   - `poem_google.mp3`: Google poet's poem
   - `poem_groq.mp3`: Groq poet's poem
   - `judgment.mp3`: Judgment results

## Project Structure

```
ai-poem-generator/
├── config.py                 # Configuration and API keys
├── document_processor.py     # Document parsing and extraction
├── vector_store_manager.py   # AstraDB vector store management
├── poem_agents.py            # AI agents (Google, Groq, Judge)
├── poem_workflow.py          # LangGraph workflow orchestration
├── audio_generator.py        # Text-to-speech generation
├── main.py                   # Main CLI application
├── requirements.txt          # Python dependencies
├── .env.example              # Environment variables template
└── README.md                 # This file
```

## How It Works

### Workflow

1. **Document Processing**:
   - Extract text from document (PDF/DOCX/TXT/Image)
   - Split into semantic chunks
   - Store in AstraDB vector store

2. **Poem Generation** (Alternating):
   ```
   Google → Groq → Google → Groq → ... (until N verses)
   ```
   - Each agent retrieves relevant facts
   - Generates verse grounded in facts
   - Sees previous verses for coherence

3. **Judging**:
   - Judge retrieves original facts
   - Evaluates both poems on 5 criteria
   - Assigns scores and declares winner
   - Provides detailed justification

4. **Output Generation**:
   - Save results as JSON and text
   - Generate audio files (optional)

## Judging Criteria Details

### 1. Factual Accuracy (30 points)
- Are verses supported by source document?
- Any factual errors or hallucinations?
- Appropriate use of facts in creative context

### 2. Literary Quality (25 points)
- Use of metaphor, simile, personification
- Vivid imagery and sensory details
- Literary devices (alliteration, assonance, etc.)
- Emotional impact and resonance

### 3. Coherence (20 points)
- Smooth transitions between verses
- Consistent theme and tone
- Logical narrative or thematic progression
- Unity of the poem as a whole

### 4. Creativity (15 points)
- Original expressions and perspectives
- Unexpected but apt word choices
- Avoidance of clichés and overused phrases
- Fresh approach to the subject matter

### 5. Rhythm & Sound (10 points)
- Consistent meter (if intended)
- Pleasant phonetic qualities
- Internal rhyme, alliteration, assonance
- Overall musicality when read aloud

## Troubleshooting

### Issue: "No module named 'cassandra'"
```bash
pip install cassandra-driver
```

### Issue: Tesseract not found
Install Tesseract OCR and add to PATH

### Issue: Audio generation fails
```bash
pip install --upgrade gTTS pydub
```


## Performance Notes

- **Google Gemini**: Fast, good at creative writing
- **Groq Llama**: Very fast inference, strong reasoning
- **Vector Store**: Retrieves 2-4 relevant chunks per verse
- **Audio Generation**: ~2-3 seconds per poem

## Future Enhancements

- [ ] Support for more AI models
- [ ] Real-time streaming of verse generation
- [ ] Web UI interface
- [ ] Multiple poem styles (haiku, sonnet, free verse)
- [ ] Multi-language support
- [ ] Custom judging criteria weights
- [ ] Collaborative refinement rounds

## License

MIT License

## Contributing

Contributions welcome! Please open an issue or pull request.

## Credits

- **LangChain/LangGraph**: Workflow orchestration
- **Google Gemini**: AI model
- **Groq**: Fast inference platform
- **FAISS**: Vector database
- **Hugging Face**: Embedding models

---

Made with ❤️ by AI Poetry Enthusiasts
