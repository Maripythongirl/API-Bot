import discord
from discord.ext import commands
import requests


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.command()
async def start(ctx):
    await ctx.send("Oi Oi! Seja bem-vindo(a) ao servidor! Sinta-se à vontade e divirta-se")


bot.run("")
