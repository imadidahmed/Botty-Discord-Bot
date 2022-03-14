import os

import hikari
import  lightbulb
import requests
import datetime
import dotenv


plugin = lightbulb.Plugin("serie")
dotenv.load_dotenv()

base_url="https://api.themoviedb.org/3"
API_KEY=os.environ["MOVIE_API_KEY"]

@plugin.command
@lightbulb.command("serie","command that gonna help you in the tv-show's world.",auto_defer=True)
@lightbulb.implements(lightbulb.PrefixCommandGroup,lightbulb.SlashCommandGroup)
async def serie():
    ...


@serie.child
@lightbulb.option("name","The name of the Tv Show you want to search for.")
@lightbulb.command("search","Get details about a Tv Show.")
@lightbulb.implements(lightbulb.PrefixSubCommand,lightbulb.SlashSubCommand)
async def search(ctx: lightbulb.Context) -> None:
    #connect to api
    endpoint_path="/search/tv"
    endpoint=f"{base_url}{endpoint_path}?api_key={API_KEY}&query={ctx.options.name}"
    r=requests.get(endpoint)
    if r.status_code in range(200,299):
        data = r.json()
        serie_id=data["results"][0]["id"]
    
    endpoint_path2=f"/tv/{serie_id}"
    endpoint2=f"{base_url}{endpoint_path2}?api_key={API_KEY}"
    r2=requests.get(endpoint2)
    if r2.status_code in range(200,299):
        data2 = r2.json()
    
    #manipulate data
    num_of_episodes=data2["number_of_episodes"]
    num_of_seasons=data2["number_of_seasons"]
    overview=data2["overview"]
    serie_title=data2["original_name"]
    rating=data2["vote_average"]
    year=data2["first_air_date"][0:4]
    time=data2["episode_run_time"][0]
    status=data2["status"]
    poster_path=data2["poster_path"]
    poster=f"https://image.tmdb.org/t/p/w500/{poster_path}"
    
    creators=[]
    for i in range(len(data2["created_by"])):
        creators.append(data2["created_by"][i]["name"])
    creators=" - ".join(creators)

    if len(creators)==0:
        creators="Unknown"
    
    genres=[]
    for i in range(len(data2["genres"])):
        genres.append(data2["genres"][i]["name"])
    genres="  ".join(genres)

    
    embed=(hikari.Embed(
        title=f"{serie_title.upper()} ({year})",
        colour= hikari.Color(0xe5e5e5),
        timestamp=datetime.datetime.now().astimezone(),
    )
    .set_thumbnail(poster)
    .add_field(name="OVERVIEW",value=overview)
    .add_field(name="GENRES",value=genres,inline=True)
    .add_field(name="RATING",value=rating,inline=True)
    .add_field(name="STATUS",value=status,inline=True)
    .add_field(name="SEASONS",value=f"{int(num_of_seasons)} season(s)",inline=True)
    .add_field(name="EPISODES",value=f"{int(num_of_episodes)} episode(s)",inline=True)
    .add_field(name="DURATION",value=f"{int(time)} min",inline=True)
    .add_field(name="CREATORS",value=creators)
    .set_footer(f"Requested by {ctx.member.display_name}",icon=ctx.member.avatar_url)

    )
    await ctx.respond(embed)


@serie.child
@lightbulb.option("episode_number"," Episode's number.",type=int)
@lightbulb.option("season_number","Season's number.",type=int)
@lightbulb.option("name","name of the Tv Show you want to watch.")
@lightbulb.command("watch","Watch a chosen Episode from your TV show.")
@lightbulb.implements(lightbulb.PrefixSubCommand,lightbulb.SlashSubCommand)
async def watch(ctx: lightbulb.Context) -> None:
    #connect to api
    endpoint_path="/search/tv"
    endpoint=f"{base_url}{endpoint_path}?api_key={API_KEY}&query={ctx.options.name}"
    r=requests.get(endpoint)
    if r.status_code in range(200,299):
        data = r.json()
    serie_id=data["results"][0]["id"]

    endpoint_path3 = f"/tv/{serie_id}/season/{ctx.options.season_number}"
    endpoint3 = f"{base_url}{endpoint_path3}?api_key={API_KEY}"
    r3=requests.get(endpoint3)
    if r3.status_code in range(200,299):
        data3 = r3.json()

    episode=f"https://imdbembed.xyz/tv/tmdb/{serie_id}-{ctx.options.season_number}-{ctx.options.episode_number}"
    serie_title=data["results"][0]["original_name"]
    poster_path=data["results"][0]["poster_path"]
    poster=f"https://image.tmdb.org/t/p/w500/{poster_path}"

    embed=(hikari.Embed(
        title=f"WATCH {serie_title.upper()} S{ctx.options.season_number} E{ctx.options.episode_number}",
        colour= hikari.Color(0xe5e5e5),
        timestamp=datetime.datetime.now().astimezone(),
        url=episode
    )
    .set_image(poster)
    .set_footer(f"Requested by {ctx.member.display_name}",icon=ctx.member.avatar_url)
    )

    await ctx.respond(embed)


@serie.child
@lightbulb.command("top_rated","Get a list of the top rated TV shows.")
@lightbulb.implements(lightbulb.PrefixSubCommand,lightbulb.SlashSubCommand)
async def top_rated(ctx: lightbulb.Context) -> None:
    endpoint_path="/tv/top_rated"
    endpoint = f"{base_url}{endpoint_path}?api_key={API_KEY}"
    r=requests.get(endpoint)
    if r.status_code in range(200,299):
        data = r.json()

    series_name=[]
    for i in range(len(data["results"])):
        lst = data["results"][i]["original_name"] + " (" + str(data["results"][i]["vote_average"]) + ")"
        series_name.append(lst)
    series_name="\n".join(series_name)
    poster_path=data["results"][0]["poster_path"]
    poster=f"https://image.tmdb.org/t/p/w500/{poster_path}"

    embed=(hikari.Embed(
        title="TOP RATED TV-SHOWS",
        colour= hikari.Color(0xe5e5e5),
        timestamp=datetime.datetime.now().astimezone(),
        )
    .add_field(name="LIST OF TOP RATED TV-SHOWS",value=series_name)
    .set_footer(f"Requested by {ctx.member.display_name}",icon=ctx.member.avatar_url)
    .set_thumbnail(poster)
    )

    await ctx.respond(embed)


@serie.child
@lightbulb.command("popular","Get a list of the current popular TV shows.")
@lightbulb.implements(lightbulb.PrefixSubCommand,lightbulb.SlashSubCommand)
async def popular(ctx: lightbulb.Context) -> None:
    endpoint_path="/tv/popular"
    endpoint = f"{base_url}{endpoint_path}?api_key={API_KEY}"
    r=requests.get(endpoint)
    if r.status_code in range(200,299):
        data = r.json()

    series_name=[]
    for i in range(len(data["results"])):
        lst=data["results"][i]["original_name"] +" ("+ data["results"][i]["first_air_date"][0:4] + ")"
        series_name.append(lst)
    series_name="\n".join(series_name)
    poster_path=data["results"][0]["poster_path"]
    poster=f"https://image.tmdb.org/t/p/w500/{poster_path}"

    embed=(hikari.Embed(
        title="POPULAR TV-SHOWS",
        colour= hikari.Color(0xe5e5e5),
        timestamp=datetime.datetime.now().astimezone(),
        )
    .add_field(name="list of the current popular TV shows".upper(),value=series_name)
    .set_footer(f"Requested by {ctx.member.display_name}",icon=ctx.member.avatar_url)
    .set_thumbnail(poster)
    )

    await ctx.respond(embed)


@serie.child
@lightbulb.option("name","The name of the TV show you want similar TV shows like it.")
@lightbulb.command("similar","Get a list of similar TV shows.")
@lightbulb.implements(lightbulb.PrefixSubCommand,lightbulb.SlashSubCommand)
async def search(ctx: lightbulb.Context) -> None:
    #connect to api
    endpoint_path="/search/tv"
    endpoint=f"{base_url}{endpoint_path}?api_key={API_KEY}&query={ctx.options.name}"
    r=requests.get(endpoint)
    if r.status_code in range(200,299):
        data = r.json()
        serie_id=data["results"][0]["id"]

    endpoint_path2 = f"/tv/{serie_id}/similar"
    endpoint2 = f"{base_url}{endpoint_path2}?api_key={API_KEY}"
    r2=requests.get(endpoint2)
    if r2.status_code in range(200,299):
        data2 = r2.json()

    poster_path=data["results"][0]["poster_path"]
    poster=f"https://image.tmdb.org/t/p/w500/{poster_path}" 
    similar=[]
    for i in range(len(data2["results"])):
        similar.append(data2["results"][i]["original_name"])

    similar="\n".join(similar)
    title=data["results"][0]["original_name"]

    embed=(hikari.Embed(
        title="SIMILAR TV-SHOWS",
        colour= hikari.Color(0xe5e5e5),
        timestamp=datetime.datetime.now().astimezone(),
        )
        .add_field(name=f"LIST OF TV-SHOWS LIKE {title.upper()}",value=similar)
        .set_footer(f"Requested by {ctx.member.display_name}",icon=ctx.member.avatar_url)
        .set_thumbnail(poster)

    )     

    await ctx.respond(embed)

    

def load(bot:lightbulb.BotApp):
    bot.add_plugin(plugin)

def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(plugin)