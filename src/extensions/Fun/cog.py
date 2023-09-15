from src.utils.base_imports import *
from src.services.LogService import SpecificLog

from .features import eightball, Actions
from .features.UnoGame import Game

Logger = SpecificLog(__name__)
Action_List = [
    'bully', 'cuddle', 'cry', 'hug',
    'kiss', 'lick', 'pat', 'smug', 'bonk',
    'yeet', 'blush', 'smile', 'wave', 'highfive',
    'handhold', 'nom', 'bite', 'slap',
    'kill', 'kick', 'happy', 'wink', 'poke', 'dance', 'cringe'
]


class Fun(Extension):
    def __init__(self, bot):
        self.bot = bot
        self.action_help = self.set_actions_cmd_help()
        self.games: "dict[int, Game.Game]" = {}
        self.users: "dict[int, int]" = {}

    def set_actions_cmd_help(self):
        msg = "```\nCommand Options:"
        for i in Action_List:
            msg += f"\n     {i}"
        msg += "```"
        return msg

    @bridge_command(name="8ball")
    @commands.guild_only()
    async def EightBall(self, ctx, *, asked):
        """Magic 8 ball

        Args:
            asked ([string]): the question
        """
        embeds = await eightball.EightBall(self.bot, ctx, asked)
        if isinstance(ctx, BridgeExtContext):
            await ctx.reply(embed=embeds.Embedded)
        elif isinstance(ctx, BridgeApplicationContext):
            await ctx.respond(embed=embeds.Embedded)

    @bridge_command()
    @discord.option(name="action", choices=Action_List)
    async def do(self, ctx: BridgeContext, action: str = "None", member: DiscordMember = None):
        """Anime Emotions: Actions required, Member sometimes
        """
        if isinstance(ctx, BridgeExtContext):
            if action == "None":
                await ctx.reply(self.action_help)
            elif action not in Action_List:
                await ctx.reply(self.action_help)
            else:
                Embed = await Actions.Actions(ctx, action, member)
                await ctx.send(embed=Embed.Embeded)
                try:
                    pass
                except Exception as E:
                    print(E)
                    await ctx.reply("that command needs a member mentioned", delete_after=10)
        elif isinstance(ctx, BridgeApplicationContext):
            try:
                Embed = await Actions.Actions(ctx, action, member)
                await ctx.respond(embed=Embed.Embeded)
            except Exception as E:
                print(E)
                await ctx.reply("that command needs a member mentioned", delete_after=10)
        if member != None:
            await ctx.send(member.mention)

    def getActors(self, bot, killer, target):
        return {'id': bot.id, 'nick': bot.display_name, 'formatted': bot.mention}, {'id': killer.id,
                                                                                    'nick': killer.display_name,
                                                                                    'formatted': "<@{}>".format(
                                                                                        killer.id)}, {'id': target.id,
                                                                                                      'nick': target.display_name,
                                                                                                      'formatted': target.mention}

    @commands.command()
    async def slap(self, ctx, *, user: discord.Member):
        """Open hand, not a closed fist!"""

        bot, killer, target = self.getActors(
            ctx.bot.user, ctx.message.author, user)

        diceroll = random.randint(0, 100)

        if target['id'] == bot['id']:  # tryng to slap the bot, eh?

            message1 = "{} looks at {}... ✋😏 🤖".format(
                killer['nick'], bot['nick'])
            message2 = "but {} suddenly slaps {} with his silver sword! 😵💫 🍆🤖".format(
                bot['nick'], killer['nick'])

        elif killer['id'] == target['id']:  # wants to slap themselves

            message1 = "{} looks themselves in the mirror... 🖼😐".format(
                killer['nick'])

            if diceroll > 89:
                message2 = "and smashes their head against it! ✨🖼💥😫"

            elif diceroll > 10:
                message2 = "and gently pats their cheeks to wake up! 🖼😊"

            else:
                message2 = "and trips on the wet floor! Ouch! 🤕"

        else:  # wants to slap another user

            message1 = "{} raises their hand... ✋😏".format(killer['nick'])

            if diceroll > 89:
                message2 = "and mutilates {}! Oh my god, there's blood everywhere! 😵💥🤛😡".format(
                    target['formatted'])

            elif diceroll > 50 and diceroll < 55:
                message2 = "and gives {} a romantic spanking 😊🍑 👋😍".format(
                    target['formatted'])

            elif diceroll > 10:
                message2 = "and slaps {} senseless! 😫💫👋😠".format(
                    target['formatted'])

            else:
                message2 = "and misses! So stupid! 👋😟💨 😛"

        await ctx.send(message1)
        time.sleep(1)
        await ctx.send(message2)

    @commands.command()
    async def punch(self, ctx, *, user: discord.Member):
        """Open up a can of whoop-ass on a user!"""

        bot, killer, target = self.getActors(
            ctx.bot.user, ctx.message.author, user)

        diceroll = random.randint(0, 100)

        if target['id'] == bot['id']:  # tryng to punch the bot, eh?

            message1 = "{} waves their fists at {}... 🤖 ✊🧐".format(
                killer['nick'], bot['nick'])
            message2 = "but {} casts Igni on {}! 🤖 🔥😫🔥".format(
                bot['nick'], killer['formatted'])

        elif killer['id'] == target['id']:  # wants to punch themselves

            message1 = "{} looks at their own fist... 😒✊".format(
                killer['nick'])

            if diceroll > 89:
                message2 = "and bashes their head through the nearest wall! 😫▮💥"
            elif diceroll > 69:
                message2 = "and bashes their head against it until its broken! 😡💫🤟"
            elif diceroll > 10:
                message2 = "and repeatedly hits themselves with their pathetic little hands 🤜😣🤛"
            else:
                message2 = "tries to throw a punch, but misses and breaks their ankle! ☹️🦵"

        else:  # wants to punch another user

            message1 = "{} raises their fists towards {}... 😧 ✊😠".format(
                killer['formatted'], target['formatted'])

            if diceroll > 89:
                message2 = "\"Omae wa mou shindeiru\", says {}, before {} explodes into a cloud of blood and guts. 💥🤯💥 👈😎".format(
                    killer['formatted'], target['formatted'])

            elif diceroll > 59:
                message2 = "and a flurry of punches break every bone in {}'s body! Ora! Ora! Ora! Ora! 😣🤛🤛🤛 😡".format(
                    target['formatted'])
            elif diceroll > 10:
                message2 = "and punches {} right in the face! Hard! 😣🤛 😠".format(
                    target['formatted'])
            else:
                message2 = "and trips on a banana peel! Doofus! 🤣👉 😖🍌"

        await ctx.send(message1)
        time.sleep(1)
        await ctx.send(message2)

    @commands.command()
    async def stab(self, ctx, *, user: discord.Member):
        """Turn a user into shish kebab!"""

        bot, killer, target = self.getActors(
            ctx.bot.user, ctx.message.author, user)

        diceroll = random.randint(0, 100)

        if target['id'] == bot['id']:  # tryng to shoot the bot, eh?

            message1 = "{} raises their dagger at {}... 😠🔪 🤖".format(
                killer['nick'], bot['nick'])
            message2 = "but {} teleports behind {} and strikes! 😵💫 ⚔️🤖 {}".format(
                bot['nick'], killer['formatted'], '`"Nothing personell, kid"`')

        elif killer['id'] == target['id']:  # wants to slap themselves

            message1 = "{} holds a knife against their abdomen...".format(
                killer['nick'])

            if diceroll > 89:
                message2 = "and cuts their own head off! How is that even possible!? 🙃👕"
            elif diceroll > 10:
                message2 = "and commits sudoku! 🔪😵"
            else:
                message2 = "and accidentally cuts their finger on a hentai magazine! 📕😫 {}-no skebe!".format(
                    target['nick'])

        else:  # wants to slap another user

            message1 = "{} raises their dagger... 😏🔪 😶".format(killer['nick'])

            if diceroll > 89:
                message2 = "and turns {} into a sheesh kebab! RIP in pieces! 😡🔪 👣 😵 🤚 👕 👖 ✋".format(
                    target['formatted'])
            elif diceroll > 10:
                message2 = "and stabs {}! Yikes! 😠🔪💥 ✋😵🤚".format(
                    target['formatted'])
            elif diceroll > 5:
                message2 = "but {} dodges like a ninja! 😛💨 😟🔪".format(
                    target['formatted'])
            else:
                message2 = "and cuts his own hand off! What an amateur! 😟🔪🤚 😝"

        await ctx.send(message1)
        time.sleep(1)
        await ctx.send(message2)

    @commands.command()
    async def shoot(self, ctx, *, user: discord.Member):
        """Shoot another user (or yourself) dead!"""

        bot, killer, target = self.getActors(
            ctx.bot.user, ctx.message.author, user)

        diceroll = random.randint(0, 100)

        if (target['id'] == bot['id']):  # tryng to shoot the bot, eh?

            message1 = "{} aims their gun, pulls the trigger...".format(
                killer['nick'])
            message2 = "but {} shot first! 😵 💥🔫🤖".format(bot['nick'])

        elif killer['id'] == target['id']:  # wants to kill themselves

            message1 = "{} holds a gun to their head, pulls the trigger...".format(
                killer['nick'])

            if diceroll > 89:
                message2 = "and explodes! Boom! Splat! What a mess! 💥😵💥"
            elif diceroll > 30:
                message2 = "and commits sudoku! 💥😵🔫"
            elif diceroll > 20:
                message2 = "and KYSed themselves! 💥😵🔫"
            elif diceroll > 10:
                message2 = "and somehow didn't miss! At least this idiot is good for something! 💥😵🔫"
            else:
                message2 = "and misses! What an idiot! Should've aimed at the temple! 💥🔫😯"

        else:  # wants to kill other user

            message1 = "{} aims their gun, pulls the trigger...".format(
                killer['nick'])

            if diceroll > 89:
                message2 = "and {} explodes into a red, gut-ridden, eyeball-strewn paste. Fun!!! 💥🔴 🔫🤠".format(
                    target['formatted'])
            elif diceroll > 75:
                message2 = "and shoots {} in the head! Bang! 💥😵 🔫😆".format(
                    target['formatted'])
            elif diceroll > 10:
                message2 = "and shoots {} dead! 😱 💥🔫😁".format(
                    target['formatted'])
            elif diceroll > 5:
                message2 = "and misses {}! Doh! 😗 💨🔫😣".format(
                    target['formatted'])
            else:
                message2 = "and shoots themselves instead of {}! LOL! 🤣 💥😵🔫".format(
                    target['formatted'])

        await ctx.send(message1)
        time.sleep(1)
        await ctx.send(message2)

    @commands.command()
    async def love(self, ctx, *, user: discord.Member):
        """Show some affection for once!"""

        bot, killer, target = self.getActors(
            ctx.bot.user, ctx.message.author, user)

        diceroll = random.randint(0, 100)

        if target['id'] == bot['id']:  # love the bot
            message = "{} loves {} 😍 🤖".format(killer['nick'], bot['nick'])
        elif killer['id'] == target['id']:  # loves themselves
            message = "{} loves themselves, because nobody else does 😕".format(
                killer['nick'])
        else:
            if diceroll > 90:
                message = "{} and {} sitting under a tree... 💕".format(
                    killer['formatted'], target['formatted'])
            elif diceroll > 10:
                message = "{} loves {} aww... 😍 😊".format(
                    killer['formatted'], target['formatted'])
            else:
                message = "{} loves {}, but not in return 😭 😑".format(
                    killer['formatted'], target['formatted'])

        await ctx.send(message)

    @commands.command()
    async def sex(self, ctx, *, user: discord.Member):
        """Sex a user, because there's no NSFW channel!"""

        bot, killer, target = self.getActors(
            ctx.bot.user, ctx.message.author, user)

        diceroll = random.randint(0, 100)

        if target['id'] == bot['id']:  # sex the bot
            if diceroll > 89:
                message = "{} is taken by {} on top of a stuffed unicorn 😝🦄🤖".format(
                    killer['formatted'], bot['nick'])
            else:
                message = "Everbody wants to sex {}, get in line, loser!".format(
                    bot['nick'])
        elif killer['id'] == target['id']:  # sex themselves
            message = "{} does as they are told and f***s themselves 😓".format(
                killer['formatted'])
        else:
            message = "This is a Christmas Discord, get a room! 🎄"

        await ctx.send(message)

    @commands.command()
    async def succ(self, ctx, *, user: discord.Member):
        """Succ a user like a lollipop"""

        bot, killer, target = self.getActors(
            ctx.bot.user, ctx.message.author, user)

        diceroll = random.randint(0, 100)

        if target['id'] == bot['id']:  # succ the bot
            if diceroll > 89:
                message = "{} enjoys {}'s magic juice 😙🍆🤖".format(
                    killer['formatted'], bot['nick'])
            else:
                message = "You already succ CDPR's dick every day!"
        elif killer['id'] == target['id']:  # succ themselves
            message = "{} succs themselves. Impressive, I guess...".format(
                killer['formatted'])
        else:
            if diceroll > 80:
                message = "Sucks to be you, {}".format(killer['formatted'])
            else:
                message = "This is a Christmas Discord, get a room! 🎄"

        await ctx.send(message)

    @commands.Cog.listener()
    async def on_message(self, msg: discord.Message) -> None:
        """Handle the game process over DMs."""
        author = msg.author
        if (author == self.bot.user or
                not isinstance(msg.channel, discord.DMChannel)):
            return

        COLORS = {
            "r": Game.Cards.CardColour.RED,
            "g": Game.Cards.CardColour.GREEN,
            "b": Game.Cards.CardColour.BLUE,
            "y": Game.Cards.CardColour.YELLOW,
            "": None
        }
        try:
            user_pos = self.users[author.id]
            game = self.games[user_pos]
            player_pos = [p.user for p in game.players].index(author)
        except KeyError:
            await author.send("You have to be in a game to play.")
            return

        text = msg.content.split(" ")
        if len(text) < 2:
            text.append("")

        success = False
        try:
            if text[0] == "0":
                success = game.draw_card(player_pos)
            else:
                success = game.play_card(
                    player_pos,
                    int(text[0]) - 1,
                    COLORS[text[1].lower()])
        except (ValueError, IndexError):
            await author.send("Invalid Card. Use number!")
        except KeyError:
            await author.send("Invalid color: use r, g, b or y!")
        except (
                Game.WrongCardException,
                Game.NotYourTurnException,
                Game.MissingColourException) as e:
            await author.send(e.args[0])

        if not success:
            return

        if winner := game.check_win():
            await Fun.show_win(game, winner)
            self._end_uno(game)
            return
        else:
            game.next_turn()
        for p in game.players:
            await Fun.show_status(game, p)

    @commands.command("start-uno")
    async def start_uno(self, ctx: commands.Context) -> None:
        """Start a uno game with the @mentioned users."""
        # Get Discord Users
        users: "list[DC_Clients]" = [ctx.author]
        users += [u for u in ctx.message.mentions if
                  isinstance(u, (discord.Member, discord.User))]

        # Check if Users are already in a game
        if unavailable := [int(u.id) for u in users if u.id in self.users.keys()]:
            unavailable = ', '.join([f"<@{str(id)}>" for id in unavailable])
            await ctx.send(
                f"Can't start game, because {unavailable} are already in a game.")
            return

        # Create Game and add users to list
        game_id = Fun._find_first_unused_key(self.games)
        game = Game.Game([Game.Player(p) for p in users], game_id)
        self.games[game_id] = game
        for i, user in enumerate(users):
            self.users[user.id] = game_id
            await Fun.show_status(game, game.players[i])

    @commands.command("leave-uno")
    async def leave(self, ctx: commands.Context):
        await self._leave_uno(ctx.author.id)

    async def _leave_uno(self, uid: int):
        """Remove a player from their game."""
        game_id = self.users.pop(uid)
        game = self.games[game_id]
        game.players = (
            [u for u in game.players if u.user.id != uid])

        if len(game.players) == 0:
            self._end_uno(game)
            return

        for p in game.players:
            await Fun.show_status(game, p)

    def _end_uno(self, game: Game.Game) -> None:
        """Stop a game and remove the users."""
        # Remove Players from users
        for u in game.players:
            self.users.pop(u.user.id)

        # Remove game from games
        self.games.pop(game.id)

    @staticmethod
    def _find_first_unused_key(dic: "dict[int, Any]") -> int:
        """Find the first unused integer key of a dictionary."""
        key = 0
        while key in dic.keys():
            key += 1
        return key

    @staticmethod
    async def show_status(game: Game.Game, player: Game.Player) -> None:
        """Show the current status of the game to the player."""
        colour = discord.Color.green() if player.turn else discord.Color.dark_gray()
        turn = game.players[game.turn].user.name

        emb = discord.Embed(
            color=colour,
            title=f"UNO-Game - It's {turn}s turn",
            description="Type 0 to draw a card or the card number to play that card."
        )

        players = [f"{pl.user.name}: {len(pl.deck)}" for pl in game.players]
        cards = [f"{i + 1}.{str(card)}" for i, card in enumerate(player.deck)]

        emb.add_field(name="Draw", value=str(game.drawcache - 1))
        emb.add_field(name="Discard", value=str(game.discard))
        emb.add_field(name="Cards Left", value="\n".join(players))
        emb.add_field(name="Your Cards", value=" ".join(cards))

        await player.user.send(embed=emb)

    @staticmethod
    async def show_win(game: Game.Game, winplayer: Game.Player) -> None:
        """Show a win message to all players of a game."""
        emb = discord.Embed(
            color=discord.Color.red(),
            title=f"UNO-Game - {winplayer.user.name} won!"
        )

        for p in game.players:
            if p == winplayer:
                emb.color = discord.Color.green()
            else:
                emb.color = discord.Color.red()
            await p.user.send(embed=emb)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    async def ping_command(self, ctx: commands.Context) -> None:
        await ctx.send(
            f"🏓 Pong!: {self.bot.latency * 1000:.2f}ms",
        )

    # @commands.cooldown(1, 5, commands.BucketType.user)
    # @commands.command(name="poll", description="Creates a reaction poll")
    # async def poll_command(self, ctx: commands.Context, *, text: str) -> None:
    #     with suppress(discord.HTTPException, AttributeError):
    #         await ctx.message.delete()
    #
    #     embed = PollEmbed(ctx, text)
    #
    #     message = await ctx.send(embed=embed)
    #     await message.add_reaction("👍")
    #     await message.add_reaction("👎")
    #     await message.add_reaction("🤷")

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    async def roll_command(
            self,
            ctx: commands.Context,
            maximum: int = 100,
    ) -> None:
        await ctx.send(f"🎲 Rolled: **{random.randint(1, maximum)}**")

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    async def flip_command(self, ctx: commands.Context) -> None:
        await ctx.send(f"🪙 Flipped: **{'Heads' if random.randint(0, 1) else 'Tails'}**")

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    async def duel_command(self, ctx: commands.Context, user: discord.User) -> None:
        if user is ctx.author:
            await ctx.send("You can't duel yourself!")
            return

        if user.bot:
            await ctx.send("You can't duel a bot!")
            return

        await ctx.send(
            f"{ctx.author.mention} and {user.mention} dueled for **{random.randint(2, 120)}** hours! It was a long battle, but {numpy.choice([ctx.author.mention, user.mention])} came out victorious!",
            silent=True,
        )

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    async def love_command(self, ctx: commands.Context, user: discord.User) -> None:
        if user is ctx.author:
            await ctx.send("You can't love yourself!")
            return

        if user.bot:
            await ctx.send("You can't love a bot!")
            return

        love_percentage = (ctx.author.id + user.id) % 100

        await ctx.send(
            f"{ctx.author.mention} and {user.mention} love each other **{love_percentage}%**!",
            silent=True,
        )

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(
        aliases=["rd", "hc"],
    )
    async def rollduel_command(self, ctx: commands.Context, user: discord.User) -> None:
        if user is ctx.author:
            await ctx.send("You can't duel yourself!")
            return

        if user.bot:
            await ctx.send("You can't duel a bot!")
            return

        roll_1 = random.randint(1, 100)
        roll_2 = random.randint(1, 100)

        if roll_1 == roll_2:
            await ctx.send(
                f"{ctx.author.mention} and {user.mention} dueled in a roll off!\nThey tied with a roll of **{roll_1}**!",
                silent=True,
            )
            return

        winner, loser = (ctx.author, user) if roll_1 > roll_2 else (user, ctx.author)
        roll_1, roll_2 = max(roll_1, roll_2), min(roll_1, roll_2)
        await ctx.send(
            f"{ctx.author.mention} and {user.mention} dueled in a roll off!\n{winner.mention} rolled **{roll_1}** and {loser.mention} rolled **{roll_2}**!\n{winner.mention} won!",
            silent=True,
        )


def setup(bot):
    c = Fun(bot)
    bot.add_cog(c)
