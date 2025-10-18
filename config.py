import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Model configurations
GOOGLE_MODEL = "models/gemini-2.5-flash"  # Free tier model
GROQ_MODEL = "llama-3.3-70b-versatile"  # Fast and free
JUDGE_MODEL = "models/gemini-flash-latest"  # Better reasoning for judging

# Embedding model
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# Vector store settings (FAISS)
VECTOR_STORE_TABLE = "poem_knowledge_base"
FAISS_INDEX_DIR = "faiss_index"  # Directory to store FAISS index
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

# Audio settings
AUDIO_OUTPUT_DIR = "audio_outputs"
AUDIO_LANGUAGE = "en"

# Document processing settings
SUPPORTED_EXTENSIONS = ['.pdf', '.docx', '.doc', '.txt', '.png', '.jpg', '.jpeg']