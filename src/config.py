import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file
load_dotenv()

class Config:
    """Configuration manager"""
    
    # API Keys
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    HF_TOKEN = os.getenv("HF_TOKEN")
    YOUTUBE_CLIENT_SECRET = os.getenv("YOUTUBE_CLIENT_SECRET")
    
    # Video Settings
    VIDEO_WIDTH = int(os.getenv("VIDEO_WIDTH", "1280"))
    VIDEO_HEIGHT = int(os.getenv("VIDEO_HEIGHT", "720"))
    VIDEO_FPS = int(os.getenv("VIDEO_FPS", "24"))
    
    # TTS Settings
    TTS_VOICE = os.getenv("TTS_VOICE", "en-US-ChristopherNeural")
    
    # YouTube Settings
    YOUTUBE_PRIVACY_STATUS = os.getenv("YOUTUBE_PRIVACY_STATUS", "public")
    YOUTUBE_CATEGORY_ID = os.getenv("YOUTUBE_CATEGORY_ID", "22")
    
    # Default Topic
    DEFAULT_TOPIC = os.getenv("DEFAULT_TOPIC", "amazing space facts")
    
    # Output directories
    OUTPUT_DIR = Path("output")
    IMAGES_DIR = OUTPUT_DIR / "images"
    AUDIO_DIR = OUTPUT_DIR / "audio"
    
    @classmethod
    def validate(cls):
        """Validate required environment variables"""
        errors = []
        
        if not cls.GROQ_API_KEY:
            errors.append("GROQ_API_KEY is not set")
        
        if not cls.YOUTUBE_CLIENT_SECRET:
            errors.append("YOUTUBE_CLIENT_SECRET is not set")
        
        if errors:
            print("❌ Configuration errors:")
            for error in errors:
                print(f"  - {error}")
            print("\nPlease check your .env file or GitHub Secrets")
            return False
        
        print("✅ Configuration validated")
        return True
