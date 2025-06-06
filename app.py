import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio
import logging

load_dotenv()

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=".", intents=intents, help_command=None)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
discord.utils.setup_logging(handler=handler, level=logging.INFO)

async def event_load():
    for filename in os.listdir('./events'):
        if filename.endswith('.py'):
            extension = f"events.{filename[:-3]}"
            try:
                await bot.load_extension(extension)
                print(f"📦 Loaded events: {extension}")
            except Exception as e:
                print(f"❌ Failed to load cog {extension}: {e}")

async def command_load():
    for filename in os.listdir('./commands'):
        if filename.endswith('.py'):
            extension = f"commands.{filename[:-3]}"
            try:
                await bot.load_extension(extension)
                print(f"📦 Loaded commands: {extension}")
            except Exception as e:
                print(f"❌ Failed to load cog {extension}: {e}")

async def main():
    async with bot:
        await event_load()
        await command_load()
        await bot.start(TOKEN)

try:
    asyncio.run(main())
except KeyboardInterrupt:
    logging.warning("Bot was stopped manually (KeyboardInterrupt).")