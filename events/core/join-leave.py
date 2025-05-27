import discord
from discord.ext import commands
from database import db
import datetime

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        joined_at = datetime.datetime.now(datetime.UTC).isoformat()
        await db.add_user(member.id, str(member), joined_at)
        await db.log_action(member.id, "joined", joined_at)

        channel = discord.utils.get(member.guild.text_channels, name="general")
        if channel:
            await channel.send(f"👋 Welcome {member.mention} to the server!")

async def setup(bot):
    await bot.add_cog(Events(bot))