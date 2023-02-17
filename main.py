# main.py
import asyncio
import discord
import os
from discord.ext import commands
from dotenv import load_dotenv

# Takes bot token and command prefix from .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = os.getenv('COMMAND_PREFIX')

# Establishes intents (events that the bot watches for and responds to) and connect bot to discord
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix = PREFIX, intents=intents)

# 
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

# Loads all cogs into main.py
async def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')

# 
async def main():
    await load()
    await bot.start(TOKEN)

asyncio.run(main())
