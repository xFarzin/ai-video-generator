import asyncio
import edge_tts
import os
from pathlib import Path

async def generate_tts_for_slide(text, output_path, voice="en-US-ChristopherNeural"):
    """Generate TTS for a single slide"""
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_path)

def generate_audio(script, output_dir="output/audio", voice="en-US-ChristopherNeural"):
    """Generate audio for all slides"""
    
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    audio_paths = []
    
    for i, slide in enumerate(script["slides"]):
        narration = slide["narration"]
        audio_path = f"{output_dir}/slide_{i+1}.mp3"
        
        print(f"Generating audio {i+1}/{len(script['slides'])}...")
        
        try:
            # Run async function with specified voice
            asyncio.run(generate_tts_for_slide(narration, audio_path, voice))
            audio_paths.append(audio_path)
            print(f"✓ Saved: {audio_path}")
            
        except Exception as e:
            print(f"Error generating audio {i+1}: {e}")
            audio_paths.append(None)
    
    return audio_paths
