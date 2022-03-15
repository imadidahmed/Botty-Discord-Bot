
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

@plugin.command
@lightbulb.command("help","a commands helper")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def help(ctx: lightbulb.Context) -> None:
    movie_commands=["","👉 !𝖒𝖔𝖛𝖎𝖊 𝖘𝖊𝖆𝖗𝖈𝖍 [𝖒𝖔𝖛𝖎𝖊 𝖓𝖆𝖒𝖊]: 𝕲𝖊𝖙 𝖉𝖊𝖙𝖆𝖎𝖑𝖘 𝖆𝖇𝖔𝖚𝖙 𝖙𝖍𝖊 𝖒𝖔𝖛𝖎𝖊.","👉 !𝖒𝖔𝖛𝖎𝖊 𝖜𝖆𝖙𝖈𝖍 [𝖒𝖔𝖛𝖎𝖊 𝖓𝖆𝖒𝖊]: 𝕲𝖊𝖙 𝖆 𝖉𝖎𝖗𝖊𝖈𝖙 𝖘𝖙𝖗𝖊𝖆𝖒𝖎𝖓𝖌 𝖑𝖎𝖓𝖐𝖘 𝖋𝖔𝖗 𝖜𝖆𝖙𝖈𝖍𝖎𝖓𝖌 𝖆𝖓𝖉 𝖉𝖔𝖜𝖓𝖑𝖔𝖆𝖉𝖎𝖓𝖌.","👉 !𝖒𝖔𝖛𝖎𝖊 𝖙𝖗𝖊𝖓𝖉𝖎𝖓𝖌: 𝕲𝖊𝖙 𝖙𝖗𝖊𝖓𝖉𝖎𝖓𝖌 𝖒𝖔𝖛𝖎𝖊𝖘 𝖙𝖍𝖎𝖘 𝖜𝖊𝖊𝖐.","👉 !𝖒𝖔𝖛𝖎𝖊 𝖘𝖎𝖒𝖎𝖑𝖆𝖗 [𝖒𝖔𝖛𝖎𝖊 𝖓𝖆𝖒𝖊]: 𝕲𝖊𝖙 𝖆 𝖑𝖎𝖘𝖙 𝖔𝖋 𝖘𝖎𝖒𝖎𝖑𝖆𝖗 𝖒𝖔𝖛𝖎𝖊𝖘.","👉 !𝖒𝖔𝖛𝖎𝖊 𝖕𝖔𝖕𝖚𝖑𝖆𝖗: 𝕲𝖊𝖙 𝖆 𝖑𝖎𝖘𝖙 𝖔𝖋 𝖙𝖍𝖊 𝖈𝖚𝖗𝖗𝖊𝖓𝖙 𝖕𝖔𝖕𝖚𝖑𝖆𝖗 𝖒𝖔𝖛𝖎𝖊𝖘."]
    serie_commands=["","👉 !𝖘𝖊𝖗𝖎𝖊 𝖘𝖊𝖆𝖗𝖈𝖍 [𝖘𝖊𝖗𝖎𝖊 𝖓𝖆𝖒𝖊]: 𝕲𝖊𝖙 𝖉𝖊𝖙𝖆𝖎𝖑𝖘 𝖆𝖇𝖔𝖚𝖙 𝖙𝖍𝖊 𝕿𝖁 𝕾𝖍𝖔𝖜.","👉 !𝖘𝖊𝖗𝖎𝖊 𝖜𝖆𝖙𝖈𝖍 [𝖘𝖊𝖗𝖎𝖊 𝖓𝖆𝖒𝖊] [𝖘𝖊𝖆𝖘𝖔𝖓 𝖓𝖚𝖒𝖇𝖊𝖗] [𝖊𝖕𝖎𝖘𝖔𝖉𝖊 𝖓𝖚𝖒𝖇𝖊𝖗]: 𝖂𝖆𝖙𝖈𝖍 𝖆 𝖈𝖍𝖔𝖘𝖊𝖓 𝕰𝖕𝖎𝖘𝖔𝖉𝖊 𝖋𝖗𝖔𝖒 𝖞𝖔𝖚𝖗 𝕿𝖁 𝖘𝖍𝖔𝖜.","👉 !𝖘𝖊𝖗𝖎𝖊 𝖙𝖔𝖕_𝖗𝖆𝖙𝖊𝖉: 𝕲𝖊𝖙 𝖆 𝖑𝖎𝖘𝖙 𝖔𝖋 𝖙𝖍𝖊 𝖙𝖔𝖕 𝖗𝖆𝖙𝖊𝖉 𝕿𝖁 𝖘𝖍𝖔𝖜𝖘.","👉 !𝖘𝖊𝖗𝖎𝖊 𝖕𝖔𝖕𝖚𝖑𝖆𝖗: 𝕲𝖊𝖙 𝖆 𝖑𝖎𝖘𝖙 𝖔𝖋 𝖙𝖍𝖊 𝖈𝖚𝖗𝖗𝖊𝖓𝖙 𝖕𝖔𝖕𝖚𝖑𝖆𝖗 𝕿𝖁 𝖘𝖍𝖔𝖜𝖘.","👉 !𝖘𝖊𝖗𝖎𝖊 𝖘𝖎𝖒𝖎𝖑𝖆𝖗 [𝖘𝖊𝖗𝖎𝖊 𝖓𝖆𝖒𝖊]: 𝕲𝖊𝖙 𝖆 𝖑𝖎𝖘𝖙 𝖔𝖋 𝖘𝖎𝖒𝖎𝖑𝖆𝖗 𝕿𝖁 𝖘𝖍𝖔𝖜𝖘." ]
    others=["👉 !𝖇𝖔𝖙𝖙𝖞: 𝕴𝖙 𝖌𝖎𝖛𝖊𝖘 𝖎𝖓𝖋𝖔𝖘 𝖆𝖇𝖔𝖚𝖙 𝖙𝖍𝖊 𝖇𝖔𝖙.","👉 !𝖕𝖎𝖓𝖌: 𝕷𝖆𝖙𝖊𝖓𝖈𝖞."]
    others= "\n".join(others)
    movie_commands="\n".join(movie_commands)
    serie_commands="\n".join(serie_commands)
    embed=(hikari.Embed(
        title="𝐁𝐎𝐓𝐓𝐘 𝐁𝐈𝐁𝐋𝐄",
        colour= hikari.Color(0xe5e5e5),
        timestamp=datetime.datetime.now().astimezone(),
    )
    .add_field(name="𝓓𝓘𝓢𝓒𝓛𝓐𝓘𝓜𝓔𝓡",value="𝖞𝖔𝖚 𝖈𝖆𝖓 𝖚𝖘𝖊 𝖊𝖎𝖙𝖍𝖊𝖗 / 𝖔𝖗 ! \n 𝕽𝖊𝖒𝖔𝖛𝖊 𝖙𝖍𝖊 𝖕𝖆𝖗𝖊𝖓𝖙𝖍𝖊𝖘𝖊𝖘 𝖜𝖍𝖊𝖓 𝖞𝖔𝖚'𝖗𝖊 𝖜𝖗𝖎𝖙𝖙𝖎𝖓𝖌 𝖙𝖍𝖊 𝖒𝖔𝖛𝖎𝖊 𝖔𝖗 𝖙𝖍𝖊 𝖘𝖊𝖗𝖎𝖊 𝖓𝖆𝖒𝖊 𝖎𝖓 𝖙𝖍𝖊 𝖈𝖔𝖒𝖒𝖆𝖓𝖉𝖘.")
    .add_field(name="𝓜𝓞𝓥𝓘𝓔 𝓒𝓞𝓜𝓜𝓐𝓝𝓓𝓢",value=movie_commands)
    .add_field(name="𝓢𝓔𝓡𝓘𝓔 𝓒𝓞𝓜𝓜𝓐𝓝𝓓𝓢",value=serie_commands)
    .add_field(name="𝓞𝓣𝓗𝓔𝓡 𝓒𝓞𝓜𝓜𝓐𝓝𝓓𝓢",value=others)
    .set_footer(f"Requested by {ctx.member.display_name}",icon=ctx.member.avatar_url)

)
    await ctx.respond(embed)


def load(bot:lightbulb.BotApp):
    bot.add_plugin(plugin)

def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(plugin)