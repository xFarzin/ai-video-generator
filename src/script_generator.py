import requests
import json
import os

def generate_script(topic="amazing space facts"):
    """Generate video script using Groq API (free)"""
    
    api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key:
        # Fallback to template if no API key
        return get_template_script(topic)
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    prompt = f"""Create a 60-second video script about {topic}.
Return JSON format with 5 slides:
{{
  "slides": [
    {{
      "image_prompt": "detailed image description for AI generation",
      "narration": "what the narrator says (15-20 seconds)"
    }}
  ]
}}

Make it engaging, educational, and viral-worthy."""

    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 1000
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        content = result["choices"][0]["message"]["content"]
        
        # Parse JSON from response
        script = json.loads(content)
        return script
        
    except Exception as e:
        print(f"Error generating script: {e}")
        return get_template_script(topic)


def get_template_script(topic):
    """Fallback template script"""
    return {
        "slides": [
            {
                "image_prompt": f"Breathtaking view of {topic}, cinematic lighting, 8k, ultra realistic",
                "narration": f"Welcome to today's video about {topic}. Let's explore some amazing facts!"
            },
            {
                "image_prompt": f"Close-up detail of {topic}, dramatic lighting, photorealistic",
                "narration": "Did you know that this is one of the most fascinating phenomena in the universe?"
            },
            {
                "image_prompt": f"Wide shot of {topic} in action, epic scale, movie style",
                "narration": "Scientists have been studying this for decades, and we're still discovering new things."
            },
            {
                "image_prompt": f"Artistic representation of {topic}, vibrant colors, detailed",
                "narration": "What makes this so special is how it connects to everything around us."
            },
            {
                "image_prompt": f"Peaceful scene of {topic}, mysterious atmosphere, cinematic",
                "narration": "Thanks for watching! What topic should we cover next? Let us know in the comments."
            }
        ]
    }
