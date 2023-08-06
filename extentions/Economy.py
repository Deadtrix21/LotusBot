from utils.CommonImports import *
from utils.DiscordImports import *
from utils.OrmModels import User, Economy, Role, Permission, Account, Work, Occupation

JsonConfig = None
with open(os.getcwd() + "/configs/" + "EconomyConfig.json", "r") as file:
    JsonConfig = json.load(file)


class EconomyCog(Cog, name="Economy"):
    JobsAvailable = ["1", "2"]

    def __init__(self, bot: AutoShardedBot):
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

    async def level_check(self, level):
        # deadtrix's fuck you over system
        partzero = 0.08 * (level ** 3)
        partone = 0.4 * (level ** 3)
        parttwo = 0.8 * (level ** 2)
        partthree = 9 * (level ** 1)
        final = round(partzero + partone + parttwo + partthree, None)
        return float(final)

    async def handleExp(self, ctx, fromUser: User):
        embed = None
        work = fromUser.occupation.work
        exp = work.daily_exp
        rate = work.daily_rate
        fromUser.economy.wallet += rate
        cap = await self.level_check(fromUser.occupation.level)
        fromUser.occupation.exp += exp
        if cap <= fromUser.occupation.exp:
            fromUser.occupation.exp = fromUser.occupation.exp - cap
            fromUser.occupation.level += 1
            embed = discord.Embed(
                title=f"Level up",
                description="",
                color=0x000c30
            )
        await fromUser.occupation.save()
        return embed

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
            account = await User.find_one(User.dn_id == str(member.id), fetch_links=True)
            staffAccount = await Account.find_one(Account.dn_id == str(member.id), fetch_links=True)
        else:
            account = await User.find_one(User.dn_id == str(ctx.author.id), fetch_links=True)
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
                if account.occupation:
                    Embed.add_field(name=f"Account Level", value=f"{account.occupation.level}", inline=True)
                    Embed.add_field(name=f"Account Exp", value=f"{account.occupation.exp}", inline=True)
                    Embed.add_field(name=f"Exp Needed", value=f"{await self.level_check(account.occupation.level)}",
                                    inline=True)
                    Embed.add_field(name=f"Net Worth:", value=f" ", inline=False)
                Embed.add_field(name=f"Bank Account", value=f"{account.economy.bank}", inline=True)
                Embed.add_field(name=f"Wallet", value=f"{account.economy.wallet}", inline=True)
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
            occupation = Occupation(level=0, exp=0, last_work_day="")
            await occupation.save()
            fromUser.occupation = occupation;
            await fromUser.save()
            await ctx.send("Registered for tax.")

    @bridge.bridge_command(description=JsonConfig["intern-jobs-des"])
    @UserBanned()
    @discord.option(name="internship", choices=JsonConfig["intern-jobs"])
    async def internship(self, ctx: bridge.BridgeContext, *, internship: str = "None"):
        fromUser = await User.find_one(User.dn_id == str(ctx.author.id))
        if fromUser == None:
            raise UserNotRegistered()
        elif fromUser.occupation == None:
            raise UserNotRegisteredForTax()
        work = await Work.find_one(Work.name == internship)
        if isinstance(ctx, bridge.BridgeExtContext):
            fromUser.occupation.work = work
            await fromUser.save()
            await ctx.send(f"{ctx.author.mention} you have applied and been accepted as an {internship}")
        elif isinstance(ctx, bridge.BridgeApplicationContext):
            fromUser.occupation.work = work
            await fromUser.save()
            await ctx.respond(f"{ctx.author.mention} you have applied and been accepted as an {internship}")

    @bridge.bridge_command()
    @UserBanned()
    @commands.cooldown(1, 7200, commands.BucketType.user)
    async def work(self, ctx: bridge.BridgeContext, ):
        fromUser = await User.find_one(User.dn_id == str(ctx.author.id), fetch_links=True)
        if fromUser == None:
            raise UserNotRegistered()
        elif fromUser.occupation == None:
            raise UserNotRegisteredForTax()
        emb = await self.handleExp(ctx, fromUser)
        await fromUser.save()
        if isinstance(ctx, bridge.BridgeExtContext):
            await ctx.send(
                f"{ctx.author.mention} you have earned {fromUser.occupation.work.daily_rate} gold for today.",
                embed=emb)
        elif isinstance(ctx, bridge.BridgeApplicationContext):
            await ctx.respond(
                f"{ctx.author.mention} you have earned {fromUser.occupation.work.daily_rate} gold for today.",
                embed=emb)


def setup(bot):
    cog = EconomyCog(bot)
    bot.add_cog(cog)


