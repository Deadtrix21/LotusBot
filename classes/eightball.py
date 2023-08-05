import discord, os, random
from asyncinit import asyncinit

@asyncinit
class EightBall:
    
    async def __init__(self, bot, ctx, asked):
        self.bot = bot
        self.context = ctx
        self.asked = asked
        self.Args = {}
        await self.__autogen()
        await self.send()
        
    async def __autogen(self, Args=None):
        for i in range(14):
            self.Args[i] = getattr(EightBall, f'_{i}')(self)
            
    def _0 (self):
        return "It is Certain"
    def _1 (self):
        return "Without a doubt"
    def _2 (self):
        return "As i see it, yes"
    def _3 (self):
        return "Ask again later"
    def _4 (self):
        return "Reply hazy, try again"
    def _5 (self):
        return "Don't count on it"
    def _6 (self):
        return "My sources say no"
    def _7 (self):
        return "Outlook not so good"
    def _8 (self):
        return "Maybe"
    def _9 (self):
        return "Unsure"
    def _10(self):
        return "Yes"
    def _11(self):
        return "Better not tell you now"
    def _12(self):
        return "Cannot predict now"
    def _13(self):
        return "Very doubtful."
    
    async def __get_prediction(self):
        num = random.randint(0, 13)
        return self.Args[num]
    
    async def __add_question(self, Embed:discord.Embed):
        Embed.add_field(
            inline  = False,
            name    = "Question:",
            value   = f"{self.asked}"
            )
        return None
    
    async def __add_8ball(self, Embed:discord.Embed):
        Embed.add_field(
            inline  = False,
            name    = "Prediction:",
            value   = f"{await self.__get_prediction()}"
            )
        return None
    
    async def __build_embed(self, Embed=None):
        Embed = discord.Embed(
            title= "8-Ball",
            description="",
            color= 0x000c30
        )
        await self.__add_question(Embed)
        await self.__add_8ball(Embed)
        return Embed
    
    async def send(self):
        self.Embedded = await self.__build_embed()