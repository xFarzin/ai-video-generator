import os
import sys
from datetime import datetime
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from config import Config
from script_generator import generate_script
from image_generator import generate_images
from tts_generator import generate_audio
from video_assembler import create_video
from youtube_uploader import upload_video

def main():
    print("=" * 60)
    print("🎬 AI Video Generator")
    print("=" * 60)
    
    # Validate configuration
    if not Config.validate():
        sys.exit(1)
    
    # Create output directories
    Config.IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    Config.AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    
    # Step 1: Generate script
    print("\n📝 Step 1: Generating script...")
    topic = Config.DEFAULT_TOPIC
    script = generate_script(topic)
    print(f"✓ Generated {len(script['slides'])} slides")
    
    # Step 2: Generate images
    print("\n🖼️ Step 2: Generating images...")
    image_paths = generate_images(script, str(Config.IMAGES_DIR))
    print(f"✓ Generated {len([p for p in image_paths if p])} images")
    
    # Step 3: Generate audio
    print("\n🎙️ Step 3: Generating audio...")
    audio_paths = generate_audio(script, str(Config.AUDIO_DIR), Config.TTS_VOICE)
    print(f"✓ Generated {len([p for p in audio_paths if p])} audio files")
    
    # Step 4: Assemble video
    print("\n🎬 Step 4: Assembling video...")
    video_path = str(Config.OUTPUT_DIR / "final_video.mp4")
    create_video(image_paths, audio_paths, video_path)
    print(f"✓ Video created: {video_path}")
    
    # Step 5: Upload to YouTube
    print("\n📤 Step 5: Uploading to YouTube...")
    try:
        today = datetime.now().strftime("%Y-%m-%d")
        title = f"Amazing Space Facts - {today}"
        description = f"Daily AI-generated video about {topic}\n\nGenerated with AI automation."
        
        video_id = upload_video(video_path, title, description)
        print(f"\n✅ SUCCESS! Video uploaded: https://youtube.com/watch?v={video_id}")
        
    except Exception as e:
        print(f"\n⚠️ Upload failed: {e}")
        print(f"Video saved locally at: {video_path}")
    
    print("\n" + "=" * 60)
    print("🎉 Done!")
    print("=" * 60)

if __name__ == "__main__":
    main()
