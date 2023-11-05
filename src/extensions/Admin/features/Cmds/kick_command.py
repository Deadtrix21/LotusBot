from src.utils.base_imports import *


async def KickDiscordMember(ctx: commands.Context, member: DiscordMember, *, reason=None):
    if not reason:
        reason = "No reason provided."
    await member.kick(reason=reason)
    await ctx.send(f'Kicked `{member}`')


async def MassKickDiscordMember(ctx: commands.Context, member: commands.Greedy[DiscordMember], *, reason=None):
    if not len(member):
        await ctx.send('One or more required arguments are missing.')
    else:
        for target in member:
            await target.kick(reason=reason)
            await ctx.send(f'Banned `{target}`')
