import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import logging
import asyncio

load_dotenv()
token = os.getenv('TOKEN')

intents = discord.Intents.all()

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
bot = commands.Bot(command_prefix="!", intents=intents)

async def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f"cogs.{filename[:-3]}")

asyncio.run(load())

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    await bot.tree.sync()

@bot.hybrid_command(name="ping", description="Pong")
async def ping(ctx: commands.Context):
    try:
        await ctx.message.delete()
    except:
        print()
    embed = discord.Embed(
        title="🏓 Pong!",
        description=f"The latency is {round(bot.latency * 1000)} ms",
        color=discord.Colour.blue()
    )
    await ctx.send(embed=embed)

bot.run(token, log_handler=handler, log_level=logging.DEBUG)