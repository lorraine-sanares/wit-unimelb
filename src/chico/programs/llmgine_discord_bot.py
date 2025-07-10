"""
Enhanced Discord bot with LLMgine integration.
This bot uses LLMgine to process natural language and automatically call appropriate tools.
"""

import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio
from typing import Dict, Optional

from chico.llmgine.discord_engine import DiscordEngine, DiscordEngineCommand
from chico.llmgine.humanitix_tools import (
    list_events,
    get_event_details,
    get_ticket_status,
    search_events,
    get_upcoming_events
)
from llmgine.llm import SessionID
from llmgine.bootstrap import ApplicationBootstrap, ApplicationConfig

# Load environment variables
load_dotenv()
token = os.getenv("BOT_TOKEN")
openai_api_key = os.getenv("OPENAI_API_KEY")

# Create bot
bot = commands.Bot(command_prefix='!', intents=discord.Intents.default())

# Store engine instances per user for session management
user_engines: Dict[str, DiscordEngine] = {}

# System prompt for the LLM
SYSTEM_PROMPT = """You are a helpful assistant for WIT Unimelb (Women in Technology at University of Melbourne). 
You help users find information about events, check ticket availability, and provide details about upcoming activities.

You have access to the following tools:
- list_events: Lists all available events
- get_event_details: Gets detailed information about a specific event
- get_ticket_status: Checks ticket availability for an event
- search_events: Searches for events matching a query
- get_upcoming_events: Shows upcoming events

When users ask about events, tickets, or activities, use the appropriate tools to provide accurate information.
Be friendly and helpful, and always provide relevant information about WIT Unimelb events.

If a user asks about something not related to events or WIT Unimelb, politely redirect them to ask about events or activities."""


async def get_or_create_engine(user_id: str) -> DiscordEngine:
    """Get or create an LLMgine engine for a user.
    
    Args:
        user_id: The Discord user ID
        
    Returns:
        DiscordEngine: The engine instance for the user
    """
    if user_id not in user_engines:
        # Create new engine for user
        engine = DiscordEngine(
            session_id=SessionID(f"discord_{user_id}"),
            system_prompt=SYSTEM_PROMPT
        )
        
        # Register all tools
        await engine.register_tool(list_events)
        await engine.register_tool(get_event_details)
        await engine.register_tool(get_ticket_status)
        await engine.register_tool(search_events)
        await engine.register_tool(get_upcoming_events)
        
        user_engines[user_id] = engine
        print(f"Created new engine for user {user_id}")
    
    return user_engines[user_id]


@bot.event
async def on_ready():
    print(f'✅ LLMgine Discord Bot is online: {bot.user}')
    print(f'🤖 Bot is ready to process natural language queries!')


@bot.event
async def on_message(message):
    # Don't respond to ourselves
    if message.author == bot.user:
        return
    
    # Check if bot is mentioned or message starts with command prefix
    is_mentioned = bot.user in message.mentions
    is_command = message.content.startswith('!')
    
    if is_mentioned or is_command:
        # Extract the actual message content (remove mention or command prefix)
        if is_mentioned:
            # Remove the bot mention from the message
            content = message.content.replace(f'<@{bot.user.id}>', '').strip()
        else:
            # Remove the command prefix
            content = message.content[1:].strip()
        
        # Skip if no content after removing mention/prefix
        if not content:
            await message.reply("👋 Hi! I can help you with WIT Unimelb events. Try asking me about events, tickets, or upcoming activities!")
            return
        
        # Show typing indicator
        async with message.channel.typing():
            try:
                # Get or create engine for this user
                engine = await get_or_create_engine(str(message.author.id))
                
                # Create command for LLMgine
                command = DiscordEngineCommand(
                    prompt=content,
                    user_id=str(message.author.id),
                    channel_id=str(message.channel.id)
                )
                
                # Process with LLMgine
                result = await engine.handle_command(command)
                
                if result.success:
                    # Send the response
                    response = result.result
                    # Split long responses if needed
                    if len(response) > 2000:
                        # Split into chunks
                        chunks = [response[i:i+1900] for i in range(0, len(response), 1900)]
                        for i, chunk in enumerate(chunks):
                            if i == 0:
                                await message.reply(chunk)
                            else:
                                await message.channel.send(chunk)
                    else:
                        await message.reply(response)
                else:
                    await message.reply(f"❌ Sorry, I encountered an error: {result.error}")
                    
            except Exception as e:
                print(f"Error processing message: {e}")
                await message.reply("❌ Sorry, I encountered an error processing your request. Please try again!")
    
    # Process commands (needed for Discord.py)
    await bot.process_commands(message)


@bot.command(name='clear')
async def clear_context(ctx):
    """Clear the conversation context for the user."""
    user_id = str(ctx.author.id)
    if user_id in user_engines:
        await user_engines[user_id].clear_context()
        await ctx.reply("🧹 Conversation context cleared!")
    else:
        await ctx.reply("No conversation context to clear.")


@bot.command(name='withelp')
async def help_command(ctx):
    """Show help information."""
    help_text = """🤖 **WIT Unimelb Bot Help**

I can help you with information about WIT Unimelb events! Here's what I can do:

**Natural Language Queries:**
- Mention me and ask questions like:
  - "What events are coming up?"
  - "Tell me about the coding workshop"
  - "How many tickets are left for the networking event?"
  - "Show me all events"

**Commands:**
- `!clear` - Clear our conversation history
- `!withelp` - Show this help message

**Examples:**
- @bot "What events are happening this month?"
- @bot "Tell me about the leetcode workshop"
- @bot "Check ticket availability for the networking event"

Just mention me and ask naturally! 🎉"""
    
    await ctx.reply(help_text)


async def main():
    """Initialize and run the bot."""
    # Initialize LLMgine bootstrap
    config = ApplicationConfig(
        enable_console_handler=False,
        enable_file_handler=False
    )
    bootstrap = ApplicationBootstrap(config)
    await bootstrap.bootstrap()
    
    # Start the bot
    await bot.start(token)


if __name__ == "__main__":
    asyncio.run(main()) 