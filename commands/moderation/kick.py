import discord
from discord.ext import commands
from database import db
import datetime
from datetime import datetime, timedelta, timezone

class KickCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason="No reason provided"):
        await member.kick(reason=reason)
        await ctx.send(f"👢 {member.mention} was kicked. Reason: {reason}")
        day = datetime.now(timezone(timedelta(hours=7))).strftime('%Y-%m-%d %H:%M:%S')
        await db.mod_log(member.name, member.id, ctx.author.name, ctx.author.id, f"Kicked: {reason}", f"{day}")

async def setup(bot):
    await bot.add_cog(KickCommand(bot))