import discord
from discord.ext import commands
from database import db

class Ready(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        await db.init_db()
        print(f"✅ Logged in as {self.bot.user}")

async def setup(bot):
    await bot.add_cog(Ready(bot))