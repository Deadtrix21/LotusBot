from utils.CommonImports import *
from utils.orm_models import User, Economy, Role, Permission


class EconomyCog(Cog, name="Economy"):
    def __init__(self, bot):
        self.bot = bot

    async def dig_values(self):
        items = random.randrange(0, 300), random.randrange(300, 500), random.randrange(500, 700), random.randrange(700,
                                                                                                                   1200)
        probabilities = [0.5, 0.35, 0.1, 0.05]
        return numpy.random.choice(items, p=probabilities)

    @commands.command(aliases=["dig"])
    @commands.guild_only()
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def Search(self, ctx):
        user = await User.find_one(User.dn_id == ctx.author.id)
        if user == None:
            await ctx.send("Please consider registering.")
        else:
            amount = await self.dig_values()
            await user.set({User.economy: Economy(wallet=user.economy.wallet + int(amount), bank=user.economy.bank)})
            await ctx.send(f"{ctx.author.mention} Mined {amount} gold Illegally")

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def Profile(self, ctx):
        """
        View your profile
        """
        account = await User.find_one(User.dn_id == ctx.author.id)
        Embed = discord.Embed(
            title=f"Profile: {ctx.author.name}",
            description="",
            color=0x000c30
        )
        Embed.add_field(name=f"Bank Account", value=f"{account.economy.bank}")
        Embed.add_field(name=f"Wallet", value=f"{account.economy.wallet}")
        await ctx.send(embed=Embed)


def setup(bot):
    cog = EconomyCog(bot)
    bot.add_cog(cog)
