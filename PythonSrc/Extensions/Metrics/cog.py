from PythonSrc.Utilities.Imports import System, Database, Discord
from PythonSrc.Utilities import Logger


class HumanMetrics(Discord.Cog):
    def __init__(self, bot):
        self.bot = bot

    @Discord.bridge.bridge_command(name='storage-size')
    @Discord.commands.cooldown(1, 10, Discord.commands.BucketType.user)
    async def ss(self, ctx, size):
        """
        Turn a values into it's representation of storage
        Example: 16GB
        Result: 14.9Gb
        """
        bytesSize = System.humanfriendly.parse_size(size)
        Embed = Discord.discord.Embed(
            title=f"Metrics: {size}",
            description="",
            color=0x000c30
        )
        Embed.add_field(name=f"Binary", value=f"{System.humanfriendly.format_size(bytesSize, binary=True)}",
                        inline=True)
        Embed.add_field(name=f"Decimal", value=f"{System.humanfriendly.format_size(bytesSize)}", inline=True)
        await ctx.send(embed=Embed)

    @Discord.bridge.bridge_command(name="value-to-size")
    @Discord.commands.cooldown(1, 10, Discord.commands.BucketType.user)
    async def vtsts(self, ctx, size: int):
        """
        Turn a number into b|kb|mb|gb|tb
        """
        Embed = Discord.discord.Embed(
            title=f"Metrics: {size}",
            description="",
            color=0x000c30
        )
        Embed.add_field(name=f"Representation", value=f"{System.humanfriendly.format_size(size)}", inline=True)
        await ctx.send(embed=Embed)

    @Discord.bridge.bridge_command(name="value-to-length")
    @Discord.commands.cooldown(1, 10, Discord.commands.BucketType.user)
    async def vtl(self, ctx, *, size):
        """
        Takes a number and converts it to lengths
        """
        Embed = Discord.discord.Embed(
            title=f"Metrics: {size}",
            description="",
            color=0x000c30
        )
        Embed.add_field(name=f"Representation",
                        value=f"{System.humanfriendly.format_length(System.humanfriendly.parse_length(size))}",
                        inline=True)
        await ctx.send(embed=Embed)


def setup(bot):
    cog = (HumanMetrics(bot))
    bot.add_cog(cog)
