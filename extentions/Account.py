from utils.CommonImports import *
from utils.DiscordImports import *
from utils.OrmModels import User, Economy, Role, Permission, Account as StaffAccount, Work, Occupation


class Account(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def staff_perms(user_level: str):
        async def predicate(ctx: bridge.BridgeExtContext):
            pass

        return commands.check(predicate)

    @commands.command()
    @commands.dm_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def register(self, ctx, email: str, psw: str):
        """
        Created an Account for yourself

        :parameter email: Enter your email
        :parameter psw: Enter a password
        """
        account = await User.find_one(User.dn_id == str(ctx.author.id))
        if (account):
            await ctx.send(f"Account already Exists")
        else:
            user = User(dn_id=str(ctx.author.id), email=email, password=hashlib.sha256(psw.encode('utf-8')).hexdigest(),
                        economy=Economy(Wallet=0, BankAccount=0))
            await user.insert()
            await ctx.send(f"Account Created using {email}")

    @commands.command()
    @commands.dm_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def login(self, ctx, email: str, psw: str):
        """
        Login to an Account

        :parameter email: Enter your email
        :parameter psw: Enter a password
        """
        account = await User.find_one(User.email == email)
        if (account):
            if (account.password == hashlib.sha256(psw.encode('utf-8')).hexdigest()):
                account.dn_id = str(ctx.author.id)
                await account.update()
                await ctx.send("Account moved to this discord account.")
            else:
                await ctx.send("What are you doing.")
        else:
            await ctx.send("Please register first.")

    @commands.command()
    @commands.is_owner()
    async def CreateRole(self, ctx, name: str):
        selected_role = await Role.find_one(Role.name == name)
        if (selected_role):
            await ctx.send(f"Role does exist already.")
        else:
            await Role(name=name).insert()
            await ctx.send(f"Role '{name}' Created")

    @commands.command()
    @commands.is_owner()
    async def AssignRole(self, ctx, member: discord.Member, name: str):
        selected_role = await Role.find_one(Role.name == name)
        if not selected_role:
            await ctx.send(f"Role does not exist.")
        account = await StaffAccount.find_one(StaffAccount.dn_id == str(member.id))
        if (account):
            account.role = selected_role
            account.update()
        else:
            await StaffAccount(dn_id=str(member.id), role=selected_role).insert()
        await ctx.send(f"Role has been updated for {member.name}")

    @commands.command()
    @commands.is_owner()
    async def RemoveRole(self, ctx, member: discord.Member):
        account = await StaffAccount.find_one(StaffAccount.dn_id == str(member.id))
        if (account == None):
            await ctx.send(f"{member.mention} has no staff account.")
        else:
            await account.delete()
            await ctx.send(f"{member.mention} has staff account removed.")

    @commands.command()
    @commands.is_owner()
    async def CreateJob(self, ctx, lvl: float, nameJ: str, daily: float, exp:float):
        fromJob = await Work.find_one(Work.name == nameJ)
        if fromJob:
            return await ctx.send("That Job name already exists.")
        fromJob = await Work.find_one(Work.level == lvl)
        if fromJob:
            return await ctx.send("That Job level already exists.")
        work = Work(level=lvl, name=nameJ, daily_rate=daily, daily_exp=exp)
        await work.save()
        await ctx.send("That Job has been created.")


def setup(bot):
    cog = Account(bot)
    bot.add_cog(cog)
