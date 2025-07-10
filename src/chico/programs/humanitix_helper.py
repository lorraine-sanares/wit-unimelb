# bot.py
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import re
from chico.tools.humanitix import Humanitix

# Load environment variables
load_dotenv()
token = os.getenv("BOT_TOKEN")

# Initialize Humanitix client
humanitix = Humanitix()

# Create bot
bot = commands.Bot(command_prefix='!', intents=discord.Intents.default())

@bot.event # run when bot is ready
# async wait for discord response
async def on_ready():
    print(f'✅ Bot is online: {bot.user}')

@bot.event # run when a message is sent to the bot
async def on_message(message):
    # Don't respond to ourselves
    if message.author == bot.user:
        return
    
    # Respond to mentions with 'list events' or 'show events'
    if bot.user in message.mentions:
        content = message.content.lower()
        
        # queries for listing events
        if "list events" in content or "show events" in content:
            await list_events(message)

        # queries for event summary
        elif "event details" in content:
            # Extract event name from the message, e.g. 'event details intro to leetcode'
            match = re.search(r"event details (.+)", content)
            if match:
                user_input = match.group(1).strip()
                await show_event_details_by_name(message, user_input)
            else:
                await message.reply("Please specify the event name, e.g. event details intro to leetcode")
        
        # queries for ticket status - be more specific to avoid conflicts
        elif any(phrase in content for phrase in ["ticket status", "tickets remaining", "how many tickets", "attendees for", "capacity for"]):
            await show_ticket_status(message)
        
        else:
            await message.reply("👋 You mentioned me!")
    
    # Process commands (needed even if we don't have any)
    await bot.process_commands(message)

# ------------------------------------------------------------------------ */
async def list_events(message):
    """List all events using the Humanitix client."""
    msg = humanitix.list_events()
    await message.reply(msg)
        
# ------------------------------------------------------------------------ */
async def show_event_details_by_name(message, user_input):
    """Show event details by name using the Humanitix client."""
    msg = humanitix.show_event_details_by_name(user_input)
    await message.reply(msg)

# ------------------------------------------------------------------------ */
async def show_ticket_status(message):
    """Handle queries for ticket status or attendee count for an event by name."""
    try:
        content = message.content.lower()
        # Try to extract event name from the message
        match = re.search(r"(?:attendees|tickets remaining|ticket status) for (.+?)(\?|$)", content)
        if not match:
            await message.reply("Please specify the event name, e.g. 'How many tickets remaining for [event name]?' or 'What is the ticket status for [event name]?'")
            return
        user_input = match.group(1).strip()
        
        msg = humanitix.get_ticket_status(user_input)
        await message.reply(msg)
    except Exception as e:
        await message.reply(f"Error fetching ticket status: {e}")

# --- Start the bot (if not running as __main__) ---
bot.run(token)

