import requests
import os
from pathlib import Path

def generate_images(script, output_dir="output/images"):
    """Generate images using Pollinations.ai (no API key needed)"""
    
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    image_paths = []
    
    for i, slide in enumerate(script["slides"]):
        prompt = slide["image_prompt"]
        
        # Pollinations.ai URL
        encoded_prompt = requests.utils.quote(prompt)
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1280&height=720&nologo=true&seed={i}"
        
        print(f"Generating image {i+1}/{len(script['slides'])}...")
        
        try:
            response = requests.get(url, timeout=60)
            response.raise_for_status()
            
            # Save image
            image_path = f"{output_dir}/slide_{i+1}.png"
            with open(image_path, "wb") as f:
                f.write(response.content)
            
            image_paths.append(image_path)
            print(f"✓ Saved: {image_path}")
            
        except Exception as e:
            print(f"Error generating image {i+1}: {e}")
            # Create placeholder
            image_paths.append(None)
    
    return image_paths
