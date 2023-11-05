from src.utils.base_imports import *


async def BanDiscordMember(ctx: commands.Context, member: DiscordMember, *, reason=None):
    if reason:
        await member.ban(reason=f"{reason}", delete_message_days=0)
        await ctx.send(f'Banned `{member}`')
    else:
        await ctx.send(f"Provide a reason to ban this user.")


async def MassBanDiscordMember(ctx: commands.Context, member: commands.Greedy[DiscordMember], *, reason=None):
    if not len(member):
        await ctx.send('One or more required arguments are missing.')
    else:
        for target in member:
            await target.ban(reason=reason)
            await ctx.send(f'Banned `{target}`')
