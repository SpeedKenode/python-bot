import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    async def help(self, ctx, *, command_name=None):
        """Show help for all commands or a specific one."""
        prefix = "."
        if command_name is None:
            embed = discord.Embed(title="📖 Help Menu", description="List of available commands:", color=discord.Color.blurple())
            for cog in self.bot.cogs:
                cog_commands = self.bot.get_cog(cog).get_commands()
                filtered = [cmd for cmd in cog_commands if not cmd.hidden]
                if filtered:
                    embed.add_field(
                        name=f"📁 {cog}",
                        value=" ".join(f"`{cmd.name}`" for cmd in filtered),
                        inline=False
                    )
            embed.set_footer(text=f"Use {prefix}help <command> for more details.")
            await ctx.send(embed=embed)
        
        else:
            command = self.bot.get_command(command_name)
            if command is None:
                await ctx.send(f"❌ Command `{command_name}` not found.")
                return

            embed = discord.Embed(title=f"🛠️ Help: `{command.name}`", color=discord.Color.green())
            embed.add_field(name="Description", value=command.help or "No description.", inline=False)
            embed.add_field(name="Usage", value=f"`{prefix}{command.qualified_name} {command.signature}`", inline=False)
            if command.aliases:
                embed.add_field(name="Aliases", value=", ".join(f"`{a}`" for a in command.aliases), inline=False)
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Help(bot))