# LLMgine Integration for Chico Bot

This directory contains the LLMgine integration for the Chico Discord bot, enabling natural language processing and automatic tool calling.

## What is LLMgine?

LLMgine is a pattern-driven framework for building production-grade, tool-augmented LLM applications. It provides:

- **Engines**: Conversation logic with session isolation
- **Tool Management**: Automatic function calling and execution
- **Message Bus**: Async command and event handling
- **Context Management**: Chat history and conversation state
- **Observability**: Logging and monitoring capabilities

## Files Overview

### Core Engine
- `discord_engine.py` - Main Discord engine that integrates LLMgine with Discord
- `humanitix_tools.py` - Wrapper functions for existing Humanitix tools

### Bot Programs
- `llmgine_discord_bot.py` - Enhanced Discord bot with LLMgine integration
- `test_llmgine_cli.py` - CLI test program for testing the integration

## Setup

### 1. Install Dependencies

The LLMgine dependencies have been added to `pyproject.toml`. Install them with:

```bash
uv sync
```

### 2. Environment Variables

Make sure you have the following environment variables set in your `.env` file:

```env
BOT_TOKEN=your_discord_bot_token
OPENAI_API_KEY=your_openai_api_key
```

### 3. Test the Integration

Before running the Discord bot, test the LLMgine integration:

```bash
python src/chico/programs/test_llmgine_cli.py
```

This will start an interactive CLI where you can test natural language queries like:
- "What events are coming up?"
- "Tell me about the coding workshop"
- "How many tickets are left for the networking event?"

### 4. Run the Enhanced Discord Bot

```bash
python src/chico/programs/llmgine_discord_bot.py
```

## How It Works

### Natural Language Processing

Instead of using specific commands, users can now interact with the bot using natural language:

**Before (old bot):**
```
@bot list events
@bot event details intro to leetcode
@bot ticket status for networking event
```

**After (LLMgine bot):**
```
@bot What events are happening this month?
@bot Tell me about the leetcode workshop
@bot How many tickets are left for the networking event?
@bot Show me all upcoming events
```

### Tool Integration

The LLMgine engine automatically:
1. **Processes** natural language queries
2. **Determines** which tools to call
3. **Executes** the appropriate functions
4. **Returns** formatted responses

Available tools:
- `list_events()` - Lists all available events
- `get_event_details(event_name)` - Gets detailed information about a specific event
- `get_ticket_status(event_name)` - Checks ticket availability
- `search_events(query)` - Searches for events matching a query
- `get_upcoming_events()` - Shows upcoming events

### Session Management

Each Discord user gets their own LLMgine engine instance with:
- **Conversation history** - Remembers previous interactions
- **Context awareness** - Can reference previous messages
- **Session isolation** - Users don't interfere with each other

## Commands

The enhanced bot supports these commands:

- `!help` - Show help information
- `!clear` - Clear conversation history for the user

## Architecture

```
User Message → Discord Bot → LLMgine Engine → Tool Manager → Humanitix Tools
                    ↓              ↓              ↓              ↓
              Natural Language → OpenAI API → Function Call → Event Data
```

## Benefits

1. **Natural Interaction**: Users can ask questions in plain English
2. **Automatic Tool Selection**: LLM decides which tools to use
3. **Context Awareness**: Bot remembers conversation history
4. **Extensible**: Easy to add new tools and capabilities
5. **Robust**: Built-in error handling and session management

## Troubleshooting

### Common Issues

1. **"OPENAI_API_KEY not set"**
   - Make sure you have set your OpenAI API key in the `.env` file

2. **"Tool not found"**
   - Check that all tools are properly registered in the engine

3. **"Engine not responding"**
   - Verify that the LLMgine bootstrap is properly initialized

### Debug Mode

To enable debug logging, modify the `ApplicationConfig` in the bot:

```python
config = ApplicationConfig(
    enable_console_handler=True,  # Enable console logging
    enable_file_handler=True,     # Enable file logging
    log_level="debug"             # Set log level
)
```

## Extending the Integration

### Adding New Tools

1. Create a new function in `humanitix_tools.py`:

```python
def new_tool_function(param: str) -> str:
    """Description of what this tool does.
    
    Args:
        param: Description of the parameter
        
    Returns:
        Description of the return value
    """
    # Your tool logic here
    return "result"
```

2. Register it in the engine:

```python
await engine.register_tool(new_tool_function)
```

3. Update the system prompt to mention the new tool.

### Custom Engines

You can create custom engines by extending the `DiscordEngine` class or creating new engines following the LLMgine pattern.

## Resources

- [LLMgine Documentation](https://nathan-luo.github.io/llmgine/)
- [LLMgine GitHub Repository](https://github.com/nathan-luo/llmgine)
- [OpenAI Function Calling](https://platform.openai.com/docs/guides/function-calling) 