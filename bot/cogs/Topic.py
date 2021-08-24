from discord.ext import commands
import re
import requests
from discord.ext.tasks import loop

class Topic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def get_current_mainline(self):
        site_content = str(requests.get('http://kernel.org').content)
        mainline = re.search('mainline:(.+?)</strong>', site_content).group(1)
        mainline = re.sub(re.compile(r'(.+?)<strong>', re.I), r'', mainline)
        return mainline

    @loop(hours=8)
    async def update_mainline_topic(self):
        mainline = self.get_current_mainline()
        for guild in self.bot.guilds:
            for channel in guild.text_channels:
                if channel.name == 'mainline':
                    await channel.edit(topic=f'{mainline} is out! https://www.kernel.org/')


def setup(bot):
    bot.add_cog(Topic(bot))
    Topic(bot).update_mainline_topic.start()
    
