# duel.py
import asyncio
import discord
import random
from discord.ext import commands

class Duel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Dictionary storing all attack names, damages, and probabilities of success
    attacks = {
        "k": {"name": "Katana", "damage": 20, "probability": 0.8},
        "b": {"name": "Crossbow", "damage": 60, "probability": 0.50},
        "r": {"name": "Capture Net", "damage": 80, "probability": 0.20}
    }

    # Waits for opponent to accept or deny challenge, returns true or false
    async def acceptance(self, ctx, opponent):
        # Send initial message and wait for response
        await ctx.send(f"**{ctx.author.name} has dared to challenge {opponent.mention}!**\n\nWill you accept?\n\nRespond with ``yes`` or ``no``.")

            # Wait for the opponent's response
        def check(msg):
            return msg.author == opponent
        
        try:
            response = await self.bot.wait_for('message', check=check, timeout=60.0)
        except asyncio.TimeoutError:
            await ctx.send(f"{opponent.mention} was so afraid that they went ahead and died, failing to respond!")
            return False
        
        # Process user's response
        if response.content.lower() == "yes":
            await ctx.send(f"**An epic battle between {ctx.author.mention} and {opponent.mention} has begun!** Good luck to both!")
            return True
        else:
            await ctx.send(f"It seems {opponent.mention} lacked the courage to honor your duel.")
            return False
    
    # Simulates a battle between the user who invoked the !challenge command and the specified opponent.
    async def duel(self, ctx, opponent):
        # Initialize health for each player
        players = [opponent, ctx.author]
        healths = [100, 100]
        round = 1
        over_battle = False
        
        # Alternate between players selecting attacks until one player has 0 health
        while over_battle == False:
            for x in range(len(healths)):
                await ctx.send(f"**[Round {round}]**\n\nFighters'current HP: {ctx.author.mention} ({healths[1]}%) - {opponent.mention} ({healths[0]}%)")
                healths[(x + 1) % len(healths)] = await self.turn(ctx, players[x], players[(x + 1) % len(players)], healths[(x + 1) % len(healths)])
                over_battle = await self.battle_over(healths[1], healths[0])

            round +=1

        # Determine winner
        if healths[1] > 0:
            result = f"**The battle ends!** {ctx.author.mention} wins!"
        else:
            result = f"**The battle ends!** {opponent.mention} wins!"

        # Send battle result to channel
        await ctx.send(result)

    async def turn(self, ctx, player, other, other_health):
        player_attack = await self.prompt_attack(ctx, player)
        
        if random.random() < self.attacks[player_attack]["probability"]:
            player_damage = self.attacks[player_attack]["damage"]
            other_health -= player_damage
            await ctx.send(f"**{player.name}** attacks **{other.name}** with **{self.attacks[player_attack]['name']}**. It successfully removed **{player_damage} life!**")
        else:
            await ctx.send(f"**{player.name}** attacks **{other.name}** with **{self.attacks[player_attack]['name']}**. The attack **failed.**")

        return other_health

    async def battle_over(self, challenger_health, opponent_health):
        if challenger_health <= 0 or opponent_health <= 0:
            return True
        else:
            return False

    # Prompts the specified player to select an attack from the list of attacks.   
    async def prompt_attack(self, ctx, player):
        # Prompt the player to select an attack
        await ctx.send(f"**Turn of {player.name} starts!** To know your attacks, type: ``!gladiator``.")

        # Wait for the player's response
        def check(msg):
            return msg.author == player and msg.content.lower() in self.attacks
        attack_msg = await self.bot.wait_for('message', check=check)

        # Return the selected attack         
        return attack_msg.content.lower()

    @commands.command(name = 'challenge')
    # Waits for opponent to accept or deny challenge, returns true or false
    async def challenge(self, ctx, opponent: discord.Member):
        accepted = await self.acceptance(ctx, opponent)

        if accepted == True:
            await self.duel(ctx, opponent)

    @commands.command(name = 'gladiator')
    async def gladiator(self, ctx):
        menu = f""
        for key in self.attacks:
            menu = menu + f"- {self.attacks[key]['name']}: -{self.attacks[key]['damage']}% HP, {self.attacks[key]['probability'] * 100}% accuracy. ``Use: {key}``\n"
        await ctx.send(f"{ctx.author.mention}:\n {menu}")

async def setup(bot):
    await bot.add_cog(Duel(bot))
