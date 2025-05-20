import discord
from discord.ext import commands
from discord.ext.commands.errors import MissingPermissions, MissingRequiredArgument, BadArgument

class moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f"{member.mention} has been kicked")
    
    @commands.command()
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f"{member.mention} has been banned")
    
    @commands.command()
    async def unban(self, ctx, user_id: str, reason=None):
        bans = [entry.user.id async for entry in ctx.guild.bans()]
        member = await self.bot.fetch_user(user_id)
        await ctx.guild.unban(member)
        await ctx.send(f"{member.mention}is unbanned.")

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int):
        await ctx.message.delete()
        if amount > 0:
            if amount > 10:
                message = await ctx.send("Reach the limit")
                await message.delete(delay=1)
                amount = 10
            deleted = await ctx.channel.purge(limit = amount)
            message = await ctx.send(f"Done. Delete {len(deleted)} messages.")
            await message.delete(delay=2)
        else:
            await ctx.send("Dafuq")
        

    @purge.error
    async def purge_error(self, ctx: commands.Context, error):
        if isinstance(error, MissingPermissions):
            await ctx.send("You don't have permission")
        elif isinstance(error, MissingRequiredArgument):
            await ctx.send("add number to execute command")
        elif isinstance(error, BadArgument):
            await ctx.send("PLS use number you dumbsh#t")
        else:
            print(error)


async def setup(bot):
    await bot.add_cog(moderation(bot))