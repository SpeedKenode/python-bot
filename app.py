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

@bot.command(name="ping", description="Pong")
async def ping(ctx):
    await ctx.message.delete()
    embed = discord.Embed(
        title="🏓 Pong!",
        description=f"The latency is {round(bot.latency * 1000)} ms",
        color=discord.Colour.blue()
    )
    await ctx.send(embed=embed)

"""
@bot.command(name='deletecommands', aliases=['clear'])
@commands.has_any_role('Owner')
async def delete_commands(ctx):
    bot.tree.clear_commands(guild=None)
    await bot.tree.sync()
    await ctx.send('Commands deleted.')
"""

bot.run(token, log_handler=handler, log_level=logging.DEBUG)