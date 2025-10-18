import os
from gtts import gTTS
from pydub import AudioSegment
from typing import List
from config import AUDIO_OUTPUT_DIR, AUDIO_LANGUAGE


class AudioGenerator:
    """Generate audio output from poem verses."""
    
    def __init__(self):
        # Create output directory if it doesn't exist
        os.makedirs(AUDIO_OUTPUT_DIR, exist_ok=True)
    
    def generate_poem_audio(self, verses: List[str], output_filename: str, 
                           agent_name: str = "") -> str:
        """
        Generate audio file from poem verses.
        
        Args:
            verses: List of verse strings
            output_filename: Name for output file (without extension)
            agent_name: Optional agent name to include in audio
            
        Returns:
            Path to generated audio file
        """
        # Combine verses into full text
        intro = f"Poem by {agent_name}\n\n" if agent_name else ""
        full_text = intro + "\n\n".join(verses)
        
        # Generate audio
        tts = gTTS(text=full_text, lang=AUDIO_LANGUAGE, slow=False)
        
        # Save audio file
        output_path = os.path.join(AUDIO_OUTPUT_DIR, f"{output_filename}.mp3")
        tts.save(output_path)
        
        return output_path
    
    def generate_combined_audio(self, verses_a: List[str], verses_b: List[str],
                               agent_a_name: str, agent_b_name: str,
                               output_filename: str = "combined_poem") -> str:
        """
        Generate audio with alternating verses from both agents.
        
        Args:
            verses_a: Verses from agent A
            verses_b: Verses from agent B
            agent_a_name: Name of agent A
            agent_b_name: Name of agent B
            output_filename: Output filename
            
        Returns:
            Path to combined audio file
        """
        # Generate individual audio files
        audio_a_path = self.generate_poem_audio(verses_a, "temp_a", agent_a_name)
        audio_b_path = self.generate_poem_audio(verses_b, "temp_b", agent_b_name)
        
        # Load audio files
        audio_a = AudioSegment.from_mp3(audio_a_path)
        audio_b = AudioSegment.from_mp3(audio_b_path)
        
        # Add silence between poems
        silence = AudioSegment.silent(duration=2000)  # 2 seconds
        
        # Combine audio
        combined = audio_a + silence + audio_b
        
        # Export combined audio
        output_path = os.path.join(AUDIO_OUTPUT_DIR, f"{output_filename}.mp3")
        combined.export(output_path, format="mp3")
        
        # Clean up temporary files
        os.remove(audio_a_path)
        os.remove(audio_b_path)
        
        return output_path
    
    def generate_judgment_audio(self, judgment_text: str, 
                                output_filename: str = "judgment") -> str:
        """
        Generate audio for judgment results.
        
        Args:
            judgment_text: Text of the judgment
            output_filename: Output filename
            
        Returns:
            Path to generated audio file
        """
        tts = gTTS(text=judgment_text, lang=AUDIO_LANGUAGE, slow=False)
        output_path = os.path.join(AUDIO_OUTPUT_DIR, f"{output_filename}.mp3")
        tts.save(output_path)
        return output_path
