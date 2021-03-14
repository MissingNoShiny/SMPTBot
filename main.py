import socket

from configparser import ConfigParser

import discord

from discord.ext import commands, tasks
from mcstatus import MinecraftServer

server = MinecraftServer.lookup("smpt.schnaps.fun")

bot = commands.Bot(command_prefix="!")


@tasks.loop(seconds=15)
async def update_activity():
    try:
        player_count = server.status().players.online
        s = '' if player_count == 1 else 's'
        await bot.change_presence(status=discord.Status.online,
                                  activity=discord.Game(name=f"{player_count} joueur{s} connecté{s}"))
    except socket.timeout:
        await bot.change_presence(status=discord.Status.idle, activity=None)


@bot.command()
async def online(ctx: commands.Context):
    try:
        player_list = server.status().players.sample
        await ctx.send(f"Joueurs en ligne : {', '.join([player.name for player in player_list])}")
    except socket.timeout:
        await ctx.send("Le serveur est hors-ligne ou n'a pas pu être contacté")


@bot.event
async def on_ready():
    print("Ready")
    update_activity.start()


if __name__ == "__main__":

    config = ConfigParser()
    config.read('config.ini')
    token = config['discord']['token']
    bot.run(token)
