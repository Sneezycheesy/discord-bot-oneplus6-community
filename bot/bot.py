from pathlib import Path
import discord
from discord.ext import commands
from decouple import config

class DiscordBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=self.prefix,
            case_insensitive=True,
            intents=discord.Intents.all()
        )

    def prefix(self, bot, msg):
        return commands.when_mentioned_or(config("PREFIX"))(bot, msg)

    def setup_cogs(self):
        for c in Path('.').glob('./bot/cogs/*.py'):
            self.load_extension(f'bot.cogs.{c.stem}')

    def run(self):
        api_token = config('API_TOKEN')
        super().run(api_token, reconnect=True)

    async def process_commands(self, msg):
        ctx = await self.get_context(msg, cls=commands.Context)
        if ctx.command is not None:
            await self.invoke(ctx)
    
    async def on_ready(self):
        self.setup_cogs()
        print(f'{self.user} has logged in.')

