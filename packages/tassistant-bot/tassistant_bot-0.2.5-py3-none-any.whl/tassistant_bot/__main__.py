# -*- coding: utf-8 -*-
import logging
import os

import colorlog
import click

from pyrogram import Client, idle
import asyncio

from tassistant_bot.helpers import config, I18n
from tassistant_bot.loader import ModuleLoader

formatter = colorlog.ColoredFormatter(
    "| %(log_color)s%(asctime)s%(reset)s | %(log_color)s%(levelname)s%(reset)s | %(log_color)s%(name)s%(reset)s, "
    "%(log_color)s%(funcName)s:%(lineno)d%(reset)s: %(message)s",
    datefmt=None,
    reset=True,
    log_colors={
        "DEBUG": "cyan",
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "bold_red",
    },
)

file_formatter = logging.Formatter(
    "| %(asctime)s | %(levelname)s | %(name)s, %(funcName)s:%(lineno)d: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

log_handler = colorlog.StreamHandler()
log_handler.setFormatter(formatter)

file_handler = logging.FileHandler("app.log")
file_handler.setFormatter(file_formatter)

logger = logging.getLogger()
logger.addHandler(log_handler)
logger.addHandler(file_handler)

logger.setLevel(logging.INFO)
logging.getLogger("pyrogram").setLevel(logging.INFO)


def get_env(key, default=None):
    value = os.environ.get(key)
    return value if value is not None else default


@click.command()
@click.option("--api-id", default=None, help="Telegram API ID.")
@click.option("--session-string", default=None, help="Telegram Session String.")
@click.option("--api-hash", default=None, help="Telegram API Hash.")
@click.option("--use-core-module", default=None, help="Use default core pack")
@click.option("--log-level", default="INFO", help="Logging level.")
@click.option(
    "--env",
    is_flag=True,
    help="Get api_id, api_hash, session_string from environment variables.",
)
def main(api_id, api_hash, session_string, use_core_module, log_level, env):
    logger.setLevel(getattr(logging, log_level.upper()))

    if env:
        api_id = api_id if api_id is not None else os.getenv("TELEGRAM_API_ID")
        api_hash = api_hash if api_hash is not None else os.getenv("TELEGRAM_API_HASH")
        session_string = (
            session_string
            if session_string is not None
            else os.getenv("TELEGRAM_SESSION_STRING")
        )
        use_core_module = (
            use_core_module
            if use_core_module is not None
            else os.getenv("USE_CORE_MODULE", "True")
        )

    if api_id:
        config.set("TELEGRAM_API_ID", api_id)
    if api_hash:
        config.set("TELEGRAM_API_HASH", api_hash)
    if session_string:
        config.set("TELEGRAM_SESSION_STRING", session_string)
    if use_core_module is not None:
        config.set("USE_CORE_MODULE", use_core_module)

    asyncio.run(run_main())


async def run_main():
    _ = I18n("ru").get

    if config.get("TELEGRAM_SESSION_STRING"):
        app = Client("_user_", session_string=config.get("TELEGRAM_SESSION_STRING"))
    else:
        app = Client(
            name="my_account",
            api_id=config.get("TELEGRAM_API_ID"),
            api_hash=config.get("TELEGRAM_API_HASH"),
        )

    await app.start()
    loader = ModuleLoader(client=app, command_prefix=".")
    loader.download_module(
        "https://github.com/kinsoRick/tassistant-core.git", "tassistant_core"
    )
    loader.update_all()
    loader.load_all_modules()

    await idle()


if __name__ == "__main__":
    main()
