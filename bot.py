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
    default_enabled_guilds=[int(os.environ["SNEAKY_GUILD_ID"]),int(os.environ["MOVIESLAND_GUILD_ID"]),int(os.environ["SAID_GUILD_ID"])],
    owner_ids=[int(os.environ["OWNER_ID"])],
    case_insensitive_prefix_commands=True,
    intents = hikari.Intents.ALL,
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
    await bot.rest.create_message(channel=int(os.environ["GENERAL_CHANNEL_ID"]),content="Wassup Buddy.")

@bot.listen(hikari.StoppingEvent)
async def on_stopped(event: hikari.StoppingEvent) -> None:
    await bot.rest.create_message(channel=int(os.environ["GENERAL_CHANNEL_ID"]),content="See You Soon Buddy.")   
  

bot.run(
    status=hikari.Status.ONLINE,
    activity=hikari.Activity(name="NETFLIX",type=hikari.ActivityType.WATCHING),
)

