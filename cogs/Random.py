from discord.ext import commands
import random
import time

class Random(commands.Cog, name="Random"):
    def __init__(self, bot):
        self.bot = bot
        self.loading_time = time.time()

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Random cog loaded in {round(time.time() - self.loading_time, 2)} seconds')

    @commands.hybrid_command(name="random", aliases=["rand"], usage=">random <min> <max>")
    async def random(self, ctx, min: int, max: int):
        '''Generates a random number between min and max'''
        await ctx.reply(f'Result: {random.randint(min, max)}')

    @commands.hybrid_command(name="choose", aliases=["choice"], usage=">choose <choice1; choice2; ...>")
    async def choose(self, ctx, choices: str):
        '''Chooses between multiple choices
        > **Note:** Choices have to be separated by `; ` *(e.g. "choice1; choice2")*'''
        choices = choices.split('; ')
        if not all(isinstance(choice, str) for choice in choices):
            await ctx.reply('**All choices have to be strings!**')
            return
        
        await ctx.reply(f'**Choice:** {random.choice(choices)}')

    @commands.hybrid_command(name="coinflip", aliases=["flip"], usage=">coinflip [head/tail]")
    async def coinflip(self, ctx, prediction: str = None):
        ''':coin: Flips a coin'''
        result = random.choice(["Head", "Tail"])

        if prediction is not None and prediction.lower() not in ["head", "tail"]:
            await ctx.reply('**Invalid prediction!**')
            return

        if prediction is None:
            await ctx.reply(f':coin: {result} !')
        else:
            if prediction.lower() == result.lower():
                await ctx.reply(f':coin: {result} !\n**You won!**')
            else:
                await ctx.reply(f':coin: {result} !\n**You lost!**')

    @commands.hybrid_command(name="roll", aliases=["dice"], usage=">roll <NdN>")
    async def roll(self, ctx, dice: str):
        ''':game_die: Rolls a dice in NdN format'''
        try:
            rolls, limit = map(int, dice.split('d'))
        except Exception:
            await ctx.reply('Format has to be in NdN!')
            return

        result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
        await ctx.reply(f':game_die: **{dice}**\n**Result:** {result}')

    @commands.hybrid_command(name="8ball", aliases=["8b"], usage=">8ball <question>")
    async def eightball(self, ctx, *, question: str):
        ''':crystal_ball: Ask the magic 8ball a question'''
        responses = [
            'It is certain.',
            'It is decidedly so.',
            'Without a doubt.',
            'Yes - definitely.',
            'You may rely on it.',
            'As I see it, yes.',
            'Most likely.',
            'Outlook good.',
            'Yes.',
            'Signs point to yes.',
            'Reply hazy, try again.',
            'Ask again later.',
            'Better not tell you now...',
            'Cannot predict now.',
            'Concentrate and ask again.',
            "Don't count on it.",
            'My reply is no.',
            'My sources say no.',
            'Outlook not so good...',
            'Very doubtful.'
        ]
        await ctx.reply(f'**Question:** {question}\n:crystal_ball: **Answer:** {random.choice(responses)}')

    def _rps_to_emoji(self, choice: str):
        if choice.lower() == "rock":
            return ":right_facing_fist:"
        elif choice.lower() == "paper":
            return ":rightwards_hand:"
        elif choice.lower() == "scissors":
            return ":v:"

    @commands.hybrid_command(name="rps", aliases=["rockpaperscissors"], usage=">rps <rock/paper/scissors>")
    async def rps(self, ctx, choice: str):
        '''Play rock paper scissors'''
        choice = choice.lower()

        beats = {
            'rock': 'scissors',
            'paper': 'rock',
            'scissors': 'paper'
        }

        if choice not in beats.keys():
            await ctx.reply('**Invalid choice!**')
            return
        
        bot_choice = random.choice(list(beats.keys()))

        you_msg = f'**You:** {self._rps_to_emoji(choice)}'
        bot_msg = f'**Bot:** {self._rps_to_emoji(bot_choice)}'

        if choice == bot_choice:
            await ctx.reply(f'{you_msg}\n{bot_msg}\n**Draw!**')
        elif beats[choice] == bot_choice:
            await ctx.reply(f'{you_msg}\n{bot_msg}\n**You won!**')
        else:
            await ctx.reply(f'{you_msg}\n{bot_msg}\n**You lost!**')

async def setup(bot):
    await bot.add_cog(Random(bot))