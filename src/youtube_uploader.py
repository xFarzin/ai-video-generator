import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import pickle

SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

def get_youtube_service():
    """Get YouTube API service"""
    creds = None
    
    # Check for token file
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    # If no valid credentials, get new ones
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # In GitHub Actions, use service account or pre-generated token
            client_secret = os.getenv('YOUTUBE_CLIENT_SECRET')
            if not client_secret:
                raise Exception("YouTube credentials not configured")
            
            # Save client secret to file
            with open('client_secret.json', 'w') as f:
                f.write(client_secret)
            
            flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save credentials
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    return build('youtube', 'v3', credentials=creds)

def upload_video(video_path, title, description, tags=None):
    """Upload video to YouTube"""
    print("Creating YouTube service...")
    youtube = get_youtube_service()


    channel = youtube.channels().list(
        part="snippet",
        mine=True
    ).execute()

    print("Connected channel:")
    print(channel["items"][0]["snippet"]["title"])
    print("Channel ID:", channel["items"][0]["id"])


    if tags is None:
        tags = ["ai", "automation", "facts"]
    
    body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': tags,
            'categoryId': '22'  # People & Blogs
        },
        'status': {
            'privacyStatus': 'public',
            'selfDeclaredMadeForKids': False
        }
    }
    
    media = MediaFileUpload(video_path, mimetype='video/mp4', resumable=True)
    print("Preparing upload request...")
    request = youtube.videos().insert(
        part=','.join(body.keys()),
        body=body,
        media_body=media
    )
    print("Starting upload...")
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Upload progress: {int(status.progress() * 100)}%")
    
    video_id = response['id']
    print(f"✓ Video uploaded: https://youtube.com/watch?v={video_id}")
    
    return video_id
