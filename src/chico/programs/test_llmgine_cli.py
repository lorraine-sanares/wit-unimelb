"""
Test CLI for LLMgine integration.
This allows testing the LLMgine engine and tools without running the Discord bot.
"""

import asyncio
import os
from dotenv import load_dotenv

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


async def test_llmgine():
    """Test the LLMgine integration."""
    print("🤖 Initializing LLMgine test...")
    
    # Initialize LLMgine bootstrap
    config = ApplicationConfig(
        enable_console_handler=False,
        enable_file_handler=False
    )
    bootstrap = ApplicationBootstrap(config)
    await bootstrap.bootstrap()
    
    # Create engine
    engine = DiscordEngine(
        session_id=SessionID("test_session"),
        system_prompt=SYSTEM_PROMPT
    )
    
    # Register tools
    print("🔧 Registering tools...")
    await engine.register_tool(list_events)
    await engine.register_tool(get_event_details)
    await engine.register_tool(get_ticket_status)
    await engine.register_tool(search_events)
    await engine.register_tool(get_upcoming_events)
    
    print("✅ Tools registered successfully!")
    print("\n" + "="*50)
    print("🤖 LLMgine Test CLI")
    print("="*50)
    print("Type your questions about WIT Unimelb events!")
    print("Type 'quit' to exit.")
    print("="*50)
    
    while True:
        try:
            # Get user input
            user_input = input("\n👤 You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            
            if not user_input:
                continue
            
            print("🤖 Bot: Processing...")
            
            # Create command
            command = DiscordEngineCommand(
                prompt=user_input,
                user_id="test_user",
                channel_id="test_channel"
            )
            
            # Process with LLMgine
            result = await engine.handle_command(command)
            
            if result.success:
                print(f"🤖 Bot: {result.result}")
            else:
                print(f"❌ Error: {result.error}")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


if __name__ == "__main__":
    # Check if OpenAI API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY environment variable not set!")
        print("Please set your OpenAI API key in your .env file:")
        print("OPENAI_API_KEY=your_api_key_here")
        exit(1)
    
    asyncio.run(test_llmgine()) 