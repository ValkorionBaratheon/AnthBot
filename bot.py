# bot.py
import os
import random
import discord
import asyncio
from dotenv import load_dotenv
from discord.ext import commands

# Takes bot token and command prefix from .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = os.getenv('COMMAND_PREFIX')

# Establishes intents (events that the bot watches for and responds to) and connect bot to discord
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix = PREFIX, intents=intents)

# Dictionary storing all attack names, damages, and probabilities of success
attacks = {
    "k": {"name": "Katana", "damage": 20, "probability": 0.8},
    "b": {"name": "Crossbow", "damage": 60, "probability": 0.50},
    "r": {"name": "Capture Net", "damage": 80, "probability": 0.20}
}

# Waits for opponent to accept or deny challenge, returns true or false
async def acceptance(ctx, opponent):
    # Send initial message and wait for response
    await ctx.send(f"**{ctx.author.name} has dared to challenge {opponent.mention}!** Will accept? ``If the answer is positive, please write yes - Otherwise no``")

        # Wait for the opponent's response
    def check(msg):
        return msg.author == opponent
    
    try:
        response = await bot.wait_for('message', check=check, timeout=30.0)
    except asyncio.TimeoutError:
        await ctx.send(f"The coward {opponent.mention} failed to show.")
        return False
    
    # Process user's response
    if response.content.lower() == "yes":
        return True
    else:
        await ctx.send(f"It seems {opponent.name} was too scared to fight!")
        return False
   
# Simulates a battle between the user who invoked the !challenge command and the specified opponent.
async def duel(ctx, opponent):
    # Initialize health for each player
    challenger_health = 100
    opponent_health = 100
    round = 1

    # Start of duel message
    await ctx.send(f"**An epic battle between {ctx.author.mention} and {opponent.mention} has begun!** Good luck to both!")

    # Alternate between players selecting attacks until one player has 0 health
    while challenger_health > 0 and opponent_health > 0:
        # Prompt each player to select an attack
        await ctx.send(f"**[Round {round}]** Fighters'current HP: {ctx.author.mention} ({challenger_health}%) - {opponent.mention} ({opponent_health}%)")
        challenger_health = await turn(ctx, opponent, ctx.author, challenger_health)
        await ctx.send(f"**[Round {round}]** Fighters'current HP: {ctx.author.mention} ({challenger_health}%) - {opponent.mention} ({opponent_health}%)")
        opponent_health = await turn(ctx, ctx.author, opponent, opponent_health)
        round +=1

    # Determine winner
    if challenger_health > 0:
        result = f"**The battle ends!** {ctx.author.mention} wins!"
    else:
        result = f"**The battle ends!** {opponent.mention} wins!"

    # Send battle result to channel
    await ctx.send(result)

async def turn(ctx, player, other, other_health):
    player_attack = await prompt_attack(ctx, player)
    
    if random.random() < attacks[player_attack]["probability"]:
        player_damage = attacks[player_attack]["damage"]
        other_health -= player_damage
        await ctx.send(f"**{player.name}** attacks **{other.name}** with **{attacks[player_attack]['name']}**. It successfully removed **{player_damage} life!**")
    else:
        await ctx.send(f"**{player.name}** attacks **{other.name}** with **{attacks[player_attack]['name']}**. The attack **failed.**")

    return other_health

# Prompts the specified player to select an attack from the list of attacks.   
async def prompt_attack(ctx, player):
    # Prompt the player to select an attack
    await ctx.send(f"**Turn of {player.name} starts!** To know your attacks, type: ``!gladiator``.")

    # Wait for the player's response
    def check(msg):
        return msg.author == player and msg.content.lower() in attacks
    attack_msg = await bot.wait_for('message', check=check)

    # Return the selected attack         
    return attack_msg.content.lower()

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name = 'ping')
async def ping(ctx):
    await ctx.send('Pong!')

@bot.command(name = 'challenge')
async def challenge(ctx, opponent: discord.Member):
    accepted = await acceptance(ctx, opponent)

    if accepted == True:
        await duel(ctx, opponent)

@bot.command(name = 'gladiator')
async def gladiator(ctx):
    menu = f""
    for key in attacks:
        menu = menu + f"- {attacks[key]['name']}: -{attacks[key]['damage']}% HP, {attacks[key]['probability'] * 100}% accuracy. ``Use: {key}``\n"
    await ctx.send(f"{ctx.author.mention}:\n {menu}")

bot.run(TOKEN)
