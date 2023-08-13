from ...Utilities.Imports.SysImports import *
from ...Utilities.Imports.DiscordImports import *


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bridge.bridge_command()
    @commands.guild_only()
    @commands.has_guild_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        """
        Kicks a member from the server. Reason is required.
        """
        if not reason:
            reason = "No reason provided."

        await member.kick(reason=reason)
        await ctx.send(f'Kicked `{member}`')

    @bridge.bridge_command()
    @commands.has_guild_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def ban(self, ctx, member: discord.Member, *, reason):
        """
        Bans a member from the server. Reason is required
        You can also ban someone that is not in the server using their user ID.
        """
        if reason:
            if isinstance(member, int):
                await ctx.guild.ban(discord.Object(id=member), reason=f"{reason}")
                user = await self.bot.fetch_user(member)
                await ctx.send(f'Banned `{user}`')
            else:
                await member.ban(reason=f"{reason}", delete_message_days=0)
                await ctx.send(f'Banned `{member}`')
        else:
            await ctx.send(f"Provide a reason to ban this user.")

    @commands.command(aliases=['mb'])
    @commands.guild_only()
    @commands.has_guild_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def massban(self, ctx, members: commands.Greedy[discord.Member], *, reason):
        """
        Mass bans multiple members from the server. Reason is required.
        You can only ban users who are in the server.
        """
        if not len(members):
            await ctx.send('One or more required arguments are missing.')

        else:
            for target in members:
                await target.ban(reason=reason, delete_message_days=0)
                await ctx.send(f'Banned `{target}`')

    @bridge.bridge_command()
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, member):
        """
        Unban a user from server
        """
        try:
            member: discord.User = await self.bot.fetch_user(member)
            try:
                await ctx.guild.unban(member)
                await ctx.send(f"{member.name} has been unbanned.")
            except Exception as EE:
                print(EE)
                await ctx.send("This user  was never banned or on this server")
        except Exception as E:
            print(E)
            await ctx.send("User Does Not Exist")

    @bridge.bridge_command()
    @commands.guild_only()
    async def invite(self, ctx):
        """
        Create a server invite
        """
        await ctx.send(await discord.abc.GuildChannel.create_invite(ctx.message.channel))

    @bridge.bridge_command(aliases=['mute'])
    @commands.guild_only()
    @commands.has_guild_permissions(moderate_members=True)
    @commands.bot_has_permissions(moderate_members=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def timeout(self, ctx, member: discord.Member, time, *, reason=None):
        """
        Mute's a member for specific time.
        Use 5m for 5 mins, 1hr for 1 hour etc...
        """
        if reason is None:
            reason = 'No reason provided'
        time = humanfriendly.parse_timespan(time)
        await member.timeout(until=discord.utils.utcnow() + datetime.timedelta(seconds=time), reason=reason)
        await ctx.send(f"{member} has been muted for {time}.\nReason: {reason}")

    @bridge.bridge_command()
    @commands.guild_only()
    @commands.has_guild_permissions(moderate_members=True)
    @commands.bot_has_permissions(moderate_members=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def unmute(self, ctx, member: discord.Member, *, reason=None):
        """
        Unmutes a member.
        """
        if reason is None:
            reason = 'No reason provided'
        await member.remove_timeout(reason=reason)
        await ctx.send(f"{member} has been unmuted!")


def setup(bot):
    cog = Admin(bot)
    bot.add_cog(cog)
