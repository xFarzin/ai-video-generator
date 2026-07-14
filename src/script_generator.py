import requests
import json
import os
import re

def generate_script(topic="amazing space facts"):
    """Generate video script using Groq API"""


    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        print("No GROQ_API_KEY found, using template script")
        return get_template_script(topic)

    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    prompt = f"""


    Create a 60-second video script about {topic}.

    Return ONLY valid JSON.

    Do not use markdown.
    Do not use json.
    Do not include explanations.
    Do not include any text before or after the JSON.

    Format:

    {{
    "slides": [
    {{
    "image_prompt": "detailed image description for AI image generation",
    "narration": "short narration for this slide"
    }}
    ]
    }}

    Create exactly 5 slides.
    Make the content engaging, educational, and viral-worthy.
    """

    
    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {
                "role": "system",
                "content": "You are a JSON generator. Always return valid JSON only."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.7,
        "max_tokens": 1000
    }

    try:
        response = requests.post(
            url,
            headers=headers,
            json=data,
            timeout=60
        )

        print(f"Groq status code: {response.status_code}")

        if response.status_code != 200:
            print("Groq error response:")
            print(response.text)
            return get_template_script(topic)

        result = response.json()

        content = result["choices"][0]["message"]["content"]

        print("Raw Groq response:")
        print(content)

        content = content.strip()

        if content.startswith(""):
            content = re.sub(r"^json\s*", "", content)
            content = re.sub(r"^\s*", "", content)
            content = re.sub(r"\s*$", "", content)

        first_brace = content.find("{")
        last_brace = content.rfind("}")

        if first_brace != -1 and last_brace != -1:
            content = content[first_brace:last_brace + 1]

        script = json.loads(content)

        if "slides" not in script:
            raise ValueError("Missing 'slides' field")

        print(f"Successfully generated {len(script['slides'])} slides")

        return script

    except Exception as e:
        print(f"Error generating script: {e}")
        print("Using fallback template")
        return get_template_script(topic)


def get_template_script(topic):
    """Fallback template script"""


    return {
        "slides": [
            {
                "image_prompt": f"Breathtaking view of {topic}, cinematic lighting, 8k, ultra realistic",
                "narration": f"Welcome to today's video about {topic}. Let's explore some amazing facts."
            },
            {
                "image_prompt": f"Close-up detail of {topic}, dramatic lighting, photorealistic",
                "narration": "Did you know this is one of the most fascinating discoveries related to our topic?"
            },
            {
                "image_prompt": f"Wide shot of {topic} in action, epic scale, movie style",
                "narration": "Scientists continue to study it and uncover surprising new information."
            },
            {
                "image_prompt": f"Artistic representation of {topic}, vibrant colors, highly detailed",
                "narration": "Its impact reaches far beyond what most people realize."
            },
            {
                "image_prompt": f"Peaceful scene of {topic}, mysterious atmosphere, cinematic ending",
                "narration": "Thanks for watching. Follow for more amazing facts and discoveries."
            }
        ]
    }

