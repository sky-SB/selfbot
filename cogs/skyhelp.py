#  ______     __  __     __  __     ______     ______
# /\  ___\   /\ \/ /    /\ \_\ \   /\  ___\   /\  == \
# \ \___  \  \ \  _--.  \ \____ \  \ \___  \  \ \  __<
#  \/\_____\  \ \_\ \_\  \/\_____\  \/\_____\  \ \_____\
#   \/_____/   \/_/\/_/   \/_____/   \/_____/   \/_____/
#
#                    AGPL-3.0 license

from utils import *

from discord.ext import commands as skySB


class Help(skySB.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.langpack = langs.getcurrent()["help"]

    @skySB.command(
        aliases=["h", "commands"],
        description=langs.getcurrent()["help"]["help"]["description"],
    )
    async def help(self, ctx):
        msg = ""
        msg += self.langpack["help"]["title"]
        msg += self.langpack["help"]["prefix"].format(config.get("prefix"))

        for cog in self.bot.cogs:
            cog_commands = self.bot.get_cog(cog).get_commands()

            for command in cog_commands:
                msg += self.langpack["help"]["cmdformat"].format(
                    command.name, command.description
                )

        await answer(ctx, msg)


async def setup(bot):
    await bot.add_cog(Help(bot))
