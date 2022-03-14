
from __init__ import PREFIX
import hikari
import lightbulb
import datetime


plugin = lightbulb.Plugin("random")

@plugin.command
@lightbulb.command(name="botty",description="give infos about the bot",aliases=["bt","info","if"])
@lightbulb.implements(lightbulb.PrefixCommand,lightbulb.SlashCommand)
async def embed(ctx: lightbulb.Context) -> None:
        aliases=[]
        aliases=" ".join(ctx.command.aliases)
        embed=(
            hikari.Embed(
            title=f"{str(ctx.bot.get_me()).upper()}",
            description=f"{plugin.bot.application.owner.username} is my only owner!!!",
            timestamp=datetime.datetime.now().astimezone(),
            colour= hikari.Color(0x7f9c85),
            )
            .add_field(name=" I was created in".upper(), value=plugin.bot.application.created_at.astimezone().ctime())
            .add_field(name="You can call me by these commands:".upper(),value=aliases)
            .set_footer(
                text=f"Requested by {ctx.member.display_name}",
                icon=ctx.member.avatar_url
            )
            .set_thumbnail("https://media.vogue.fr/photos/5c8a55363d44a0083ccbef54/2:3/w_1600,c_limit/GettyImages-625257378.jpg")
        )
        await ctx.respond(embed, reply=True, mentions_reply=True)




def load(bot:lightbulb.BotApp):
    bot.add_plugin(plugin)

def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(plugin)