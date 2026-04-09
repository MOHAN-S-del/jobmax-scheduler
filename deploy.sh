#!/bin/bash

# FreelanceMax Deployment Script
echo "🚀 FreelanceMax Deployment Script"
echo "================================="

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI not found. Install it first:"
    echo "npm install -g @railway/cli"
    echo "railway login"
    exit 1
fi

# Check if git repo is clean
if [ -n "$(git status --porcelain)" ]; then
    echo "⚠️  You have uncommitted changes. Commit them first:"
    git status
    echo ""
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Deploy to Railway
echo "📤 Deploying to Railway..."
railway up

# Get the deployment URL
echo "🔗 Deployment URL:"
railway domain

echo ""
echo "✅ Deployment complete!"
echo ""
echo "Next steps:"
echo "1. Set environment variables in Railway dashboard:"
echo "   - SECRET_KEY: $(openssl rand -hex 32)"
echo "   - GOOGLE_APPLICATION_CREDENTIALS_JSON: Your Firebase service account JSON"
echo "2. Test the application at the deployment URL"
echo "3. Set up custom domain (optional)"