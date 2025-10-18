from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from typing import List, Dict
from config import GOOGLE_API_KEY, GROQ_API_KEY, GOOGLE_MODEL, GROQ_MODEL, JUDGE_MODEL


class PoemAgent:
    """Base class for poem generation agents."""
    
    def __init__(self, agent_name: str, llm, retriever):
        self.agent_name = agent_name
        self.llm = llm
        self.retriever = retriever
        self.output_parser = StrOutputParser()
    
    def generate_verse(self, context: str, previous_verses: List[str] = None) -> str:
        """
        Generate a verse based on context and previous verses.
        
        Args:
            context: Factual context from the document
            previous_verses: List of previously generated verses
            
        Returns:
            Generated verse
        """
        # Retrieve relevant facts
        relevant_docs = self.retriever.invoke(context)
        facts = "\n".join([doc.page_content for doc in relevant_docs[:2]])
        
        # Build conversation history
        conversation = ""
        if previous_verses:
            conversation = "\n".join([f"Line {i+1}: {verse}" 
                                     for i, verse in enumerate(previous_verses)])
        
        # Create prompt
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a talented poet. Create ONE poetic line that:
1. Is factually grounded in the provided context
2. Flows naturally with previous lines (if any)
3. Uses vivid imagery and literary devices
4. Maintains consistent rhythm and theme
5. Is creative yet truthful to the facts

Context Facts:
{facts}

Previous Lines:
{conversation}

Create the next line of the poem. Output ONLY the verse, nothing else."""),
            ("human", "Create the next poetic line based on: {context}")
        ])
        
        # Generate verse
        chain = prompt | self.llm | self.output_parser
        verse = chain.invoke({
            "facts": facts,
            "conversation": conversation if conversation else "This is the first line.",
            "context": context
        })
        
        return verse.strip()


class GooglePoemAgent(PoemAgent):
    """Poem agent using Google's Gemini model."""
    
    def __init__(self, retriever):
        llm = ChatGoogleGenerativeAI(
            model=GOOGLE_MODEL,
            google_api_key=GOOGLE_API_KEY,
            temperature=0.8,
            max_output_tokens=2048  # Add this instead of max_retries
        )
        super().__init__("Google Poet", llm, retriever)


class GroqPoemAgent(PoemAgent):
    """Poem agent using Groq's Llama model."""
    
    def __init__(self, retriever):
        llm = ChatGroq(
            groq_api_key=GROQ_API_KEY,
            model_name=GROQ_MODEL,
            temperature=0.8
        )
        super().__init__("Groq Poet", llm, retriever)


class JudgeAgent:
    """Agent to judge and compare poem verses."""
    
    def __init__(self, retriever):
        self.llm = ChatGoogleGenerativeAI(
            model=JUDGE_MODEL,
            google_api_key=GOOGLE_API_KEY,
            temperature=0.3,
            max_output_tokens=4096  # Add this instead of max_retries
        )
        self.retriever = retriever
        self.output_parser = StrOutputParser()
    
    def judge_verses(self, verses_a: List[str], verses_b: List[str], 
                     context: str) -> Dict[str, any]:
        """
        Judge two sets of verses based on multiple criteria.
        
        Judging Framework:
        1. Factual Accuracy (30%): How well grounded in source material
        2. Literary Quality (25%): Use of metaphors, imagery, literary devices
        3. Coherence (20%): Flow and connection between verses
        4. Creativity (15%): Originality and unique expression
        5. Rhythm & Sound (10%): Musicality and phonetic appeal
        
        Args:
            verses_a: Verses from first agent
            verses_b: Verses from second agent
            context: Original context/theme
            
        Returns:
            Dictionary with detailed judgment
        """
        # Retrieve relevant facts for verification
        relevant_docs = self.retriever.invoke(context)
        facts = "\n".join([doc.page_content for doc in relevant_docs[:3]])
        
        # Format verses
        poem_a = "\n".join([f"{i+1}. {v}" for i, v in enumerate(verses_a)])
        poem_b = "\n".join([f"{i+1}. {v}" for i, v in enumerate(verses_b)])
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert poetry critic and judge. Evaluate two poems based on:

JUDGING CRITERIA (Total: 100 points):

1. FACTUAL ACCURACY (30 points):
   - Are verses grounded in the provided facts?
   - Any factual errors or unsupported claims?
   - Score: 0-30

2. LITERARY QUALITY (25 points):
   - Use of metaphors, similes, and imagery
   - Literary devices (alliteration, personification, etc.)
   - Emotional resonance
   - Score: 0-25

3. COHERENCE (20 points):
   - Do verses flow naturally?
   - Consistent theme throughout?
   - Logical progression
   - Score: 0-20

4. CREATIVITY (15 points):
   - Originality of expression
   - Unique perspective
   - Avoidance of clichés
   - Score: 0-15

5. RHYTHM & SOUND (10 points):
   - Musicality and meter
   - Phonetic appeal
   - Internal rhyme/assonance
   - Score: 0-10

Provide your judgment in this EXACT format:

POEM A SCORES:
Factual Accuracy: X/30
Literary Quality: X/25
Coherence: X/20
Creativity: X/15
Rhythm & Sound: X/10
TOTAL: X/100

POEM B SCORES:
Factual Accuracy: X/30
Literary Quality: X/25
Coherence: X/20
Creativity: X/15
Rhythm & Sound: X/10
TOTAL: X/100

WINNER: [Poem A or Poem B]

JUSTIFICATION:
[2-3 sentences explaining the decision]

STRENGTHS OF WINNER:
- [Point 1]
- [Point 2]

AREAS FOR IMPROVEMENT:
- [Point 1]
- [Point 2]

Source Facts for Verification:
{facts}"""),
            ("human", """Poem A (Google Poet):
{poem_a}

Poem B (Groq Poet):
{poem_b}

Context: {context}

Judge these poems.""")
        ])
        
        chain = prompt | self.llm | self.output_parser
        judgment = chain.invoke({
            "facts": facts,
            "poem_a": poem_a,
            "poem_b": poem_b,
            "context": context
        })
        
        # Parse judgment
        result = self._parse_judgment(judgment)
        result["full_judgment"] = judgment
        
        return result
    
    def _parse_judgment(self, judgment: str) -> Dict[str, any]:
        """Parse the judgment text into structured data."""
        lines = judgment.strip().split('\n')
        result = {
            "poem_a_scores": {},
            "poem_b_scores": {},
            "winner": None,
            "justification": "",
            "total_a": 0,
            "total_b": 0
        }
        
        try:
            # Extract scores (simplified parsing)
            for line in lines:
                if "WINNER:" in line:
                    result["winner"] = line.split("WINNER:")[1].strip()
                elif "TOTAL:" in line and "poem_a_scores" not in str(result["total_a"]):
                    if result["total_a"] == 0:
                        result["total_a"] = int(line.split(":")[1].split("/")[0].strip())
                    else:
                        result["total_b"] = int(line.split(":")[1].split("/")[0].strip())
        except:
            pass  # Return partial results if parsing fails
        
        return result