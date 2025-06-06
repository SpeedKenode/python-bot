import discord
from discord.ext import commands
from database import db

class JoinLeave(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel_id = await db.get_welcome()
        channel = discord.utils.get(member.guild.channels, id=channel_id)
        await channel.send(f"{member} join the server")
    
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel_id = await db.get_goodbye()
        channel = discord.utils.get(member.guild.channels, id=channel_id)
        await channel.send(f"{member} leave the server")

async def setup(bot):
    await bot.add_cog(JoinLeave(bot))