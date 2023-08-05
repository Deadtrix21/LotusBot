import discord

from utils.CommonImports import *
from utils.orm_models import User, Economy, Role, Permission, Account


class EconomyCog(Cog, name="Economy"):
    def __init__(self, bot):
        self.bot = bot


    def UserBanned(_ : any = None):
        async def predicate(ctx: bridge.BridgeExtContext):
            user = await Account.find_one(Account.dn_id == ctx.author.id, fetch_links=True)
            if (user):
                role: Role = user.role
                if (role.name == "BannedAccount"):
                    return False
                else:
                    return True
            else:
                return True
        return commands.check(predicate)

    async def dig_values(self):
        items = (
            random.randrange(0, 300),
            random.randrange(300, 500),
            random.randrange(500, 700),
            random.randrange(700, 2200)
        )
        probabilities = [
            0.60,
            0.25,
            0.14,
            0.01
        ]
        return float(numpy.random.choice(items, p=probabilities))

    @commands.command(aliases=["dig"])
    @UserBanned()
    @commands.guild_only()
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def search(self, ctx):
        user = await User.find_one(User.dn_id == ctx.author.id)
        if user == None:
            await ctx.send("Please consider registering.")
        else:
            amount = await self.dig_values()
            await user.set({User.economy: Economy(wallet=user.economy.wallet + int(amount), bank=user.economy.bank)})
            await ctx.send(f"{ctx.author.mention} Mined {amount} gold Illegally")

    @commands.command()
    @UserBanned()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def profile(self, ctx, member: discord.Member = None):
        """
        View your profile
        """
        if (member):
            account = await User.find_one(User.dn_id == member.id)
            staffAccount = await Account.find_one(Account.dn_id == member.id, fetch_links=True)
        else:
            account = await User.find_one(User.dn_id == ctx.author.id)
            staffAccount = await Account.find_one(Account.dn_id == ctx.author.id, fetch_links=True)
        if account == None:
            if (member == None):
                await ctx.send("Please consider asking the person to register.")
            else:
                await ctx.send("Please consider registering.")
        else:
            Embed = discord.Embed(
                title=f"Profile: {ctx.author.name if member == None else member.name}",
                description="",
                color=0x000c30
            )
            if (staffAccount):
                Embed.add_field(name=f"Staff Role", value=f"{staffAccount.role.name}", inline=False)
            if (account):
                Embed.add_field(name=f"Bank Account", value=f"{account.economy.bank}", inline=False)
                Embed.add_field(name=f"Wallet", value=f"{account.economy.wallet}", inline=False)
            await ctx.send(embed=Embed)

    @commands.command(aliases=["give"])
    @UserBanned()
    @commands.cooldown(1, 25, commands.BucketType.user)
    async def pay(self, ctx, value: int, Member: discord.Member):
        """ Pay or Give people money
        """
        fromUser = await User.find_one(User.dn_id == ctx.author.id)
        toUser = await User.find_one(User.dn_id == Member.id)
        if fromUser == None:
            await ctx.send("Please consider registering.")
        elif toUser == None:
            await ctx.send("The user your trying to pay, is not registered.")
        else:
            if (value > fromUser.economy.wallet):
                await ctx.send("Please consider withdrawing from the bank or earning more money for doing activities.")
            elif (value <= fromUser.economy.wallet):
                wallet = fromUser.economy.wallet - value
                await fromUser.set({User.economy: Economy(wallet=wallet, bank=fromUser.economy.bank)})
                await toUser.set(
                    {User.economy: Economy(wallet=toUser.economy.wallet + value, bank=toUser.economy.bank)})
                await ctx.send(f"{ctx.author.mention} payed {value} to {Member.mention}")

    @commands.command(aliases=["dep"])
    @UserBanned()
    @commands.cooldown(1, 120, commands.BucketType.user)
    async def deposit(self, ctx, amount: int):
        """Deposit money into the bank
        """
        fromUser = await User.find_one(User.dn_id == ctx.author.id)
        if fromUser == None:
            await ctx.send("Please consider registering.")
        else:
            if (amount > fromUser.economy.wallet):
                await ctx.send("Please consider withdrawing from the bank or earning more money for doing activities.")
            elif (amount <= fromUser.economy.wallet and amount >= 5000):
                wallet = fromUser.economy.wallet - amount
                bank = fromUser.economy.bank + amount
                await fromUser.set({User.economy: Economy(wallet=wallet, bank=bank)})
                await ctx.send(f"{ctx.author.mention} deposited {amount} money into their account")


def setup(bot):
    cog = EconomyCog(bot)
    bot.add_cog(cog)
