import discord
from discord.ext import commands
from discord.ext.commands.errors import MissingRequiredArgument, MissingPermissions, MemberNotFound, BadArgument

class moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        if ctx.author.top_role <= member.top_role or member.id == ctx.guild.owner_id or member.id == ctx.author.id:
            await ctx.send("You can't do that sh*t")
        else:
            await ctx.send("Let me handle")
            await member.kick(reason=reason)
            await ctx.send(f"{member.mention} has been kicked")
    
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        if ctx.author.top_role <= member.top_role or member.id == ctx.guild.owner_id or member.id == ctx.author.id:
            await ctx.send("You can't do that sh*t")
        else:
            await member.ban(reason=reason)
            await ctx.send(f"{member.mention} has been banned")
    
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, user_id: str, reason=None):
        bans = [entry.user.id async for entry in ctx.guild.bans()]
        member = await self.bot.fetch_user(user_id)
        await ctx.guild.unban(member, reason=reason)
        await ctx.send(f"{member.mention}is unbanned.")

    @commands.command(aliases=["clear"])
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int):
        await ctx.message.delete()
        if amount > 0:
            if amount > 100:
                message = await ctx.send("Reach the limit")
                await message.delete(delay=1)
                amount = 100
            deleted = await ctx.channel.purge(limit = amount)
            message = await ctx.send(f"Done. Delete {len(deleted)} messages.")
            await message.delete(delay=2)
        else:
            await ctx.send("Dafuq")
        

    @purge.error
    async def purge_error(self, ctx, error):
        if isinstance(error, MissingRequiredArgument):
            await ctx.send("add number to execute command")
        elif isinstance(error, BadArgument):
            await ctx.send("PLS use number you dumbsh#t")
    
    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.send("You don't have permission")
        elif isinstance(error, MemberNotFound):
            await ctx.send("The user not available in server")
        elif isinstance(error, MissingRequiredArgument):
            await ctx.send("Choose a member to kick")
        print(error)
    
    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, MissingRequiredArgument):
            await ctx.send("Choose a member to ban")
        print(error)
    
    @unban.error
    async def unban_error(self, ctx, error):
        print(error)


async def setup(bot):
    await bot.add_cog(moderation(bot))