import discord
from discord.ext import commands
from database import db

class Setup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(aliases=["log"])
    async def setmodlog(self, ctx, channel: discord.TextChannel):
        """Set mod log"""
        await db.set_modlog_channel(channel.id)
        await ctx.send(f"✅ Modlog channel set to {channel.mention}")
    
    @commands.command(aliases=["welcome"])
    async def setwelcomechannel(self, ctx, channel: discord.TextChannel):
        """Set welcome channel"""
        await db.set_modlog_channel(channel.id)
        await ctx.send(f"✅ Modlog channel set to {channel.mention}")
    
    @commands.command(aliases=["goodbye"])
    async def setgoodbyechannel(self, ctx, channel: discord.TextChannel):
        """Set goodbye channel"""
        await db.set_modlog_channel(channel.id)
        await ctx.send(f"✅ Modlog channel set to {channel.mention}")

async def setup(bot):
    await bot.add_cog(Setup(bot))