from src.utils.base_imports import *
from src.services.LogService import SpecificLog

Logger = SpecificLog(__name__)
from waifu import WaifuClient, ImageCategories


@asyncinit.asyncinit
class Actions:
    async def __init__(self, Ctx, Action, Member=None):
        self.waifu = WaifuClient()
        self.action = Action
        self.context = Ctx
        self.User = Ctx.author
        self.Member = Member
        self.Embeded = None
        await self.send()

    async def get_thumbnail(self):
        return self.waifu.sfw(self.action)

    async def add_thumbnail(self, Embed: discord.Embed):
        Embed.set_image(url=await self.get_thumbnail())

    async def create_embed(self, Embed: discord.Embed = None):
        string = self.string_get()
        Embed = discord.Embed(
            title=f"{string}",
            description="",
            color=0x000c30,
        )
        await self.add_thumbnail(Embed)
        return Embed

    async def send(self):
        self.Embeded = await self.create_embed()

    def string_get(self):
        _ = self.action.lower()
        Aname = self.User.name
        Mname = self.Member
        word = None
        if _ == "bully":
            word = f"{Aname} bullies {Mname.name}"
        elif _ == "cuddle":
            word = f"{Aname} cuddles {Mname.name}"
        elif _ == "cry":
            if Mname != "None":
                word = f"{Aname} is crying because of {Mname.name}"
            else:
                word = f"{Aname} is crying"
        elif _ == "hug":
            word = f"{Aname} hugs {Mname.name}"
        elif _ == "kiss":
            word = f"{Aname} is kissing {Mname.name}"
        elif _ == "lick":
            if Mname != "None":
                word = f"{Aname} licks {Mname.name}"
            else:
                word = f"{Aname} cleans them self"
        elif _ == "pat":
            word = f"{Aname} pats {Mname.name}"
        elif _ == "smug":
            if Mname != "None":
                word = f"{Aname} is moody at {Mname.name}"
            else:
                word = f"{Aname} is acting smug"
        elif _ == "bonk":
            word = f"{Aname} bonks {Mname.name}"
        elif _ == "yeet":
            word = f"{Aname} yeets {Mname.name}"
        elif _ == "blush":
            if Mname != "None":
                word = f"{Aname} is blushing at {Mname.name}"
            else:
                word = f"{Aname} is blushing"
        elif _ == "smile":
            if Mname != "None":
                word = f"{Aname} is grining at {Mname.name}"
            else:
                word = f"{Aname} is smiling"
        elif _ == "wave":
            word = f"{Aname} waves at {Mname.name}"
        elif _ == "highdive":
            word = f"{Aname} highfives {Mname.name}"
        elif _ == "handhold":
            word = f"{Aname} holds {Mname.name}'s hand"
        elif _ == "nom":
            if Mname != "None":
                word = f"{Aname} noms on {Mname.name}"
            else:
                word = f"{Aname} is eating something"
        elif _ == "bite":
            word = f"{Aname} bites {Mname.name}"
        elif _ == "slap":
            word = f"{Aname} slaps {Mname.name}"
        elif _ == "Kill":
            word = f"{Aname} kills {Mname.name}"
        elif _ == "kick":
            word = f"{Aname} kicks {Mname.name}"
        elif _ == "happy":
            if Mname != "None":
                word = f"{Aname} is happy for {Mname.name}"
            else:
                word = f"{Aname} is happy"
        elif _ == "wink":
            word = f"{Aname} winks at {Mname.name}"
        elif _ == "poke":
            word = f"{Aname} pokes at {Mname.name}"
        elif _ == "dance":
            if Mname != "None":
                word = f"{Aname} dances with {Mname.name}"
            else:
                word = f"{Aname} is dancing"
        elif _ == "cringe":
            if Mname != "None":
                word = f"{Aname} cringes at {Mname.name}"
            else:
                word = f"{Aname} is cringing at something"
        return word
