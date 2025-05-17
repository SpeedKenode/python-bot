import discord
from discord.ext import commands

class joinleave(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = discord.utils.get(member.guild.channels, id=1371671656816443544)
        await channel.send(f"{member} join the server")
    
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = discord.utils.get(member.guild.channels, id=1371671656816443544)
        await channel.send(f"{member} leave the server")

async def setup(bot):
    await bot.add_cog(joinleave(bot))