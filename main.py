import discord
import ollama
import prompts
from dotenv import load_dotenv
import os

load_dotenv()

# 1. Setup intents
intent = discord.Intents.default()
intent.message_content = True
client = discord.Client(intents=intent)

bot_token=os.getenv("bot_token")
ollama_model=os.getenv("ollama_model")

# 2. Register the event listener
@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
def get_ollama(user_message):
    reply=ollama.generate(model=ollama_model,prompt=prompts.SYSTEM_PROMPT+user_message)
    return reply['response']
@client.event
async def on_message(message):
    # Prevent the bot from replying to itself
    if message.author == client.user:
        return
    username = str(message.author)
    user_message = str(message.content)
    channel = str(message.channel)

    # Check if the bot was mentioned in the incoming message
    if client.user in message.mentions:
        await message.reply(get_ollama(user_message), mention_author=False)
    
    content_lower=message.content.lower()
    if "lila" in content_lower:
        await message.reply(get_ollama(user_message), mention_author=False)

# 3. Run the bot
client.run(bot_token)
