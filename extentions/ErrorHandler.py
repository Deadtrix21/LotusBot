import traceback

from utils.CommonImports import *


class ErrorHandler(Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.reply(':woman_shrugging: I do not know that command!')
        if isinstance(error, commands.BotMissingPermissions):
            await ctx.reply("I don't have permissions for that!")
        if isinstance(error, commands.NotOwner):
            await ctx.reply(f'{ctx.author.mention} Your Not The Owner. Who Are you?')
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply(f'Are you trying to be a Hero')
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.reply(f"Please try again after {round(error.retry_after, 2)} seconds")
        else:
            print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)


def setup(bot):
    c = ErrorHandler(bot)
    bot.add_cog(c)
