from src.utils.base_imports import *
from src.services.LogService import SpecificLog

from features import Cmds

Logger = SpecificLog(__name__)


class Admin(Extension):
    def __init__(self, bot):
        self.bot = bot

    @commands.guild_only()
    @commands.has_guild_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    @bridge_command(name="kick")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def kick_command(self, ctx, member: DiscordMember, *, reason=None):
        """
        Kicks a member from the server. Reason is required.
        """
        await Cmds.KickDiscordMember(ctx, member, reason=reason)

    @commands.guild_only()
    @commands.has_guild_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    @commands.command(name="mass-kick", aliases=['mk'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def masskick_command(self, ctx, members: commands.Greedy[DiscordMember], *, reason):
        """
        Mass kick multiple members from the server. Reason is required.
        You can only kick users who are in the server.
        """
        await Cmds.MassKickDiscordMember(ctx, members, reason=reason)

    @commands.has_guild_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    @bridge_command(name="ban")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def ban_command(self, ctx, member: DiscordMember, *, reason):
        """
        Bans a member from the server. Reason is required
        You can also ban someone that is not in the server using their user ID.
        """
        await Cmds.BanDiscordMember(ctx, member, reason=reason)

    @commands.guild_only()
    @commands.has_guild_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    @commands.command(name="mass-ban", aliases=['mb'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def massban_command(self, ctx, members: commands.Greedy[DiscordMember], *, reason):
        """
        Mass bans multiple members from the server. Reason is required.
        You can only ban users who are in the server.
        """
        await Cmds.MassBanDiscordMember(ctx, members, reason=reason)

    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    @bridge_command(name="unban")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def unban_command(self, ctx, member):
        """
        Unban a user from server
        """
        try:
            member: DiscordUser = await self.bot.fetch_user(member)
            try:
                await ctx.guild.unban(member)
                await ctx.send(f"{member.name} has been unbanned.")
            except Exception as EE:
                print(EE)
                await ctx.send("This user  was never banned or on this server")
        except Exception as E:
            print(E)
            await ctx.send("User Does Not Exist")

    @commands.guild_only()
    @bridge_command(name="invite")
    async def invite_command(self, ctx):
        """
        Create a server invite
        """
        await ctx.send(await create_invite(ctx.message.channel))

    @commands.guild_only()
    @commands.has_guild_permissions(moderate_members=True)
    @commands.bot_has_permissions(moderate_members=True)
    @bridge_command(name="timeout", aliases=['mute'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def timeout_command(self, ctx, member: DiscordMember, time, *, reason=None):
        """
        Mute's a member for specific time.
        Use 5m for 5 mins, 1hr for 1 hour etc...
        """
        if reason is None:
            reason = 'No reason provided'
        time = humanfriendly.parse_timespan(time)
        await member.timeout(until=arrow.utcnow() + datetime.timedelta(seconds=time), reason=reason)
        await ctx.send(f"{member} has been muted for {time}.\nReason: {reason}")

    @commands.guild_only()
    @commands.has_guild_permissions(moderate_members=True)
    @commands.bot_has_permissions(moderate_members=True)
    @bridge_command(name="unmute")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def unmute_command(self, ctx, member: DiscordMember, *, reason=None):
        """
        Unmutes a member.
        """
        if reason is None:
            reason = 'No reason provided'
        await member.remove_timeout(reason=reason)
        await ctx.send(f"{member} has been unmuted!")

    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    @bridge_command(name="prune")
    async def prune_command(
            self,
            ctx: commands.Context,
            count: int,
    ) -> None:
        """
        Pruges messages from the chat
        """
        resp = await ctx.channel.purge(limit=count, bulk=True)
        await ctx.send(f"Deleted {len(resp)} messages.", delete_after=5)

    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    @bridge_command(name="clean")
    async def clean_command(self, ctx: commands.Context) -> None:
        """
        Cleans up messages left by the bot
        :param ctx:
        :return:
        """

        def is_me(m: discord.Message) -> bool:
            return m.author == self.bot.user

        resp = await ctx.channel.purge(limit=100, check=is_me)
        await ctx.send(f"Deleted {len(resp)} messages.", delete_after=5)


def setup(bot):
    cog = Admin(bot)
    bot.add_cog(cog)
