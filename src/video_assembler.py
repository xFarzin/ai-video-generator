from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips
import os
from pathlib import Path

def create_video(image_paths, audio_paths, output_path="output/final_video.mp4"):
    """Combine images and audio into a slideshow video"""
    
    Path("output").mkdir(parents=True, exist_ok=True)
    
    clips = []
    
    for i, (img_path, audio_path) in enumerate(zip(image_paths, audio_paths)):
        if not img_path or not audio_path:
            print(f"Skipping slide {i+1} (missing image or audio)")
            continue
        
        print(f"Assembling slide {i+1}...")
        
        # Load audio to get duration
        audio_clip = AudioFileClip(audio_path)
        duration = audio_clip.duration
        
        # Create image clip with audio duration
        image_clip = ImageClip(img_path, duration=duration)
        image_clip = image_clip.set_audio(audio_clip)
        
        # Resize to 1920x1080 if needed
        image_clip = image_clip.resize(height=1080)
        
        clips.append(image_clip)
    
    if not clips:
        raise Exception("No valid clips to concatenate")
    
    # Concatenate all clips
    print("Concatenating clips...")
    final_clip = concatenate_videoclips(clips, method="compose")
    
    # Write final video
    print("Rendering final video...")
    final_clip.write_videofile(
        output_path,
        fps=24,
        codec="libx264",
        audio_codec="aac",
        temp_audiofile="temp-audio.m4a",
        remove_temp=True
    )
    
    # Cleanup
    final_clip.close()
    for clip in clips:
        clip.close()
    
    print(f"✓ Video saved: {output_path}")
    return output_path
