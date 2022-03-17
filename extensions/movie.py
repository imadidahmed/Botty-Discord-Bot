import os

import datetime
import hikari
import lightbulb
import requests
import dotenv



plugin = lightbulb.Plugin("movie")
dotenv.load_dotenv()

base_url="https://api.themoviedb.org/3"
API_KEY=os.environ["MOVIE_API_KEY"]


@plugin.command()
@lightbulb.add_cooldown(5.0,3,lightbulb.UserBucket)
@lightbulb.command("movie","movie command that gonna help you a lot.",auto_defer=True)
@lightbulb.implements(lightbulb.PrefixCommandGroup,lightbulb.SlashCommandGroup)
async def movie(ctx: lightbulb.Context) -> None:
    ...

#search a movie
@movie.child
@lightbulb.add_cooldown(5.0,3,lightbulb.UserBucket)
@lightbulb.option("movie","movie you wanna search for.")
@lightbulb.command("search","Get details about a movie.",aliases=["src"])
@lightbulb.implements(lightbulb.PrefixSubCommand,lightbulb.SlashSubCommand)
async def search_movie(ctx: lightbulb.Context) -> None:
    #connection to api
    endpoint_path1="/search/movie"
    endpoint1=f"{base_url}{endpoint_path1}?api_key={API_KEY}&query={ctx.options.movie}"
    r1=requests.get(endpoint1)
    if r1.status_code in range(200,299):
        data= r1.json()
        mv_id=data["results"][0]['id']
    
    endpoint_path2=f"/movie/{mv_id}"
    endpoint2=f"{base_url}{endpoint_path2}?api_key={API_KEY}"
    r2=requests.get(endpoint2)
    if r2.status_code in range(200,299):
        data2=r2.json()

    endpoint_path3=f"/movie/{mv_id}/videos"
    endpoint3=f"{base_url}{endpoint_path3}?api_key={API_KEY}"
    r3=requests.get(endpoint3)
    if r3.status_code in range(200,299):
        data3=r3.json()
        video_key=data3["results"][0]["key"]
    
    #manipulate data
        title=data["results"][0]['title']
        overview=data["results"][0]['overview']
        release_date=data["results"][0]['release_date'][0:4]
        movie_id=data["results"][0]['id']
        poster_path=data["results"][0]['poster_path']
        image=f"https://image.tmdb.org/t/p/w500/{poster_path}"
        rating=data2["vote_average"]
        time=data2["runtime"]
        status=data2["status"]
        budget=data2["budget"]
        revenue=data2["revenue"]        
        genres=[]
        for i in range(len(data2["genres"])):
            genres.append(data2["genres"][i]["name"])
        genres='  '.join(genres)

        embed =(hikari.Embed(
            title=f"{title.upper()} ({release_date})",
            colour= hikari.Color(0xe5e5e5),
            timestamp=datetime.datetime.now().astimezone(),
            )
            .set_thumbnail(image)
            .add_field(name="OVERVIEW",value=overview)
            .add_field(name="GENRES", value=genres,inline=True)
            .add_field(name="RATING",value=f"{rating}",inline=True)
            .add_field(name="DURATION",value=f"{time} min",inline=True)
            .add_field(name="STATUS",value=status,inline=True)

            .set_footer(
                text=f"Requested by {ctx.member.display_name}",
                icon=ctx.member.avatar_url
            )
        )

        await ctx.respond(embed,reply=True,mentions_reply=True)

#watch the movie
@movie.child
@lightbulb.add_cooldown(5.0,3,lightbulb.UserBucket)
@lightbulb.option("movie"," Name of the movie you want to watch.")
@lightbulb.command("watch","watch a movie.",auto_defer=True,ephemeral=True)
@lightbulb.implements(lightbulb.PrefixSubCommand,lightbulb.SlashSubCommand)
async def search_movie(ctx: lightbulb.Context) -> None:
    #connection to api
    endpoint_path1="/search/movie"
    endpoint1=f"{base_url}{endpoint_path1}?api_key={API_KEY}&query={ctx.options.movie}"
    r1=requests.get(endpoint1)
    if r1.status_code in range(200,299):
        data= r1.json()
        
        title=data["results"][0]['title']
        movie_id=data["results"][0]['id']
        poster_path=data["results"][0]['poster_path']
        image=f"https://image.tmdb.org/t/p/w500/{poster_path}"
        movie=f"https://imdbembed.xyz/movie/tmdb/{movie_id}"

        embed2=(hikari.Embed(
            title=f"🎬 WATCH [{title.upper()}] NOW",
            url=movie,
            timestamp=datetime.datetime.now().astimezone(),
            colour=hikari.Color(0xe5e5e5),
            )
            .set_image(image)
            .set_footer(f"Requested by {ctx.member.display_name}",icon=ctx.member.avatar_url)
        )
        await ctx.respond(embed2)
    
#trending movies this week
@movie.child
@lightbulb.add_cooldown(5.0,3,lightbulb.UserBucket)
@lightbulb.command("trending","trending movies this week.")
@lightbulb.implements(lightbulb.PrefixSubCommand,lightbulb.SlashSubCommand)
async def trending_movies(ctx: lightbulb.Context) -> None:
    #connection to api
    endpoint_path="/trending/movie/week"
    endpoint=f"{base_url}{endpoint_path}?api_key={API_KEY}"
    r=requests.get(endpoint)
    if r.status_code in range(200,299):
        data=r.json()
        
        title="TRENDING MOVIES"
        poster_path=data["results"][0]['poster_path']
        thumbnail=f"https://image.tmdb.org/t/p/w500/{poster_path}"
        movies=[]
        for i in range(len(data["results"])):
            movies.append(data["results"][i]["title"])
        embedlist = '\n'.join(movies)
        
        embed=(hikari.Embed(
            title=title.upper(),
            colour=hikari.Color(0xe5e5e5),
            timestamp=datetime.datetime.now().astimezone(),
        )
        .set_thumbnail(thumbnail)
        .add_field(name="TRENDING MOVIES THIS WEEK",value=embedlist)
        .set_footer(
            text=f"Requested by {ctx.member.display_name}",
            icon=ctx.member.avatar_url
            )
        )
        await ctx.respond(embed)
        
#similar movies of a given movie
@movie.child
@lightbulb.add_cooldown(5.0,3,lightbulb.UserBucket)
@lightbulb.option("movie","The movie name.")
@lightbulb.command("similar","Get a list of similar movies.")
@lightbulb.implements(lightbulb.PrefixSubCommand,lightbulb.SlashSubCommand)
async def similar_movies(ctx: lightbulb.Context) -> None:
    #connection to api
    endpoint_path1="/search/movie"
    endpoint1=f"{base_url}{endpoint_path1}?api_key={API_KEY}&query={ctx.options.movie}"
    r1=requests.get(endpoint1)
    if r1.status_code in range(200,299):
        data1= r1.json()
        mv_id=data1["results"][0]['id']
    
    endpoint_path=f"/movie/{mv_id}/similar"
    endpoint=f"{base_url}{endpoint_path}?api_key={API_KEY}"
    r=requests.get(endpoint)
    if r.status_code in range(200,299):
        data=r.json()
        
        poster_path=data1["results"][0]['poster_path']
        image=f"https://image.tmdb.org/t/p/w500/{poster_path}"
        similar_movies=[]
        for i in range(len(data["results"])):
            similar_movies.append(data["results"][i]["title"])
        embedlist = '\n'.join(similar_movies)
        title=data1["results"][0]["original_title"]
        
        embed=(hikari.Embed(
            title="SIMILAR MOVIES",
            colour=hikari.Color(0xe5e5e5),
            timestamp=datetime.datetime.now().astimezone(),
        )
        .add_field(name=f"A LIST OF SIMILAR MOVIES LIKE {title.upper()}:",value=embedlist)
        .set_thumbnail(image)
        .set_footer(
            text=f"Requested by {ctx.member.display_name}",
            icon=ctx.member.avatar_url
            )
        )
        await ctx.respond(embed)
     
#popular movie at the moment
@movie.child
@lightbulb.add_cooldown(5.0,3,lightbulb.UserBucket)
@lightbulb.command("popular","Get a list of the current popular movies.")
@lightbulb.implements(lightbulb.PrefixSubCommand,lightbulb.SlashSubCommand)
async def popular_movies(ctx:lightbulb.Context) -> None:
    endpoint_path= "/movie/popular"
    endpoint=f"{base_url}{endpoint_path}?api_key={API_KEY}"
    r=requests.get(endpoint)
    if r.status_code in range(200,299):
        data=r.json()
    
    poster_path=data["results"][0]['poster_path']
    image=f"https://image.tmdb.org/t/p/w500/{poster_path}"
    popular_movies=[]
    for i in range(len(data["results"])):
        popular_movies.append(data["results"][i]["title"])
    popular_movies="\n".join(popular_movies)

    embed=(hikari.Embed(
        title="POPULAR MOVIES",
        colour=hikari.Color(0xe5e5e5),
        timestamp=datetime.datetime.now().astimezone()
        )
    .add_field(
        name="A LIST OF POPULAR MOVIES",
        value=popular_movies
        )
    .set_thumbnail(image)
    .set_footer(
        text=f"Requested by {ctx.member.display_name}",
        icon=ctx.member.avatar_url
        )
    )
    await ctx.respond(embed)


@movie.child
@lightbulb.add_cooldown(5.0,3,lightbulb.UserBucket)
@lightbulb.option("movie","The movie name.")
@lightbulb.command("recommendation","Get a list of recommended movies for a movie.")
@lightbulb.implements(lightbulb.PrefixSubCommand,lightbulb.SlashSubCommand)
async def similar_movies(ctx: lightbulb.Context) -> None:
    #connection to api
    endpoint_path1="/search/movie"
    endpoint1=f"{base_url}{endpoint_path1}?api_key={API_KEY}&query={ctx.options.movie}"
    r1=requests.get(endpoint1)
    if r1.status_code in range(200,299):
        data1= r1.json()
        mv_id=data1["results"][0]['id']
    
    endpoint_path=f"/movie/{mv_id}/recommendations"
    endpoint=f"{base_url}{endpoint_path}?api_key={API_KEY}"
    r=requests.get(endpoint)
    if r.status_code in range(200,299):
        data=r.json()
        
        poster_path=data1["results"][0]['poster_path']
        image=f"https://image.tmdb.org/t/p/w500/{poster_path}"
        recs_movies=[]
        for i in range(len(data["results"])):
            recs_movies.append(data["results"][i]["title"])
        embedlist = '\n'.join(recs_movies)
        title=data1["results"][0]["original_title"]
        
        embed=(hikari.Embed(
            title="movie recommendations".upper(),
            colour=hikari.Color(0xe5e5e5),
            timestamp=datetime.datetime.now().astimezone(),
        )
        .add_field(name=f"A LIST OF {title.upper()} RECOMMENDATIONS:",value=embedlist)
        .set_thumbnail(image)
        .set_footer(
            text=f"Requested by {ctx.member.display_name}",
            icon=ctx.member.avatar_url
            )
        )
        await ctx.respond(embed)

def load(bot:lightbulb.BotApp):
    bot.add_plugin(plugin)

def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(plugin)