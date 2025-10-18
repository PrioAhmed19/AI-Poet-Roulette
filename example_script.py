"""
Example usage of the AI Poem Generator system.
This script demonstrates how to use the system programmatically.
"""

from document_processor import DocumentProcessor
from vector_store_manager import VectorStoreManager
from poem_workflow import PoemWorkflow
from audio_generator import AudioGenerator


def example_basic_usage():
    """Basic example: Generate poem from a document."""
    print("="*60)
    print("EXAMPLE 1: Basic Poem Generation")
    print("="*60)
    
    # 1. Process document
    processor = DocumentProcessor()
    documents = processor.process_document("sample_document.pdf")
    print(f"✅ Processed {len(documents)} chunks")
    
    # 2. Setup vector store
    vector_store = VectorStoreManager()
    vector_store.add_documents(documents)
    retriever = vector_store.get_retriever()
    print("✅ Vector store ready")
    
    # 3. Generate poems
    workflow = PoemWorkflow(retriever, num_verses=6)
    results = workflow.run("Exploring the wonders of nature")
    
    # 4. Print results
    print("\n📖 Google's Poem:")
    for i, verse in enumerate(results["google_poem"]["verses"], 1):
        print(f"  {i}. {verse}")
    
    print("\n📖 Groq's Poem:")
    for i, verse in enumerate(results["groq_poem"]["verses"], 1):
        print(f"  {i}. {verse}")
    
    print("\n⚖️  Judgment:")
    print(results["judgment"].get("full_judgment", "No judgment"))
    
    return results


def example_with_audio():
    """Example: Generate poem with audio output."""
    print("\n" + "="*60)
    print("EXAMPLE 2: Poem Generation with Audio")
    print("="*60)
    
    # Generate poem (using previous example)
    results = example_basic_usage()
    
    # Generate audio
    audio_gen = AudioGenerator()
    
    audio_path_a = audio_gen.generate_poem_audio(
        results["google_poem"]["verses"],
        "example_google",
        "Google Poet"
    )
    print(f"🎵 Google audio: {audio_path_a}")
    
    audio_path_b = audio_gen.generate_poem_audio(
        results["groq_poem"]["verses"],
        "example_groq",
        "Groq Poet"
    )
    print(f"🎵 Groq audio: {audio_path_b}")


def example_custom_context():
    """Example: Generate poem with custom context."""
    print("\n" + "="*60)
    print("EXAMPLE 3: Custom Context Poem")
    print("="*60)
    
    # Process document
    processor = DocumentProcessor()
    documents = processor.process_document("tech_article.pdf")
    
    # Setup vector store
    vector_store = VectorStoreManager()
    vector_store.add_documents(documents)
    retriever = vector_store.get_retriever()
    
    # Generate with custom context
    workflow = PoemWorkflow(retriever, num_verses=8)
    results = workflow.run("The evolution of artificial intelligence")
    
    print("\n🎯 Winner:", results["judgment"].get("winner", "Unknown"))
    print("📊 Score A:", results["judgment"].get("total_a", 0))
    print("📊 Score B:", results["judgment"].get("total_b", 0))


def example_judge_only():
    """Example: Use judge agent separately."""
    print("\n" + "="*60)
    print("EXAMPLE 4: Judging Existing Poems")
    print("="*60)
    
    from poem_agents import JudgeAgent
    
    # Setup
    vector_store = VectorStoreManager()
    retriever = vector_store.get_retriever()
    
    # Existing poems
    poem_a = [
        "In circuits deep, where data flows",
        "The silicon mind forever grows",
        "Through layers of neural design"
    ]
    
    poem_b = [
        "Electric thoughts in binary code",
        "Intelligence on digital road",
        "Machine learning's bright cascade"
    ]
    
    # Judge
    judge = JudgeAgent(retriever)
    judgment = judge.judge_verses(
        poem_a,
        poem_b,
        "Artificial intelligence and machine learning"
    )
    
    print("\n" + judgment.get("full_judgment", ""))


def example_iterative_generation():
    """Example: Generate multiple poem variations."""
    print("\n" + "="*60)
    print("EXAMPLE 5: Multiple Poem Variations")
    print("="*60)
    
    processor = DocumentProcessor()
    documents = processor.process_document("story.txt")
    
    vector_store = VectorStoreManager()
    vector_store.add_documents(documents)
    retriever = vector_store.get_retriever()
    
    contexts = [
        "Love and loss",
        "Journey and discovery",
        "Hope and resilience"
    ]
    
    best_score = 0
    best_result = None
    
    for context in contexts:
        print(f"\n🎨 Generating for: {context}")
        workflow = PoemWorkflow(retriever, num_verses=4)
        results = workflow.run(context)
        
        score_a = results["judgment"].get("total_a", 0)
        score_b = results["judgment"].get("total_b", 0)
        max_score = max(score_a, score_b)
        
        print(f"  Best score: {max_score}/100")
        
        if max_score > best_score:
            best_score = max_score
            best_result = results
    
    print(f"\n🏆 Best overall poem scored: {best_score}/100")
    print(f"   Context: {best_result['context'][:50]}...")


def run_all_examples():
    """Run all examples in sequence."""
    examples = [
        ("Basic Usage", example_basic_usage),
        ("With Audio", example_with_audio),
        ("Custom Context", example_custom_context),
        ("Judge Only", example_judge_only),
        ("Iterative Generation", example_iterative_generation)
    ]
    
    print("\n" + "🎭"*30)
    print("AI POEM GENERATOR - EXAMPLES")
    print("🎭"*30 + "\n")
    
    for name, func in examples:
        try:
            print(f"\n▶️  Running: {name}")
            func()
            print(f"✅ {name} completed")
        except Exception as e:
            print(f"❌ {name} failed: {str(e)}")
    
    print("\n" + "="*60)
    print("✨ All examples completed!")
    print("="*60)


if __name__ == "__main__":
    # Run a single example
    example_basic_usage()
    
    # Or run all examples
    # run_all_examples()
