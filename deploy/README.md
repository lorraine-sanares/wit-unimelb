# 🚀 Free Docker Deployment Guide for WIT Discord Bot

This guide shows you how to deploy your Discord bot for free using Docker on various platforms.

## 🎯 Best Free Options (Ranked)

### 1. **Railway** (Recommended - Easiest)
- **Free Tier**: 500 hours/month 
- **Auto-deploy**: Connects to GitHub
- **Pros**: Simplest setup, automatic deployments
- **Docker**: ✅ Native support

### 2. **Fly.io** (Most Generous)
- **Free Tier**: 3 VMs with 256MB RAM forever
- **Pros**: Most generous free tier, excellent performance
- **Docker**: ✅ Native support

### 3. **Render**
- **Free Tier**: Limited but functional
- **Pros**: Easy setup, good for small projects
- **Docker**: ✅ Native support

### 4. **Google Cloud Run**
- **Free Tier**: 2M requests/month
- **Pros**: Scales to zero, enterprise-grade
- **Docker**: ✅ Native support

---

## 🚢 Option 1: Railway (Easiest)

### Step-by-Step:

1. **Push to GitHub** (if not already)
   ```bash
   git add .
   git commit -m "Add Docker deployment"
   git push
   ```

2. **Go to [Railway.app](https://railway.app/)**
   - Sign up with GitHub
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository

3. **Add Environment Variables**
   - Go to Variables tab in Railway
   - Add:
     ```
     BOT_TOKEN=your_discord_bot_token
     OPENAI_API_KEY=your_openai_api_key
     DATABASE_URL=sqlite+aiosqlite:///:memory:
     ```

4. **Deploy**
   - Railway automatically detects Dockerfile
   - Deploys and runs continuously
   - ✅ Done!

---

## 🪂 Option 2: Fly.io (Most Free Resources)

### Setup:

1. **Install Fly CLI**
   ```bash
   curl -L https://fly.io/install.sh | sh
   ```

2. **Login**
   ```bash
   fly auth login
   ```

3. **Create and deploy**
   ```bash
   # Create app
   fly apps create wit-discord-bot-unique-name
   
   # Set secrets
   fly secrets set BOT_TOKEN=your_discord_bot_token
   fly secrets set OPENAI_API_KEY=your_openai_api_key
   fly secrets set DATABASE_URL=sqlite+aiosqlite:///:memory:
   
   # Deploy
   fly deploy
   ```

### Fly Configuration:
Create `fly.toml`:
```toml
app = "wit-discord-bot-unique-name"
primary_region = "syd"

[build]

[env]
  DATABASE_URL = "sqlite+aiosqlite:///:memory:"

[[vm]]
  cpu_kind = "shared"
  cpus = 1
  memory_mb = 256

[processes]
  bot = "uv run python src/chico/programs/llmgine_discord_bot.py"

[[services]]
  processes = ["bot"]
  protocol = ""
  internal_port = 8080
```

---

## 🎨 Option 3: Render

### Setup:

1. **Go to [Render.com](https://render.com/)**
2. **Create Web Service**
   - Connect GitHub repository
   - Select Docker environment
3. **Configure**:
   - Name: `wit-discord-bot`
   - Build Command: (leave empty)
   - Start Command: (leave empty - uses Dockerfile)
4. **Environment Variables**:
   ```
   BOT_TOKEN=your_discord_bot_token
   OPENAI_API_KEY=your_openai_api_key
   DATABASE_URL=sqlite+aiosqlite:///:memory:
   ```
5. **Deploy** ✅

---

## ☁️ Option 4: Google Cloud Run

### Setup:

1. **Install Google Cloud CLI**
2. **Enable APIs**:
   ```bash
   gcloud services enable run.googleapis.com
   gcloud services enable containerregistry.googleapis.com
   ```

3. **Deploy**:
   ```bash
   gcloud run deploy wit-discord-bot \
     --source . \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --set-env-vars BOT_TOKEN=your_token,OPENAI_API_KEY=your_key,DATABASE_URL=sqlite+aiosqlite:///:memory:
   ```

---

## 🧪 Local Testing with Docker

Before deploying, test locally:

```bash
# Create .env file with your tokens
cp env.example .env
# Edit .env with real values

# Build and run
docker-compose up --build

# Or manually:
docker build -t wit-discord-bot .
docker run --env-file .env wit-discord-bot
```

---

## 🔧 Getting Your Tokens

### Discord Bot Token:
1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create New Application
3. Go to "Bot" section
4. Click "Reset Token" and copy it
5. **Invite bot to server**: Bot → OAuth2 → URL Generator → Select "bot" scope and permissions

### OpenAI API Key:
1. Go to [OpenAI Platform](https://platform.openai.com/api-keys)
2. Create new secret key
3. Copy and save it

---

## 📊 Comparison Table

| Platform | Free Tier | Setup Difficulty | Reliability | Auto-Deploy |
|----------|-----------|-----------------|-------------|-------------|
| **Railway** | 500h/month | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ✅ |
| **Fly.io** | 3 VMs forever | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ✅ |
| **Render** | Limited | ⭐⭐⭐⭐ | ⭐⭐⭐ | ✅ |
| **Google Cloud** | 2M requests | ⭐⭐ | ⭐⭐⭐⭐⭐ | ❌ |

---

## 🎯 Recommended Approach:

1. **Start with Railway** - easiest setup
2. **Switch to Fly.io** if you need more resources
3. **Use Google Cloud Run** for production/scaling

Your bot will run 24/7 and automatically restart if it crashes! 🎉 