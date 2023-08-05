from utils.CommonImports import *
from utils.orm_models import User, Economy, Role, Permission, Account as StaffAccount

class Account(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.dm_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def Register(self, ctx, email: str, psw: str):
        """
        Created an Account for yourself

        :parameter email: Enter your email
        :parameter psw: Enter a password
        """
        account = await User.find_one(User.dn_id == ctx.author.id)
        if (account):
            await ctx.send(f"Account already Exists")
        else:
            user = User(dn_id=ctx.author.id, email=email, password=hashlib.sha256(psw.encode('utf-8')).hexdigest(),
                        economy=Economy(Wallet=0, BankAccount=0))
            await user.insert()
            await ctx.send(f"Account Created using {email}")

    @commands.command()
    @commands.dm_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def Login(self, ctx, email: str, psw: str):
        """
        Login to an Account

        :parameter email: Enter your email
        :parameter psw: Enter a password
        """
        account = await User.find_one(User.email == email)
        if (account):
            if (account.password == hashlib.sha256(psw.encode('utf-8')).hexdigest()):
                account.dn_id = ctx.author.id
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
        account = await StaffAccount.find_one(StaffAccount.dn_id == member.id)
        if (account):
            account.role = selected_role
            account.update()
        else:
            await StaffAccount(dn_id=member.id,role=selected_role).insert()
        await ctx.send(f"Role has been updated for {member.name}")


def setup(bot):
    cog = Account(bot)
    bot.add_cog(cog)
