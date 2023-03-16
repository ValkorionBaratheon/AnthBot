# This file contains the classes Game() and its subclass Player() that both correspond to the !challenge command.

import random

class Game:
    def __init__(self, bot, ctx, player1, player2):
        self.bot = bot
        self.ctx = ctx
        self.player2 = player1
        self.player2 = player2
        self.players = [player1, player2]
        self.game_over = False
        self.round_count = 1
        self.attacks = {
            "k": {"name": "Katana", "damage": 20, "probability": 0.8},
            "b": {"name": "Crossbow", "damage": 60, "probability": 0.50},
            "r": {"name": "Capture Net", "damage": 80, "probability": 0.20}
        }

    # Simulates a battle between the user who invoked the !challenge command and the specified opponent.
    async def duel(self):
        # Alternate between players selecting attacks until one player has 0 health
        while self.game_over == False:
            await self.round()

        # Determine and send battle result
        await self.ctx.send(self.result())

    async def round(self):
        for x in range(len(self.players)):
            await self.ctx.send(f"**[Round {self.round_count}]**\n\nFighters'current HP: {self.players[0].user.mention} ({self.players[0].health}%) - {self.players[1].user.mention} ({self.players[1].health}%)")
            if self.players[x].turn_status == True:
                await self.turn(self.players[x], self.players[(x + 1) % len(self.players)])
                self.players[x].turn_status = False
                self.players[(x + 1) % len(self.players)].turn_status = True
                self.game_over = self.battle_over()
        self.round_count += 1

    async def turn(self, attacker, defender):
        if attacker.turn_status == True:
            move = await self.prompt_attack(attacker)
            attack_msg = f"**{attacker.user.name}** attacks **{defender.user.name}** with **{self.attacks[move]['name']}**."
            if random.random() < self.attacks[move]['probability']:
                defender.set_health(self.attacks[move]['damage'])
                await self.ctx.send(f"{attack_msg} It successfully removed **{self.attacks[move]['damage']} life!**")
            else:
                await self.ctx.send(f"{attack_msg} The attack **failed.**")

    # Prompts the specified player to select an attack from the list of attacks.   
    async def prompt_attack(self, player):
        # Prompt the player to select an attack
        await self.ctx.send(f"**Turn of {player.user.name} starts!** To know your attacks, type: ``!gladiator``.")

        # Wait for the player's response
        def check(msg):
            return msg.author == player and msg.content.lower() in self.attacks
        attack_msg = await self.bot.wait_for('message', check=check)

        # Return the selected attack         
        return attack_msg.content.lower()

    async def battle_over(self):
        if self.players[0].health <= 0 or self.players[1].health <= 0:
            return True
        else:
            return False

    async def result(self):
        if self.players[0].dead == True:
            winner = f"**The battle ends!** {self.players[1].user.mention} wins!"
        else:
            winner = f"**The battle ends!** {self.players[0].user.mention} wins!"
        return winner
