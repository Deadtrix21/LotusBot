

from utils.DiscordImports import *
from humanfriendly import parse_size, parse_timespan, parse_date, parse_path, parse_length
from humanfriendly import format_path, format_size, format_timespan, format_length, format_number


class HumanMetrics(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bridge.bridge_command(name='storage-size')
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def ss(self, ctx, size):
        """
        Turn a values into it's representation of storage
        Example: 16GB
        Result: 14.9Gb
        """
        bytesSize =  parse_size(size)
        Embed = discord.Embed(
            title=f"Metrics: {size}",
            description="",
            color=0x000c30
        )
        Embed.add_field(name=f"Binary", value=f"{format_size(bytesSize, binary=True)}", inline=True)
        Embed.add_field(name=f"Decimal", value=f"{format_size(bytesSize)}", inline=True)
        await ctx.send(embed = Embed)

    @bridge.bridge_command(name="value-to-size")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def vtsts(self, ctx, size:int):
        """
        Turn a number into b|kb|mb|gb|tb
        """
        Embed = discord.Embed(
            title=f"Metrics: {size}",
            description="",
            color=0x000c30
        )
        Embed.add_field(name=f"Representation", value=f"{format_size(size)}", inline=True)
        await ctx.send(embed = Embed)

    @bridge.bridge_command(name="value-to-length")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def vtl(self, ctx, *, size):
        """
        Takes a number and converts it to lengths
        """
        Embed = discord.Embed(
            title=f"Metrics: {size}",
            description="",
            color=0x000c30
        )
        Embed.add_field(name=f"Representation", value=f"{format_length(parse_length(size))}", inline=True)
        await ctx.send(embed = Embed)

def setup(bot):
    cog = (HumanMetrics(bot))
    bot.add_cog(cog)
