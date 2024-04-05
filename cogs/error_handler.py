#  ______     __  __     __  __     ______     ______
# /\  ___\   /\ \/ /    /\ \_\ \   /\  ___\   /\  == \
# \ \___  \  \ \  _--.  \ \____ \  \ \___  \  \ \  __<
#  \/\_____\  \ \_\ \_\  \/\_____\  \/\_____\  \ \_____\
#   \/_____/   \/_/\/_/   \/_____/   \/_____/   \/_____/
#
#                    AGPL-3.0 license

from utils import *
from discord.ext import commands as skySB


class ErrorHandler(skySB.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.langpack = langs.getcurrent()

    @skySB.Cog.listener()
    async def on_command_error(self, ctx, error):
        """
        https://github.com/vined-underscore/VBot/blob/main/cogs/error_handler.py
        """
        if ctx.cog:
            if ctx.cog._get_overridden_method(ctx.cog.cog_command_error) is not None:
                return

        error = getattr(error, "original", error)
        if isinstance(error, skySB.CommandNotFound):
            return
        elif isinstance(error, skySB.MissingRequiredArgument):
            await answer(ctx, self.langpack["argRequired"].format(error.param.name))
        elif isinstance(error, skySB.BadArgument):
            await answer(ctx, self.langpack["argBad"])
        elif isinstance(error, skySB.MissingPermissions):
            await answer(ctx, self.langpack["missingPrems"])
        else:
            print(error)


async def setup(bot):
    await bot.add_cog(ErrorHandler(bot))
