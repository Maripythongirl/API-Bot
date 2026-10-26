import discord
from discord.ext import commands
import requests


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.command()
async def start(ctx):
    await ctx.send("Oi Oi! Seja bem-vindo(a) ao servidor! Sinta-se à vontade e divirta-se")


bot.run("MTU2MTg1OTk5NzA4MjU5MTI2Mg.GvRLb4.FEKmx5ttOW7SP33sVMIZ1Xi82JhIg1-3bUFhK4")