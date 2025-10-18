import argparse
import json
import os
from pathlib import Path
from document_processor import DocumentProcessor
from vector_store_manager import VectorStoreManager
from poem_workflow import PoemWorkflow
from audio_generator import AudioGenerator
from langchain_core.documents import Document as LangchainDocument

# For comprehensive image analysis
try:
    import google.generativeai as genai
    from PIL import Image
    VISION_AVAILABLE = True
except ImportError:
    VISION_AVAILABLE = False
    print("⚠️  Vision API not available. Install with: pip install google-generativeai")


def analyze_image_comprehensively(image_path: str, google_api_key: str) -> dict:
    """
    Comprehensive image analysis using Google Gemini Vision API.
    Analyzes BOTH visual content AND extracts any text present.
    
    Args:
        image_path: Path to image file
        google_api_key: Google API key
        
    Returns:
        dict with 'visual_analysis', 'extracted_text', and 'combined_context'
    """
    if not VISION_AVAILABLE:
        return None
        
    try:
        print(f"\n🔍 Performing comprehensive AI image analysis...")
        print("   (Analyzing both visual content AND any text in the image)")
        
        # Configure Gemini
        genai.configure(api_key=google_api_key)
        model = genai.GenerativeModel('models/gemini-2.0-flash-thinking-exp')
        
        # Load image
        image = Image.open(image_path)
        
        # Step 1: Extract any text from the image
        print("  📝 Extracting text from image...")
        text_prompt = """Extract ALL text visible in this image. 
        If there is text, transcribe it exactly as it appears.
        If there is NO text or very minimal text (less than 5 words), simply respond with: [NO TEXT]
        
        Return only the extracted text, nothing else."""
        
        text_response = model.generate_content([text_prompt, image])
        extracted_text = text_response.text.strip()
        
        has_text = extracted_text and "[NO TEXT]" not in extracted_text.upper() and len(extracted_text) > 10
        
        if has_text:
            print(f"  ✅ Found text in image ({len(extracted_text)} characters)")
            print(f"     Preview: {extracted_text[:100]}...")
        else:
            print(f"  ℹ️  No significant text found in image")
            extracted_text = ""
        
        # Step 2: Analyze visual content
        print("  🎨 Analyzing visual content...")
        visual_prompt = """Analyze this image's visual content in detail. Provide a comprehensive description 
        covering:
        
        1. Main subjects, objects, and people (what do you see?)
        2. Setting, environment, and background details
        3. Colors, lighting, and visual mood/atmosphere
        4. Composition, perspective, and spatial arrangement
        5. Actions, events, or narrative elements happening
        6. Notable details, patterns, textures, or symbols
        7. Style and medium (photograph, illustration, artwork, diagram, etc.)
        8. Overall feeling and emotional tone conveyed
        
        Be specific and factual. Describe what IS visible, not interpretations.
        Write 250-350 words in flowing prose suitable for poetry context.
        
        Note: Focus ONLY on visual elements. Do NOT describe any text you see - that's handled separately."""
        
        visual_response = model.generate_content([visual_prompt, image])
        visual_analysis = visual_response.text.strip()
        
        print(f"  ✅ Generated visual analysis ({len(visual_analysis)} characters)")
        
        # Step 3: Combine text and visual analysis
        if has_text:
            combined_context = f"""IMAGE COMPREHENSIVE ANALYSIS:

TEXT CONTENT EXTRACTED FROM IMAGE:
{extracted_text}

VISUAL DESCRIPTION:
{visual_analysis}

This image contains both textual information and rich visual content. The poetry should be grounded in both the extracted text and the visual elements described above."""
        else:
            combined_context = f"""IMAGE COMPREHENSIVE ANALYSIS:

VISUAL DESCRIPTION:
{visual_analysis}

This image is primarily visual without significant text content. The poetry should be grounded in the visual elements and atmosphere described above."""
        
        print(f"\n📄 Combined analysis:")
        print(f"   Text: {len(extracted_text)} chars")
        print(f"   Visual: {len(visual_analysis)} chars")
        print(f"   Total: {len(combined_context)} chars")
        print(f"\nPreview: {combined_context[:200]}...\n")
        
        return {
            "visual_analysis": visual_analysis,
            "extracted_text": extracted_text,
            "combined_context": combined_context,
            "has_text": has_text,
            "image_path": image_path,
            "success": True
        }
        
    except Exception as e:
        print(f"❌ Comprehensive image analysis failed: {e}")
        return {"success": False, "error": str(e)}


def is_image_file(filepath: str) -> bool:
    """Check if file is an image based on extension."""
    image_extensions = {'.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.gif', '.webp'}
    return Path(filepath).suffix.lower() in image_extensions


def print_poem(title: str, agent: str, verses: list):
    """Pretty print a poem."""
    print(f"\n{'='*60}")
    print(f"📖 {title}")
    print(f"✍️  By: {agent}")
    print(f"{'='*60}")
    for i, verse in enumerate(verses, 1):
        print(f"{i}. {verse}")
    print(f"{'='*60}\n")


def print_judgment(judgment: dict):
    """Pretty print judgment results."""
    print(f"\n{'='*60}")
    print("⚖️  JUDGMENT RESULTS")
    print(f"{'='*60}")
    print(judgment.get("full_judgment", "No detailed judgment available"))
    print(f"{'='*60}\n")
    
    if judgment.get("winner"):
        print(f"🏆 WINNER: {judgment['winner']}")
        print(f"📊 Score A: {judgment.get('total_a', 'N/A')}/100")
        print(f"📊 Score B: {judgment.get('total_b', 'N/A')}/100")
    print()


def main():
    parser = argparse.ArgumentParser(
        description="AI Collaborative Poem Generator - Now supports images with OR without text!"
    )
    parser.add_argument(
        "document",
        help="Path to document (PDF, DOCX, TXT, or image - with or without text)"
    )
    parser.add_argument(
        "--verses",
        type=int,
        default=6,
        help="Number of verses to generate (default: 6)"
    )
    parser.add_argument(
        "--context",
        type=str,
        help="Custom context/theme (optional, extracted from document if not provided)"
    )
    parser.add_argument(
        "--audio",
        action="store_true",
        help="Generate audio output"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="results",
        help="Output directory for results (default: results)"
    )
    
    args = parser.parse_args()
    
    # Validate document exists
    if not os.path.exists(args.document):
        print(f"❌ Error: Document not found: {args.document}")
        return
    
    # Create output directory
    os.makedirs(args.output, exist_ok=True)
    
    print("\n🚀 Starting AI Poem Generation System")
    print("="*60)
    
    # Step 1: Process document
    print("\n📄 Step 1: Processing document...")
    processor = DocumentProcessor()
    
    # Check if it's an image - try comprehensive analysis first
    documents = None
    is_vision_based = False
    
    if is_image_file(args.document):
        print("📸 Image detected - attempting comprehensive AI vision analysis...")
        
        # Get Google API key
        from dotenv import load_dotenv
        load_dotenv()
        google_api_key = os.getenv("GOOGLE_API_KEY")
        
        if google_api_key and VISION_AVAILABLE:
            analysis_result = analyze_image_comprehensively(args.document, google_api_key)
            
            if analysis_result and analysis_result.get("success"):
                # Vision analysis successful - use comprehensive analysis
                print("✅ Successfully analyzed image with AI Vision")
                is_vision_based = True
                
                # Create document from comprehensive analysis
                documents = [
                    LangchainDocument(
                        page_content=analysis_result["combined_context"],
                        metadata={
                            "source": args.document,
                            "type": "comprehensive_image_analysis",
                            "has_text": analysis_result["has_text"],
                            "text_length": len(analysis_result["extracted_text"]),
                            "visual_length": len(analysis_result["visual_analysis"])
                        }
                    )
                ]
            else:
                print("⚠️  Vision analysis failed, falling back to OCR...")
        else:
            if not google_api_key:
                print("⚠️  Google API key not found, using OCR only...")
            if not VISION_AVAILABLE:
                print("⚠️  Vision libraries not available, using OCR only...")
    
    # If vision analysis didn't work or not an image, use regular processor
    if documents is None:
        try:
            documents = processor.process_document(args.document)
            print(f"✅ Processed {len(documents)} chunks from document")
        except Exception as e:
            print(f"❌ Error processing document: {str(e)}")
            return
    
    if not documents or len(documents) == 0:
        print("❌ Error: No content could be extracted from document")
        return
    
    # Step 2: Set up vector store
    print("\n💾 Step 2: Setting up knowledge base...")
    try:
        vector_store = VectorStoreManager()
        num_docs = vector_store.add_documents(documents)
        print(f"✅ Added {num_docs} documents to vector store")
        retriever = vector_store.get_retriever()
    except Exception as e:
        print(f"❌ Error setting up vector store: {str(e)}")
        return
    
    # Step 3: Determine context
    if args.context:
        context = args.context
        print(f"\n📝 Using custom context: {context[:100]}...")
    else:
        # Extract context from first chunk
        context = documents[0].page_content
        if len(context) > 500:
            context_preview = context[:500]
        else:
            context_preview = context
        
        print(f"\n📝 Extracted context from document ({len(context)} chars total)")
        if is_vision_based:
            print(f"   Source: AI Vision Analysis (image + text)")
        print(f"   Preview: {context_preview[:200]}...\n")
    
    # Step 4: Generate poems
    print(f"\n🎨 Step 3: Generating collaborative poems...")
    workflow = PoemWorkflow(retriever, num_verses=args.verses)
    
    try:
        results = workflow.run(context)
    except Exception as e:
        print(f"❌ Error generating poems: {str(e)}")
        import traceback
        traceback.print_exc()
        return
    
    # Step 5: Display results
    print("\n" + "="*60)
    print("📊 RESULTS")
    print("="*60)
    
    print_poem(
        "Poem A",
        results["google_poem"]["agent"],
        results["google_poem"]["verses"]
    )
    
    print_poem(
        "Poem B",
        results["groq_poem"]["agent"],
        results["groq_poem"]["verses"]
    )
    
    print_judgment(results["judgment"])
    
    # Step 6: Save results
    print("💾 Saving results...")
    results_file = os.path.join(args.output, "poem_results.json")
    
    # Add metadata
    results["metadata"] = {
        "source_file": args.document,
        "is_image": is_image_file(args.document),
        "is_vision_based": is_vision_based,
        "context_length": len(context),
        "num_verses": args.verses
    }
    
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"✅ Results saved to: {results_file}")
    
    # Save poems as text
    poems_file = os.path.join(args.output, "poems.txt")
    with open(poems_file, 'w', encoding='utf-8') as f:
        f.write("="*60 + "\n")
        f.write("COLLABORATIVE POEM GENERATION RESULTS\n")
        f.write("="*60 + "\n\n")
        
        f.write(f"Source: {args.document}\n")
        if is_vision_based:
            f.write("Method: AI Vision Analysis (Comprehensive)\n")
        f.write(f"Context: {context[:300]}...\n\n")
        
        f.write("-"*60 + "\n")
        f.write(f"POEM A - {results['google_poem']['agent']}\n")
        f.write("-"*60 + "\n")
        for i, verse in enumerate(results["google_poem"]["verses"], 1):
            f.write(f"{i}. {verse}\n")
        
        f.write("\n" + "-"*60 + "\n")
        f.write(f"POEM B - {results['groq_poem']['agent']}\n")
        f.write("-"*60 + "\n")
        for i, verse in enumerate(results["groq_poem"]["verses"], 1):
            f.write(f"{i}. {verse}\n")
        
        f.write("\n" + "="*60 + "\n")
        f.write("JUDGMENT\n")
        f.write("="*60 + "\n")
        f.write(results["judgment"].get("full_judgment", "No judgment available"))
    
    print(f"✅ Poems saved to: {poems_file}")
    
    # Step 7: Generate audio (optional)
    if args.audio:
        print("\n🎵 Generating audio output...")
        try:
            audio_gen = AudioGenerator()
            
            # Generate audio for each poem
            audio_a = audio_gen.generate_poem_audio(
                results["google_poem"]["verses"],
                "poem_google",
                results["google_poem"]["agent"]
            )
            print(f"✅ Google poem audio: {audio_a}")
            
            audio_b = audio_gen.generate_poem_audio(
                results["groq_poem"]["verses"],
                "poem_groq",
                results["groq_poem"]["agent"]
            )
            print(f"✅ Groq poem audio: {audio_b}")
            
            # Generate judgment audio
            judgment_audio = audio_gen.generate_judgment_audio(
                results["judgment"].get("full_judgment", "Judgment not available")
            )
            print(f"✅ Judgment audio: {judgment_audio}")
            
            print("\n🎧 All audio files generated successfully!")
            
        except Exception as e:
            print(f"⚠️  Warning: Could not generate audio: {str(e)}")
    
    print("\n" + "="*60)
    print("✨ Process completed successfully!")
    if is_vision_based:
        print("📸 Image was analyzed using AI Vision (text + visual)")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()