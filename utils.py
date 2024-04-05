#  ______     __  __     __  __     ______     ______
# /\  ___\   /\ \/ /    /\ \_\ \   /\  ___\   /\  == \
# \ \___  \  \ \  _--.  \ \____ \  \ \___  \  \ \  __<
#  \/\_____\  \ \_\ \_\  \/\_____\  \/\_____\  \ \_____\
#   \/_____/   \/_/\/_/   \/_____/   \/_____/   \/_____/
#
#                    AGPL-3.0 license

import json
import logging
import asyncio
import os
import re
import io

import discord
import discord.utils
from discord.ext import commands

from colored import Fore, Style
from types import FunctionType

# Logging
logging.basicConfig(
    format=f"%(asctime)s | [{Fore.CYAN}%(levelname)s{Style.RESET}] %(message)s",
    level=logging.WARNING,
    datefmt="%H:%M",
)
logger = logging.getLogger(__name__)


# Config
with open("config.json") as f:
    config = json.load(f)

# Bot
bot = commands.Bot(command_prefix=config.get("prefix"), self_bot=True)
bot.remove_command("help")


# fix
async def _get_build_number(session) -> int:
    """Fetches client build number, thx discord-S.C.U.M and discord.py-self community!"""
    default_build_number = 9999
    try:
        login_page_request = await session.get("https://discord.com/login", timeout=7)
        login_page = await login_page_request.text()
        for asset in re.compile(r"(\w+\.[a-z0-9]+)\.js").findall(login_page)[-1:]:
            build_url = "https://discord.com/assets/" + asset + ".js"
            build_request = await session.get(build_url, timeout=7)
            build_file = await build_request.text()
            build_find = re.findall(r'Build Number:\D+"(\d+)"', build_file)
            if build_find:
                return int(build_find[0]) if build_find else default_build_number
    except asyncio.TimeoutError:
        return default_build_number


discord.utils._get_build_number = _get_build_number  # type: ignore


# Langpacks
class langs:
    @staticmethod
    def all() -> list:
        """
        Get all langpacks

        Returns:
            List - list all langpacks in directory.
        """
        return os.listdir("./langs/")

    @staticmethod
    def getcurrent() -> dict:
        """
        Get current langpack

        Returns:
            Dict - langpack JSON data
        """
        with open(config.get("language")) as f:
            langpack = json.load(f)
        return langpack

    @staticmethod
    def get(file: str) -> dict:
        """
        Get langpack

        Parameters:
            file (String) - file path
        Returns:
            Dict - langpack JSON data
        """
        with open(file) as f:
            langpack = json.load(f)

        return langpack


# MOTD
motd = """
  ______     __  __     __  __     ______     ______    
 /\  ___\   /\ \/ /    /\ \_\ \   /\  ___\   /\  == \   
 \ \___  \  \ \  _--.  \ \____ \  \ \___  \  \ \  __<   
  \/\_____\  \ \_\ \_\  \/\_____\  \/\_____\  \ \_____\
   \/_____/   \/_/\/_/   \/_____/   \/_____/   \/_____/
"""


# answer
async def answer(
    ctx,
    message: str,
    photo: bool = False,
    document: bool = False,
    delete: bool = True,
    **kwargs,
) -> str:
    """
    Answer text

    Parameters:
        ctx (Content),
        message (String)

    Returns:
        String - message text
    """
    responses = []
    if len(message) > 2000:
        chunks = [message[i: i + 2000] for i in range(0, len(message), 2000)]
        for chunk in chunks:
            responses.append(await ctx.reply(chunk))
    else:
        try:
            responses.append(await ctx.message.edit(message))
        except:
            responses.append(await ctx.reply(message))

    await asyncio.sleep(config.get("deletetimer"))

    for response in responses:
        if delete:
            await response.delete()
    return responses


# system data
def get_ram() -> float:
    """
    ! from teagram

    Get your ram usage

    Returns:
        Float - ram usage
    """
    try:
        import psutil

        process = psutil.Process(os.getpid())
        mem = process.memory_info()[0] / 2.0**20
        for child in process.children(recursive=True):
            mem += child.memory_info()[0] / 2.0**20
        return round(mem, 1)
    except:
        return 0


def get_cpu() -> float:
    """
    ! from teagram

    Get CPU usage as a percentage

    Returns:
        Float - CPU usage as a percentage.
    """

    try:
        import psutil

        process = psutil.Process(os.getpid())
        cpu = process.cpu_percent()

        for child in process.children(recursive=True):
            cpu += child.cpu_percent()

        return cpu
    except:
        return 0


def get_platform() -> str:
    """
    ! from teagram

    Get the platform information

    Returns:
        String - Platform information
    """

    IS_TERMUX = "com.termux" in os.environ.get("PREFIX", "")
    IS_CODESPACES = "CODESPACES" in os.environ
    IS_DOCKER = "DOCKER" in os.environ
    IS_GOORM = "GOORM" in os.environ
    IS_WIN = "WINDIR" in os.environ
    IS_ZACHOST = "zachemhost" in os.environ
    IS_WSL = "WSL_DISTRO_NAME" in os.environ

    if IS_TERMUX:
        return "📱 Termux"
    elif IS_DOCKER:
        return "🐳 Docker"
    elif IS_GOORM:
        return "🦾 Goorm"
    elif IS_WSL:
        return "🧱 WSL"
    elif IS_WIN:
        return "💻 Windows"
    elif IS_CODESPACES:
        return "👨‍💻 Github Codespaces"
    elif IS_ZACHOST:
        return "❔ Zachem㉿Host"
    else:
        return "🖥️ VDS"


# text validators
class validators:
    def Link(url: str) -> bool:
        regex = re.compile(
            r"^(?:http|https)://"
            r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"
            r"localhost|"
            r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"
            r"(?::\d+)?"
            r"(?:/?|[/?]\S+)$",
            re.IGNORECASE,
        )
        return bool(regex.match(url))
