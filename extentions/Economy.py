from utils.CommonImports import *
from utils.DiscordImports import *
from utils.OrmModels import User, Economy, Role, Permission, Account, Work, Occupation


JsonConfig = None
with open(os.getcwd() + "/configs/" + "EconomyConfig.json", "r") as file:
    JsonConfig = json.load(file)


class EconomyCog(Cog, name="Economy"):
    JobsAvailable = ["1","2"]
    def __init__(self, bot : AutoShardedBot):
        self.bot = bot


    def UserBanned(_: any = None):
        async def predicate(ctx: bridge.BridgeExtContext):
            user = await Account.find_one(Account.dn_id == str(ctx.author.id), fetch_links=True)
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
            random.randrange(500, 1000),
            random.randrange(1000, 3800)
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
    @commands.cooldown(1, 80, commands.BucketType.user)
    async def search(self, ctx):
        user = await User.find_one(User.dn_id == str(ctx.author.id))
        if user == None:
            raise UserNotRegistered()
        else:
            amount = await self.dig_values()
            user.economy.wallet = user.economy.wallet + int(amount)
            await user.save()
            await ctx.send(f"{ctx.author.mention} Mined {amount} gold Illegally")

    @commands.command()
    @UserBanned()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def profile(self, ctx, member: discord.Member = None):
        """
        View your profile
        """
        if (member):
            account = await User.find_one(User.dn_id == str(member.id))
            staffAccount = await Account.find_one(Account.dn_id == str(member.id), fetch_links=True)
        else:
            account = await User.find_one(User.dn_id == str(ctx.author.id))
            staffAccount = await Account.find_one(Account.dn_id == str(ctx.author.id), fetch_links=True)
        if account == None:
            raise UserNotRegistered(member)
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
        fromUser = await User.find_one(User.dn_id == str(ctx.author.id))
        toUser = await User.find_one(User.dn_id == str(Member.id))
        if fromUser == None:
            raise UserNotRegistered()
        elif toUser == None:
            raise UserNotRegistered(Member)
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
        """Deposit money into the bank (must be 5000 or more)
        """
        fromUser = await User.find_one(User.dn_id == str(ctx.author.id))
        if fromUser == None:
            raise UserNotRegistered()
        else:
            if (amount > fromUser.economy.wallet):
                await ctx.send("Please consider withdrawing from the bank or earning more money for doing activities.")
            elif (amount <= fromUser.economy.wallet and amount >= 5000):
                wallet = fromUser.economy.wallet - amount
                bank = fromUser.economy.bank + amount
                await fromUser.set({User.economy: Economy(wallet=wallet, bank=bank)})
                await ctx.send(f"{ctx.author.mention} deposited {amount} money into their account")

    @commands.command(aliases=["tax"])
    @UserBanned()
    async def Register4Tax(self, ctx):
        """Register for tax
        """
        fromUser = await User.find_one(User.dn_id == str(ctx.author.id))
        if fromUser == None:
            raise UserNotRegistered()
        elif fromUser.occupation:
            raise UserRegisteredForTax()
        else:
            occupation = Occupation(level=0,exp=0,last_work_day="", work= await Work.find_one(Work.level == 0))
            await occupation.save()
            fromUser.occupation = occupation;
            await fromUser.save()
            await ctx.send("Registered for tax.")

    @bridge.bridge_command(description=JsonConfig["intern-jobs-des"])
    @discord.option(name="internship", choices=JsonConfig["intern-jobs"])
    async def internship(self, ctx:bridge.BridgeContext, *, internship:str="None"):
        fromUser = await User.find_one(User.dn_id == str(ctx.author.id))
        if fromUser == None:
            raise UserNotRegistered()
        elif fromUser.occupation == None:
            raise UserNotRegisteredForTax()
        if isinstance(ctx, bridge.BridgeExtContext):
            await ctx.send("hello world")
        elif isinstance(ctx, bridge.BridgeApplicationContext):
            await ctx.respond("hello world")



def setup(bot):
    cog = EconomyCog(bot)
    bot.add_cog(cog)
