import os

import lightbulb
import hikari
import logging
import dotenv
import datetime
from __init__ import PREFIX


dotenv.load_dotenv()
bot = lightbulb.BotApp(
    token = os.environ["TOKEN"],
    prefix = PREFIX,
    banner = None,
    owner_ids=[int(os.environ["OWNER_ID"])],
    case_insensitive_prefix_commands=True,
    intents = hikari.Intents.ALL,
    help_class=None
)


@bot.listen(hikari.StartingEvent)
async def on_starting(event: hikari.StartingEvent) -> None:
    logging.info("Bot is Starting ...")
    logging.info("extensions starts loading...")
    bot.load_extensions_from("extensions")
    
@bot.listen(hikari.StartedEvent)
async def on_started(event: hikari.StartedEvent) -> None:
    logging.info("extensions loaded succesfully")
    logging.info("Bot deployed succesfully")

@bot.listen(hikari.StoppingEvent)
async def on_stopped(event: hikari.StoppingEvent) -> None:
    ...

bot.run(
    status=hikari.Status.ONLINE,
    activity=hikari.Activity(name="NETFLIX",type=hikari.ActivityType.WATCHING),
)

