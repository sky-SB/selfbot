#  ______     __  __     __  __     ______     ______    
# /\  ___\   /\ \/ /    /\ \_\ \   /\  ___\   /\  == \   
# \ \___  \  \ \  _--.  \ \____ \  \ \___  \  \ \  __<   
#  \/\_____\  \ \_\ \_\  \/\_____\  \/\_____\  \ \_____\
#   \/_____/   \/_/\/_/   \/_____/   \/_____/   \/_____/
#   
#                    AGPL-3.0 license

import os
from utils import config, motd, bot, logger
from colored import Fore, Style

print(motd)
logger.warning(f'status: {Fore.YELLOW}loading...{Style.RESET}')

@bot.event
async def on_ready():
    os.system('clear')
    print(motd)
    logger.warning(f'status: {Fore.GREEN}success{Style.RESET}')
    logger.warning(f'connected: {Style.BOLD}{bot.user}{Style.RESET}')
    logger.warning(f'prefix: {Style.BOLD}{config.get("prefix")}{Style.RESET}')
    print("-" * 45)
    
    for file in os.listdir(f"{os.path.realpath(os.path.dirname(__file__))}/cogs"):
        if file.startswith("_"):
            pass
        if file.endswith(".py"):
            extension = file[:-3]
            try:
                await bot.load_extension(f"cogs.{extension}")
            except Exception as e:
                exception = f"{type(e).__name__}: {e}"
                logger.error(f'{extension}: {exception}')

while True:
    bot.run(config.get('token'), log_handler=None)