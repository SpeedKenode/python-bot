import discord
from discord.ext import commands, tasks
from database import db
from datetime import datetime, timedelta, timezone
import re

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check_mutes.start()
    
    @tasks.loop(seconds=5.0)
    async def check_mutes(self):
        guild = self.bot.get_guild(1370971931255242854)
        muted_role = discord.utils.get(guild.roles, name="Muted")
        data = await db.get_mute()
        for i in data:
            user_id = i[0]
            day = i[1]
            member = guild.get_member(user_id)
            date = datetime.strptime(day, "%Y-%m-%d %H:%M:%S")
            current = datetime.now()
            if current >= date:
                if muted_role and muted_role in member.roles:
                    try:
                        await member.remove_roles(muted_role, reason="Mute expired")
                        await db.remove_mute(user_id, day)
                    except Exception:
                        continue
    
    @check_mutes.before_loop
    async def before_check_mutes(self):
        await self.bot.wait_until_ready()
    
    async def send_modlog(self, ctx, member, reason, action: str):
        channel_id = await db.get_modlog()
        if channel_id:
            channel = ctx.guild.get_channel(channel_id)
            if channel:
                embed = discord.Embed(title=f"User {action}")
                embed.add_field(name="User", value=member.mention)
                embed.add_field(name="By", value=ctx.author.mention)
                embed.add_field(name="Reason", value=reason, inline=False)
                embed.timestamp = datetime.now(timezone.utc)
                await channel.send(embed=embed)
                day = datetime.now(timezone(timedelta(hours=7))).strftime('%Y-%m-%d %H:%M:%S')
                await db.mod_log(member.name, member.id, ctx.author.name, ctx.author.id, f"{action}: {reason}", f"{day}")
    
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        """Kick a member"""
        if ctx.author.top_role <= member.top_role or member.id == ctx.guild.owner_id or member.id == ctx.author.id:
            await ctx.send("You don't have permission to do this.")
        else:
            await member.kick(reason=reason)
            msg_embed = discord.Embed()
            msg_embed.add_field(name="", value=f"{member.mention} has been kicked")
            await ctx.send(embed=msg_embed)
            await self.send_modlog(ctx, member, reason, "Kicked")
    
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        """Ban a member"""
        if ctx.author.top_role <= member.top_role or member.id == ctx.guild.owner_id or member.id == ctx.author.id:
            await ctx.send("You don't have permission to do this.")
        else:
            await member.ban(reason=reason)
            msg_embed = discord.Embed()
            msg_embed.add_field(name="", value=f"{member.mention} has been banned")
            await ctx.send(embed=msg_embed)
            await self.send_modlog(ctx, member, reason, "Banned")
    
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, user_id: int, reason=None):
        """Unban a member"""
        bans = [entry.user.id async for entry in ctx.guild.bans()]
        if user_id in bans:
            member = await self.bot.fetch_user(user_id)
            await ctx.guild.unban(member, reason=reason)
            msg_embed = discord.Embed()
            msg_embed.add_field(name="", value=f"{member.mention} has been unbanned")
            await self.send_modlog(ctx, member, reason, "Unbanned")
        else:
            await ctx.send("Not found")

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member, duration: str = None, *, reason="No reason provided"):
        """Mute a member"""
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not muted_role:
            muted_role = await ctx.guild.create_role(name="Muted")
            print(muted_role.id)
        for channel in ctx.guild.channels:
            await channel.set_permissions(muted_role, send_messages=False, speak=False, add_reactions=False)

        if muted_role in member.roles:
            return await ctx.send("❌ That member is already muted.")

        await member.add_roles(muted_role, reason=reason)
        await ctx.send(f"🔇 {member.mention} has been muted. Reason: {reason}")
        await self.send_modlog(ctx, member, reason, "Muted")

        def parse_duration(duration: str) -> int:
            match = re.match(r"^(\d+)([smhd])$", duration.lower())
            if not match:
                return None
            amount, unit = match.groups()
            amount = int(amount)

            unit_multipliers = {
                "s": 1,
                "m": 60,
                "h": 3600,
                "d": 86400,
            }
            return amount * unit_multipliers[unit]

        unmute_time = None
        if duration:
            seconds = parse_duration(duration)
            if not seconds:
                return await ctx.send("⚠️ Invalid duration format. Use `10m`, `1h`, `2d`.")
            unmute_time = datetime.now() + timedelta(seconds=seconds)
            await db.add_mute(
                user_id=member.id,
                unmute_time=unmute_time.isoformat(" ", "seconds"),
            )

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member):
        """Unmute a member"""
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
        removed = False
        if muted_role and muted_role in member.roles:
            try:
                await member.remove_roles(muted_role, reason=f"Unmuted by {ctx.author}")
                await self.send_modlog(ctx, member, f"Unmuted by {ctx.author}", "Muted")
                removed = True
            except discord.Forbidden:
                return await ctx.send("❌ I don't have permission to remove the Muted role from this user.")
            except Exception as e:
                return await ctx.send(f"❌ Failed to remove Muted role: {e}")

        if removed:
            await ctx.send(f"✅ {member.mention} has been unmuted.")
        else:
            await ctx.send(f"ℹ️ {member.mention} had no muted role, but any mute record has been cleared.")
    

    @commands.command()
    @commands.has_permissions(moderate_members=True)
    async def warn(self, ctx, member: discord.Member, *, reason=None):
        """Warns a user"""
        if ctx.author.top_role <= member.top_role or member.id == ctx.guild.owner_id or member.id == ctx.author.id:
            await ctx.send("You don't have permission to do this.")
        else:
            msg_embed = discord.Embed()
            msg_embed.add_field(name="", value=f"{member.mention} has been warned")
            await ctx.send(embed=msg_embed)
            await self.send_modlog(ctx, member, reason, "Warned")

            day = datetime.now(timezone(timedelta(hours=7))).strftime('%Y-%m-%d %H:%M:%S')
            await db.warn_case(member.name, member.id, ctx.author.name, ctx.author.id, f"Warn: {reason}", f"{day}")
    
    @commands.command(aliases=["clear"])
    @commands.has_permissions(manage_channels=True)
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
    
    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def lock(self, ctx, channel: discord.TextChannel = None):
        """Lock a channel"""
        channel = channel or ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = False
        overwrite.add_reactions = False
        overwrite.send_messages_in_threads = False
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        await ctx.send(f"🔒 {channel.mention} has been locked.")
    
    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, ctx, channel: discord.TextChannel = None):
        """Unlock a channel"""
        channel = channel or ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = True
        overwrite.add_reactions = True
        overwrite.send_messages_in_threads = True
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        await ctx.send(f"🔓 {channel.mention} has been unlocked.")

async def setup(bot):
    await bot.add_cog(Moderation(bot))