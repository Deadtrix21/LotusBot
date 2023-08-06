import traceback

from utils.CommonImports import *
from utils.DiscordImports import *
import classes

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

        if isinstance(error, UserNotRegistered):
            if error.member:
                await ctx.reply(f"{error.member.display_name} is not registered.")
            else:
                await ctx.reply(f"You {ctx.author.mention} are not registered.")
        if isinstance(error, UserNotRegisteredForTax):
            await ctx.reply(f"You {ctx.author.mention} are not registered for tax.")
        if isinstance(error, UserRegisteredForTax):
            await ctx.reply(f"You {ctx.author.mention} are already registered for tax.")
        else:
            print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

def setup(bot):
    c = ErrorHandler(bot)
    bot.add_cog(c)
