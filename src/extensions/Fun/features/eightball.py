import numpy.random
from src.utils.base_imports import *
from src.services.LogService import SpecificLog

Logger = SpecificLog(__name__)

@asyncinit.asyncinit
class EightBall:
    options = [
        "It is Certain.",
        "Without a doubt.",
        "As i see it, yes.",
        "Ask again later.",
        "Can't check the cosmos now, try again.",
        "Don't count on it.",
        "My sources say no.",
        "Outlook not so good.",
        "Maybe.",
        "Unsure.",
        "Yes.",
        "Better not tell you now.",
        "Cannot predict now.",
        "Very doubtful."]

    async def __init__(self, bot, ctx, asked):
        self.bot = bot
        self.context = ctx
        self.asked = asked
        await self.send()

    async def __add_question(self, Embed: discord.Embed):
        Embed.add_field(
            inline=False,
            name="Question:",
            value=f"{self.asked}"
        )
        return None

    async def __add_8ball(self, Embed: discord.Embed):
        word = numpy.random.choice(self.options)
        Embed.add_field(
            inline=False,
            name="Prediction:",
            value=f"{word}"
        )
        return None


    async def __build_embed(self, Embed=None):
        Embed = discord.Embed(
            title="8-Ball",
            description="",
            color=0x000c30
        )
        await self.__add_question(Embed)
        await self.__add_8ball(Embed)
        return Embed


    async def send(self):
        self.Embedded = await self.__build_embed()
