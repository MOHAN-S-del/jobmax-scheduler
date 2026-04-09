# 🚀 FreelanceMax Deployment Guide

## Quick Deploy to Railway (Recommended)

### 1. Fork/Clone this repository to GitHub

### 2. Connect to Railway
1. Go to [Railway.app](https://railway.app)
2. Sign up/Login with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your forked repository

### 3. Set Environment Variables
In Railway dashboard, go to your project → Variables:

```
SECRET_KEY=your-super-secret-key-here
GOOGLE_APPLICATION_CREDENTIALS_JSON={"type":"service_account","project_id":"your-project-id",...}
PORT=8000
```

### 4. Deploy
Railway will automatically build and deploy your app!

## Alternative: Deploy to Render

### 1. Create a Render account
### 2. Connect your GitHub repo
### 3. Choose "Web Service"
### 4. Set build command: `pip install -r requirements.txt`
### 5. Set start command: `gunicorn --bind 0.0.0.0:$PORT app:app`
### 6. Add environment variables as above

## Environment Variables Required

- `SECRET_KEY`: Random string for Flask sessions (generate with `openssl rand -hex 32`)
- `GOOGLE_APPLICATION_CREDENTIALS_JSON`: Your Firebase service account JSON (as a string)
- `PORT`: Port for the server (Railway/Render set this automatically)

## Firebase Setup

1. Go to [Firebase Console](https://console.firebase.google.com)
2. Create/select your project
3. Go to Project Settings → Service Accounts
4. Generate new private key → Download JSON
5. Copy the entire JSON content as the `GOOGLE_APPLICATION_CREDENTIALS_JSON` value

## Post-Deployment

1. Update your dashboard URLs if needed
2. Test the scheduling functionality
3. Enable Firebase authentication in production

## Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export SECRET_KEY="your-secret-key"
export PORT=8000

# Run locally
python app.py
```

## Troubleshooting

- **Port issues**: Railway/Render set PORT automatically
- **Firebase errors**: Check your service account JSON format
- **Build failures**: Ensure all dependencies are in requirements.txt