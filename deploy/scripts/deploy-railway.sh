#!/bin/bash

# Railway Deployment Script for WIT Discord Bot
# This script helps automate the deployment process

set -e

echo "🚀 Deploying WIT Discord Bot to Railway..."

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "❌ Not in a git repository. Please run 'git init' first."
    exit 1
fi

# Check if there are uncommitted changes
if ! git diff-index --quiet HEAD --; then
    echo "⚠️  You have uncommitted changes. Committing them now..."
    git add .
    git commit -m "Add Docker deployment configuration"
fi

# Push to GitHub
echo "📤 Pushing to GitHub..."
git push origin main

echo "✅ Code pushed to GitHub!"
echo ""
echo "🎯 Next steps:"
echo "1. Go to https://railway.app/"
echo "2. Sign up with GitHub"
echo "3. Create New Project → Deploy from GitHub repo"
echo "4. Select this repository"
echo "5. Add environment variables:"
echo "   - BOT_TOKEN=your_discord_bot_token"
echo "   - OPENAI_API_KEY=your_openai_api_key"
echo "   - DATABASE_URL=sqlite+aiosqlite:///:memory:"
echo "6. Deploy!"
echo ""
echo "🤖 Your bot will be running 24/7 on Railway!" 