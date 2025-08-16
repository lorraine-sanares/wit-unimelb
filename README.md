# WIT Unimelb Discord Bot

A Discord bot for Women in Technology at University of Melbourne that helps users find information about events, check ticket availability, and provide details about upcoming activities.

## Features

- Natural language event queries
- Event search and details
- Ticket availability checking
- Upcoming events listing
- LLMgine-powered responses

## Setup

1. Get Discord Bot Token from [Discord Developer Portal](https://discord.com/developers/applications)
2. Get OpenAI API Key from [OpenAI Platform](https://platform.openai.com/api-keys)
3. Set environment variables in `.env` file
4. Run with Docker or locally

## Environment Variables

```
BOT_TOKEN=your_discord_bot_token
OPENAI_API_KEY=your_openai_api_key
DATABASE_URL=sqlite+aiosqlite:///:memory:
```

## Usage

Mention the bot in Discord and ask about events:
- "What events are coming up?"
- "Tell me about the coding workshop" 
- "Check ticket availability for networking event"
