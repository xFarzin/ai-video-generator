# 🎬 AI Video Generator

Automated daily video generation with AI.

## Setup

1. **Get API Keys** (all free):
   - Groq: https://console.groq.com/keys
   - YouTube: https://console.cloud.google.com/

2. **Add Secrets to GitHub**:
   - Go to: Settings → Secrets → Actions
   - Add: `GROQ_API_KEY`
   - Add: `YOUTUBE_CLIENT_SECRET` (client_secret.json content)

3. **YouTube OAuth Setup**:
   - First run will need manual auth
   - Run locally: `python main.py`
   - Copy `token.pickle` to repo (or use service account)

4. **Enable GitHub Actions**:
   - Push code to GitHub
   - Actions will run daily at 9 AM UTC

## Manual Run

```bash
pip install -r requirements.txt
python main.py
