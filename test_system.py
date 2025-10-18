"""
Test script to verify system setup and functionality.
Run this after setup to ensure everything is working.
"""

import os
import sys
from pathlib import Path


def test_imports():
    """Test if all required packages can be imported."""
    print("\n🧪 Testing imports...")
    packages = [
        ("langchain", "langchain"),
        ("langgraph", "langgraph"),
        ("langchain_google_genai", "langchain-google-genai"),
        ("langchain_groq", "langchain-groq"),
        ("sentence_transformers", "sentence-transformers"),
        ("faiss", "faiss-cpu"),
        ("PyPDF2", "PyPDF2"),
        ("docx", "python-docx"),
        ("PIL", "Pillow"),
        ("pytesseract", "pytesseract"),
        ("gtts", "gTTS"),
        ("pydub", "pydub"),
    ]
    
    failed = []
    for module, package in packages:
        try:
            __import__(module)
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package} - FAILED")
            failed.append(package)
    
    if failed:
        print(f"\n❌ Failed imports: {', '.join(failed)}")
        print("   Run: pip install " + " ".join(failed))
        return False
    else:
        print("✅ All packages imported successfully")
        return True


def test_environment():
    """Test if environment variables are set."""
    print("\n🔐 Testing environment variables...")
    required_vars = [
        "GOOGLE_API_KEY",
        "GROQ_API_KEY"
    ]
    
    from dotenv import load_dotenv
    load_dotenv()
    
    missing = []
    for var in required_vars:
        value = os.getenv(var)
        if value and value != f"your_{var.lower()}_here":
            print(f"  ✅ {var}")
        else:
            print(f"  ❌ {var} - NOT SET")
            missing.append(var)
    
    if missing:
        print(f"\n❌ Missing variables: {', '.join(missing)}")
        print("   Edit your .env file and add these values")
        return False
    else:
        print("✅ All environment variables set")
        return True


def test_external_tools():
    """Test if external tools are available."""
    print("\n🔧 Testing external tools...")
    
    import subprocess
    
    tools = {
        "tesseract": "Tesseract OCR (for image processing)",
        "ffmpeg": "FFmpeg (for audio processing)"
    }
    
    all_ok = True
    for tool, description in tools.items():
        try:
            subprocess.run([tool, "--version"], 
                          stdout=subprocess.PIPE, 
                          stderr=subprocess.PIPE,
                          check=True)
            print(f"  ✅ {tool} - {description}")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print(f"  ⚠️  {tool} - NOT FOUND (optional)")
            print(f"     {description}")
            # Don't fail test for optional tools
    
    print("✅ External tools check complete")
    return True


def test_module_imports():
    """Test if custom modules can be imported."""
    print("\n📦 Testing custom modules...")
    
    modules = [
        "config",
        "document_processor",
        "vector_store_manager",
        "poem_agents",
        "poem_workflow",
        "audio_generator"
    ]
    
    failed = []
    for module in modules:
        try:
            __import__(module)
            print(f"  ✅ {module}.py")
        except Exception as e:
            print(f"  ❌ {module}.py - {str(e)}")
            failed.append(module)
    
    if failed:
        print(f"\n❌ Failed modules: {', '.join(failed)}")
        return False
    else:
        print("✅ All custom modules imported successfully")
        return True


def test_embedding_model():
    """Test if embedding model can be loaded."""
    print("\n🤖 Testing embedding model...")
    
    try:
        from langchain_huggingface import HuggingFaceEmbeddings
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        
        # Test embedding
        test_text = "This is a test sentence."
        embedding = embeddings.embed_query(test_text)
        
        print(f"  ✅ Model loaded (embedding dim: {len(embedding)})")
        return True
    except Exception as e:
        print(f"  ❌ Failed to load model: {str(e)}")
        return False


def test_google_api():
    """Test Google API connection."""
    print("\n🌐 Testing Google API...")
    
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        from config import GOOGLE_API_KEY, GOOGLE_MODEL
        
        if not GOOGLE_API_KEY or GOOGLE_API_KEY == "your_google_api_key_here":
            print("  ⚠️  Google API key not set")
            return False
        
        llm = ChatGoogleGenerativeAI(
            model=GOOGLE_MODEL,
            google_api_key=GOOGLE_API_KEY,
            temperature=0.1
        )
        
        response = llm.invoke("Say 'test successful' in exactly those words")
        print(f"  ✅ API connected")
        print(f"     Response: {response.content[:50]}...")
        return True
    except Exception as e:
        print(f"  ❌ Failed: {str(e)}")
        return False


def test_groq_api():
    """Test Groq API connection."""
    print("\n⚡ Testing Groq API...")
    
    try:
        from langchain_groq import ChatGroq
        from config import GROQ_API_KEY, GROQ_MODEL
        
        if not GROQ_API_KEY or GROQ_API_KEY == "your_groq_api_key_here":
            print("  ⚠️  Groq API key not set")
            return False
        
        llm = ChatGroq(
            groq_api_key=GROQ_API_KEY,
            model_name=GROQ_MODEL,
            temperature=0.1
        )
        
        response = llm.invoke("Say 'test successful' in exactly those words")
        print(f"  ✅ API connected")
        print(f"     Response: {response.content[:50]}...")
        return True
    except Exception as e:
        print(f"  ❌ Failed: {str(e)}")
        return False


def test_faiss_vector_store():
    """Test FAISS vector store."""
    print("\n💾 Testing FAISS vector store...")
    
    try:
        from vector_store_manager import VectorStoreManager
        from langchain_core.documents import Document
        
        # Create test documents
        test_docs = [
            Document(page_content="Test document 1", metadata={"source": "test"}),
            Document(page_content="Test document 2", metadata={"source": "test"})
        ]
        
        # Initialize vector store
        vector_store = VectorStoreManager()
        vector_store.add_documents(test_docs)
        
        # Test retrieval
        retriever = vector_store.get_retriever()
        results = vector_store.similarity_search("Test", k=1)
        
        print(f"  ✅ FAISS index created and tested")
        print(f"     Found {len(results)} similar documents")
        
        # Clean up
        vector_store.delete()
        
        return True
    except Exception as e:
        print(f"  ❌ Failed: {str(e)}")
        return False


def test_document_processing():
    """Test document processing with sample text."""
    print("\n📄 Testing document processing...")
    
    try:
        from document_processor import DocumentProcessor
        
        # Create a temporary test file
        test_file = "test_document.txt"
        with open(test_file, 'w') as f:
            f.write("This is a test document for the AI poem generator. "
                   "It contains sample text to verify document processing works correctly.")
        
        processor = DocumentProcessor()
        documents = processor.process_document(test_file)
        
        # Clean up
        os.remove(test_file)
        
        print(f"  ✅ Processed {len(documents)} chunks")
        return True
    except Exception as e:
        print(f"  ❌ Failed: {str(e)}")
        return False


def create_sample_document():
    """Create a sample document for testing."""
    print("\n📝 Creating sample document...")
    
    sample_text = """The Evolution of Artificial Intelligence

Artificial intelligence has transformed dramatically over the past decades.
From simple rule-based systems to sophisticated neural networks, AI has 
evolved to solve increasingly complex problems.

Machine learning algorithms now power applications ranging from image 
recognition to natural language processing. Deep learning models can 
understand context, generate creative content, and even engage in 
meaningful conversations.

The future of AI holds immense potential. As computational power increases
and algorithms become more refined, we may witness breakthroughs in areas
like scientific discovery, medical diagnosis, and creative arts.

However, this progress also brings important questions about ethics, 
transparency, and the role of AI in society. Balancing innovation with
responsibility remains a crucial challenge for the field."""
    
    sample_file = "sample_ai_article.txt"
    with open(sample_file, 'w') as f:
        f.write(sample_text)
    
    print(f"  ✅ Created: {sample_file}")
    print(f"     Use this for testing: python main.py {sample_file}")
    return sample_file


def run_all_tests():
    """Run all tests and provide summary."""
    print("="*60)
    print("🧪 AI POEM GENERATOR - SYSTEM TEST")
    print("="*60)
    
    tests = [
        ("Package Imports", test_imports),
        ("Environment Variables", test_environment),
        ("External Tools", test_external_tools),
        ("Custom Modules", test_module_imports),
        ("Embedding Model", test_embedding_model),
        ("Google API", test_google_api),
        ("Groq API", test_groq_api),
        ("FAISS Vector Store", test_faiss_vector_store),
        ("Document Processing", test_document_processing),
    ]
    
    results = {}
    for name, test_func in tests:
        try:
            results[name] = test_func()
        except Exception as e:
            print(f"\n❌ {name} failed with exception: {str(e)}")
            results[name] = False
    
    # Summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status:12} {name}")
    
    print(f"\n{'='*60}")
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✨ All tests passed! System is ready.")
        print("\nNext steps:")
        print("1. Try: python main.py sample_ai_article.txt")
        print("2. Or: python example_usage.py")
        
        # Create sample document
        sample_file = create_sample_document()
        
    else:
        print("⚠️  Some tests failed. Please fix the issues above.")
        print("\nCommon fixes:")
        print("- Missing packages: pip install -r requirements.txt")
        print("- Missing API keys: Edit .env file")
        print("- Missing tools: See README.md for installation")
    
    print("="*60)
    
    return passed == total


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)