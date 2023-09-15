from src.utils.base_imports import *
from src.services.LogService import SpecificLog

Logger = SpecificLog(__name__)


class HumanMetrics(Extension):
    def __init__(self, bot):
        self.bot = bot

    @bridge_command(name='storage-size')
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def ss(self, ctx, size):
        """
        Turn a values into it's representation of storage
        Example: 16GB
        Result: 14.9Gb
        """
        bytesSize = humanfriendly.parse_size(size)
        Embed = DiscordEmbed(
            title=f"Metrics: {size}",
            description="",
            color=0x000c30
        )
        Embed.add_field(name=f"Binary", value=f"{humanfriendly.format_size(bytesSize, binary=True)}",
                        inline=True)
        Embed.add_field(name=f"Decimal", value=f"{humanfriendly.format_size(bytesSize)}", inline=True)
        await ctx.send(embed=Embed)

    @bridge_command(name="value-to-size")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def vtsts(self, ctx, size: int):
        """
        Turn a number into b|kb|mb|gb|tb
        """
        Embed = DiscordEmbed(
            title=f"Metrics: {size}",
            description="",
            color=0x000c30
        )
        Embed.add_field(name=f"Representation", value=f"{humanfriendly.format_size(size)}", inline=True)
        await ctx.send(embed=Embed)

    @bridge_command(name="value-to-length")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def vtl(self, ctx, *, size):
        """
        Takes a number and converts it to lengths
        """
        Embed = DiscordEmbed(
            title=f"Metrics: {size}",
            description="",
            color=0x000c30
        )
        Embed.add_field(name=f"Representation",
                        value=f"{humanfriendly.format_length(humanfriendly.parse_length(size))}",
                        inline=True)
        await ctx.send(embed=Embed)


def setup(bot):
    cog = (HumanMetrics(bot))
    bot.add_cog(cog)
