# duel.py

import asyncio
import discord
from discord.ext import commands
from .player import Player
from .game import Game

class Challenge(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Waits for opponent to accept or deny challenge, returns true or false
    async def acceptance(self, ctx, player1, player2):
        # Send initial message and wait for response
        await ctx.send(f"**{player1.name} has dared to challenge {player2.mention}!**\n\nWill you accept?\n\nRespond with ``yes`` or ``no``.")

        # Wait for the opponent's response
        def check(msg):
            return msg.author == player2
        
        try:
            response = await self.bot.wait_for('message', check=check, timeout=60.0)
        except asyncio.TimeoutError:
            await ctx.send(f"{player2.mention} was so afraid that they went ahead and died, failing to respond!")
            return False
        
        # Process user's response
        if response.content.lower() == "yes":
            await ctx.send(f"**An epic battle between {ctx.author.mention} and {player2.mention} has begun!** Good luck to both!")
            return True
        else:
            await ctx.send(f"It seems {player2.mention} lacked the courage to honor your duel.")
            return False

    @commands.command(name = 'challenge')
    async def challenge(self, ctx, opponent: discord.Member):
        accepted = await self.acceptance(ctx, ctx.author, opponent)

        if accepted == True:
            challenger = Player(ctx.author)
            defender = Player(opponent)
            new_game = Game(self.bot, ctx, challenger, defender)
            await new_game.duel()

    @commands.command(name = 'gladiator')
    async def gladiator(self, ctx):
        menu = f""
        for key in Game.attacks:
            menu = menu + f"- {Game.attacks[key]['name']}: -{Game.attacks[key]['damage']}% HP, {Game.attacks[key]['probability'] * 100}% accuracy. ``Use: {key}``\n"
        await ctx.send(f"{ctx.author.mention}:\n {menu}")

async def setup(bot):
    await bot.add_cog(Challenge(bot))
