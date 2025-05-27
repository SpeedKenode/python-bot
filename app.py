import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio
import logging
from database import db

load_dotenv()

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=".", intents=intents)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

@bot.event
async def on_ready():
    await db.init_db()
    print(f"✅ Logged in as {bot.user}")

# Load command cogs
async def command_load(base="commands"):
    for root, _, files in os.walk(base):
        for file in files:
            if file.endswith(".py") and not file.startswith("_"):
                filepath = os.path.join(root, file)
                cog_path = filepath.replace("/", ".").replace("\\", ".")[:-3]
                try:
                    await bot.load_extension(cog_path)
                    print(f"✅ Loaded command: {cog_path}")
                except Exception as e:
                    print(f"❌ Failed to load command {cog_path}: {e}")

# Load event cogs
async def event_load(base="events"):
    for root, _, files in os.walk(base):
        for file in files:
            if file.endswith(".py") and not file.startswith("_"):
                filepath = os.path.join(root, file)
                cog_path = filepath.replace("/", ".").replace("\\", ".")[:-3]
                try:
                    await bot.load_extension(cog_path)
                    print(f"✅ Loaded event: {cog_path}")
                except Exception as e:
                    print(f"❌ Failed to load event {cog_path}: {e}")

async def main():
    await asyncio.gather(command_load(), event_load())

asyncio.run(main())

bot.run(TOKEN, log_handler=handler, log_level=logging.DEBUG)