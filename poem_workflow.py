from typing import List, Dict, TypedDict
from langgraph.graph import StateGraph, END, START
from poem_agents import GooglePoemAgent, GroqPoemAgent, JudgeAgent


class PoemState(TypedDict):
    """State for the poem generation workflow."""
    context: str
    google_verses: List[str]
    groq_verses: List[str]
    current_verse_count: int
    total_verses: int
    judgment: Dict[str, any]
    phase: str  # 'generation' or 'judging'


class PoemWorkflow:
    """Workflow for collaborative poem generation and judging."""
    
    def __init__(self, retriever, num_verses: int = 6):
        self.retriever = retriever
        self.num_verses = num_verses
        
        # Initialize agents
        self.google_agent = GooglePoemAgent(retriever)
        self.groq_agent = GroqPoemAgent(retriever)
        self.judge_agent = JudgeAgent(retriever)
        
        # Build workflow
        self.workflow = self._build_workflow()
    
    def _build_workflow(self) -> StateGraph:
        """Build the LangGraph workflow."""
        workflow = StateGraph(PoemState)
        
        # Add nodes
        workflow.add_node("google_generates", self._google_generates)
        workflow.add_node("groq_generates", self._groq_generates)
        workflow.add_node("judge_poems", self._judge_poems)
        
        # Add edges
        workflow.add_edge(START, "google_generates")
        workflow.add_conditional_edges(
            "google_generates",
            self._check_verse_count,
            {
                "continue": "groq_generates",
                "judge": "judge_poems"
            }
        )
        workflow.add_conditional_edges(
            "groq_generates",
            self._check_verse_count,
            {
                "continue": "google_generates",
                "judge": "judge_poems"
            }
        )
        workflow.add_edge("judge_poems", END)
        
        return workflow.compile()
    
    def _google_generates(self, state: PoemState) -> PoemState:
        """Google agent generates a verse."""
        print(f"\n🌟 Google Poet generating verse {state['current_verse_count'] + 1}...")
        
        verse = self.google_agent.generate_verse(
            context=state["context"],
            previous_verses=state["google_verses"] + state["groq_verses"]
        )
        
        state["google_verses"].append(verse)
        state["current_verse_count"] += 1
        
        print(f"   Google: {verse}")
        return state
    
    def _groq_generates(self, state: PoemState) -> PoemState:
        """Groq agent generates a verse."""
        print(f"\n⚡ Groq Poet generating verse {state['current_verse_count'] + 1}...")
        
        verse = self.groq_agent.generate_verse(
            context=state["context"],
            previous_verses=state["google_verses"] + state["groq_verses"]
        )
        
        state["groq_verses"].append(verse)
        state["current_verse_count"] += 1
        
        print(f"   Groq: {verse}")
        return state
    
    def _judge_poems(self, state: PoemState) -> PoemState:
        """Judge agent evaluates both poems."""
        print("\n⚖️  Judge evaluating poems...")
        
        judgment = self.judge_agent.judge_verses(
            verses_a=state["google_verses"],
            verses_b=state["groq_verses"],
            context=state["context"]
        )
        
        state["judgment"] = judgment
        state["phase"] = "complete"
        
        return state
    
    def _check_verse_count(self, state: PoemState) -> str:
        """Check if we've generated enough verses."""
        if state["current_verse_count"] >= state["total_verses"]:
            return "judge"
        return "continue"
    
    def run(self, context: str) -> Dict[str, any]:
        """
        Run the complete poem generation and judging workflow.
        
        Args:
            context: Theme or context for the poem
            
        Returns:
            Complete results including poems and judgment
        """
        # Initialize state
        initial_state: PoemState = {
            "context": context,
            "google_verses": [],
            "groq_verses": [],
            "current_verse_count": 0,
            "total_verses": self.num_verses,
            "judgment": {},
            "phase": "generation"
        }
        
        # Run workflow
        print(f"\n{'='*60}")
        print(f"🎭 Starting Collaborative Poem Generation")
        print(f"📝 Context: {context}")
        print(f"📊 Target verses: {self.num_verses}")
        print(f"{'='*60}")
        
        final_state = self.workflow.invoke(initial_state)
        
        # Format results
        results = {
            "context": context,
            "google_poem": {
                "agent": "Google Poet (Gemini)",
                "verses": final_state["google_verses"]
            },
            "groq_poem": {
                "agent": "Groq Poet (Llama)",
                "verses": final_state["groq_verses"]
            },
            "judgment": final_state["judgment"]
        }
        
        return results
