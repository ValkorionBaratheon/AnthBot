import discord
import json
import random


with open('config.json', 'r') as f:
    config = json.load(f)

intents = discord.Intents.default()
intents.members = True
intents.messages = True
client = discord.Client(intents=intents)

def get_attack_result(attack_power):
    """Simulates an attack and returns a boolean indicating if the attack was successful."""
    return random.randint(1, 100) <= attack_power

def get_attack_power():
    """Returns a random attack power between 1 and 100."""
    return random.randint(1, 100)

async def fight(ctx, opponent):
    """Simulates a battle between the user who invoked the !battle command and the specified opponent."""
    # Determine attack power for each player
    user_attack_power = get_attack_power()
    opponent_attack_power = get_attack_power()

    # Simulate attacks
    user_attack_result = get_attack_result(user_attack_power)
    opponent_attack_result = get_attack_result(opponent_attack_power)

    # Determine winner
    if user_attack_result and not opponent_attack_result:
        result = f'{ctx.author.mention} wins!'
    elif not user_attack_result and opponent_attack_result:
        result = f'{opponent.mention} wins!'
    else:
        result = 'It\'s a tie!'

    # Send battle result to channel
    await ctx.send(result)

@client.event
async def on_ready():
    print(f'Logged in as {client.user.name} (ID: {client.user.id})')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith(config['prefix']):
        command = message.content.split([0][len(config['prefix']):].lower())

        if command == 'ping':
            await message.channel.send('Pong!')

        elif command == 'hello':
            await message.channel.send(f'Hello, {message.author.mention}!')

        elif command == 'battle':
            opponent = message.mentions[0]
            await fight(message.channel, opponent)

client.run(config['bot_token'])
