# main.py
import asyncio
import discord
import os
from discord.ext import commands
from dotenv import load_dotenv

# Takes bot token, command prefix, modules, and file type from .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = os.getenv('COMMAND_PREFIX')
MODULES = os.getenv('MODULES')
FILE_TYPE = os.getenv('FILE_TYPE')

# Establishes intents (events that the bot watches for and responds to)
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix = PREFIX, intents=intents)

# Lets us know that the bot is online
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

# Loads all commands (cogs)
async def load_cogs():
    for subdir, dirs, files in os.walk(MODULES):
        for file in files:
            if file.endswith(FILE_TYPE) and not file.startswith('__'):
                cog_path = f"{subdir.replace(os.sep, '.')}.{file[:-len(FILE_TYPE)]}"
                try:
                    await bot.load_extension(cog_path)
                    print(f"Loaded cog: {cog_path}")
                except Exception as e:
                    print(f"Failed to load cog {cog_path}: {type(e).__name__} - {e}")

#Putting it all into main()
async def main():
    await load_cogs()
    await bot.start(TOKEN)

#Executing all of the above via main()
asyncio.run(main())
