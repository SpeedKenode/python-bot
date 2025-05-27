from discord.ext import commands

class PingCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        user_id = ctx.author.id
        username = str(ctx.author)
        await self.bot.db.add_user(user_id, username)
        await ctx.send(f"The latency is {round(self.bot.latency * 1000)} ms")

async def setup(bot):
    await bot.add_cog(PingCommand(bot))