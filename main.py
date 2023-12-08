import os
import discord
import logging
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Initialize Discord client
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
discord_client = discord.Client(intents=intents)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize OpenAI client
openai.api_key = OPENAI_API_KEY

# Function to send a query to OpenAI's API and get a response
async def ask_openai(prompt):
    try:
        response = openai.Completion.create(
            model="gpt-4-1106-preview",
            prompt=prompt,
            max_tokens=150  # Adjust the number of tokens as needed
        )
        return response.choices[0].text
    except Exception as e:
        logging.error(f"Error in ask_openai: {e}")
        return "I'm having trouble processing that request."

# Discord event handlers
@discord_client.event
async def on_ready():
    logging.info(f"{discord_client.user} has connected to Discord!")

@discord_client.event
async def on_message(message):
    if message.author == discord_client.user or not discord_client.user.mentioned_in(message):
        return
    
    prompt = message.clean_content.replace(f"@{discord_client.user.name}", "").strip()
    
    response = await ask_openai(prompt)
    
    await message.channel.send(response or "Sorry, I can't process that request right now.")

# Run the Discord bot
discord_client.run(DISCORD_BOT_TOKEN)
