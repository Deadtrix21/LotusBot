from src.utils.base_imports import *
from src.services.LogService import SpecificLog

Logger = SpecificLog(__name__)


class ErrorHandler(Extension):
    def __init__(self, bot):
        self.bot = bot

    # @event_listener()
    # async def on_command_error(self, ctx, error):
    #     if isinstance(error, commands.CommandOnCooldown):
    #         return await ctx.reply(f"Please try again after {humanfriendly.format_timespan(error.retry_after)}.")
    #     if isinstance(error, commands.CommandNotFound):
    #         return await ctx.reply(':woman_shrugging: I do not know that command!')
    #     if isinstance(error, commands.BotMissingPermissions):
    #         return await ctx.reply("I don't have permissions for that!")
    #     if isinstance(error, commands.NotOwner):
    #         return await ctx.reply(f'{ctx.author.mention} Your Not The Owner. Who Are you?')
    #     if isinstance(error, commands.MissingPermissions):
    #         return await ctx.reply(f'Are you trying to be a Hero')
    #     else:
    #         Logger.trace(TracebackException(type(error), error, error.__traceback__, compact=False))


def setup(bot):
    c = ErrorHandler(bot)
    bot.add_cog(c)
