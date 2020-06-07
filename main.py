# Work with Python 3.6
import asyncio
import datetime
import os
import random
import typing
import logging
import discord.message
import Python.BGG
import Python.data_storage
import Python.Dice
import Python.YouTube
import util.database_initialization
from util.config import TOKEN
from discord.ext import commands

#from util.config import DEVELOPER_KEY

# if not os.path.isfile('boardgamebot.db'):
#     util.database_initialization.intitialize_db()

# sentry_sdk.init(sentry_url)

lf=open("log.txt", mode='w', encoding='utf_8')
logging.basicConfig(stream=lf, level=logging.DEBUG)

logger = logging.Logger('catch_all')
new_line = '\n'

def get_prefix(client, message):
    Bot_Prefix = ['==', '=']
    return commands.when_mentioned_or(*Bot_Prefix)(client, message)

#players = {}

client = commands.Bot(command_prefix=get_prefix, help_command=None, case_insensitive=True)
#client.remove_command('help')


@client.command(name='BoardGameGeek Lookup',
                description="Returns the BGG information on a game",
                brief="Shows the BoardGameGeek information of the specified game",
                usage="<game name>",
                aliases=['bggck', 'bglookup', 'bg', 'bgg']
                )
async def bgg_check(ctx, *, gamename):
    (main_response, title_text, image_url, link_url) = Python.BGG.game_lookup(gamename)
    if title_text:
        game_embed = discord.Embed()
        game_embed.title = title_text
        if image_url:
            game_embed.set_image(url=image_url)
        if link_url:
            game_embed.url = link_url
        game_embed.colour = discord.Colour.from_rgb(255, 0, 96)
        game_embed.description = main_response
        await ctx.send(embed=game_embed)
    else:
        # there was an error
        await ctx.send(main_response)

@bgg_check.error
async def bgg_check_error(ctx, error):
    if isinstance(error, BaseException):
        await ctx.send('Unexpected error, try again. If the error persists,'
                       ' get help here https://discord.gg/9pS2JdC')
        logger.error(error, exc_info=True)


@client.command(name='Expansion Check',
                description="Returns expansions for the selected game if any",
                brief="Returns expansions of a game",
                usage="=command <game name>",
                aliases=['exp', 'expchk', 'expansion']
                )
async def expansion_check(ctx, *, game):
    main_response = Python.BGG.game_expansion(game)
    await ctx.send(main_response)

@expansion_check.error
async def expansion_check_error(ctx, error):
    if isinstance(error, BaseException):
        await ctx.send('Unexpected error, try again. If the error persists,'
                       ' get help here https://discord.gg/9pS2JdC')
        logger.error(error, exc_info=True)


@client.command(name='Random Game',
                description="Returns a random game title from a provided list",
                brief="Returns a random title from a provided list of games",
                usage="<game 1>, <game 2>, <game 3>, ...",
                aliases=['randompick', 'randbg', 'rbg']
                )
async def random_game(ctx, *, arg):
    possible_responses = arg.split(',')
    await ctx.send(random.choice(possible_responses))

@random_game.error
async def random_game_error(ctx, error):
    if isinstance(error, BaseException):
        await ctx.send('Unexpected error, try again. If the error persists,'
                       ' get help here https://discord.gg/9pS2JdC')
        logger.error(error, exc_info=True)


@client.command(name='Random Owned Game',
                description="Returns a random game title from a user's owned list",
                brief="Random game from users BGG owned list",
                usage="<bgg username>",
                aliases=['randomownedpick', 'randobg', 'robg']
                )
async def random_users_game(ctx, name):
    random_game_name = Python.BGG.random_owned_game(name)
    await ctx.send(random_game_name)

@random_users_game.error
async def random_users_game_error(ctx, error):
    if isinstance(error, BaseException):
        await ctx.send('Unexpected error, try again. If the error persists,'
                       ' get help here https://discord.gg/9pS2JdC')
        logger.error(error, exc_info=True)

@client.command(name='What Can We Play',
                description="Looks up a user's collection and how many people are playing to see what games you could play",
                brief="Looks up a user's collection and how many people are playing to see what games you could play",
                usage="<bgg username> <number of players>",
                aliases=['wgcwp', 'wcwp', 'whatcanweplay']
                )
async def what_game_can_we_play(ctx, *, arg):
    user_input = arg.split(' ')
    name = user_input[0]
    number_of_players = int(user_input[1])
    games_we_can_play = Python.BGG.what_games_can_we_play(name, number_of_players)
    start = 0
    for pos in range(0, len(games_we_can_play), 1500):
        for le in range(pos, pos + 1500):
            i = games_we_can_play.find("\n", le)
            list = games_we_can_play[start:i]
        start = i + 1
        await ctx.send(list)   # + '\n' +str(i) + '\n' +str(start)

@what_game_can_we_play.error
async def what_game_can_we_play_error(ctx, error):
    if isinstance(error, BaseException):
        await ctx.send('Unexpected error, try again. If the error persists,'
                       ' get help here https://discord.gg/9pS2JdC')
        logger.error(error, exc_info=True)

@client.command(name='How To Play',
                description="Returns the top search result video from YouTube on how to play",
                brief="How to play video",
                usage="<game name>",
                aliases=['htp', 'how', 'video']
                )
async def youtube_how_to(ctx, *, game_name):
    main_response = Python.YouTube.how_to_play(game_name)
    await ctx.send(main_response)

@youtube_how_to.error
async def youtube_how_to_error(ctx, error):
    if isinstance(error, BaseException):
        await ctx.send('Unexpected error, try again. If the error persists,'
                       ' get help here https://discord.gg/9pS2JdC')
        logger.error(error, exc_info=True)

@client.command(name='Get Hot Games',
                description="Returns BoardGameGeeks current hot games",
                brief="Returns BoardGameGeeks current hot games",
                usage="",
                aliases=['ghg', 'hot', 'hotgames']
                )
async def get_hot_games(ctx):
    response = Python.BGG.hot_games()
    await ctx.send(response)

@get_hot_games.error
async def get_hot_games_error(ctx, error):
    if isinstance(error, BaseException):
        await ctx.send('Unexpected error, try again. If the error persists,'
                       ' get help here https://discord.gg/9pS2JdC')
        logger.error(error, exc_info=True)


@client.command(name='Get Hot Companies',
                description="Returns BoardGameGeeks current hot board game companies",
                brief="Returns BoardGameGeeks current hot board game companies",
                usage="",
                aliases=['ghc', 'hotcompanies']
                )
async def get_hot_companies(ctx):
    response = Python.BGG.hot_companies()
    await ctx.send(response)

@get_hot_companies.error
async def get_hot_companies_error(ctx, error):
    if isinstance(error, BaseException):
        await ctx.send('Unexpected error, try again. If the error persists,'
                       ' get help here https://discord.gg/9pS2JdC')
        logger.error(error, exc_info=True)

@client.command(name='Lookup BGG User',
                description='Looks up the BoardGameGeek list of owned game for the specified username',
                brief="lookup bgg username owned games list",
                usage="<username>",
                aliases=['gamesowned', 'lookup-games', 'go']
                )
async def lookup_bgg_user(ctx, name):
    response = Python.BGG.user_lookup(name)
    start = 0
    await ctx.send("Games that " + str(name).capitalize() + " owns: \n\n")
    for pos in range(0,len(response), 1500):
        for le in range(pos, pos+1500):
            i = response.find("\n", le)
            list = response[start:i]
        start = i+1
        await ctx.send(list)

@lookup_bgg_user.error
async def lookup_bgg_user_error(ctx, error):
    if isinstance(error, BaseException):
        await ctx.send('Unexpected error, try again. If the error persists,'
                       ' get help here https://discord.gg/9pS2JdC')
        logger.error(error, exc_info=True)

@client.command(name="Dice Roll",
                description="Returns the value of a single die with user specified number of sides",
                brief="Returns the value of a D<num> die roll",
                usage="<# of sides>",
                aliases=['dice', 'roll']
                )
async def dice_roll(ctx, sides):
    dice_roll = Python.Dice.dice(int(sides))
    await ctx.send("The " + str(sides) + " sided die resulted in: " + str(dice_roll))

@dice_roll.error
async def dice_roll_error(ctx, error):
    if isinstance(error, BaseException):
        await ctx.send('Unexpected error, try again. If the error persists,'
                       ' get help here https://discord.gg/9pS2JdC')
        logger.error(error, exc_info=True)


@client.command(name='Game Ambiance',
                description="Returns the top YouTube search result for search of 'ambiance + <gamename>' ",
                brief="Ambiance video for specified game",
                usage="<gamename>",
                aliases=['amb', 'ambiance']
                )
async def game_ambiance_playlist(ctx, *, topic):
    main_response = Python.YouTube.game_ambiance(topic)
    await ctx.send("Here's the result for " + topic +
                   " ambiance \n" + main_response)

@game_ambiance_playlist.error
async def game_ambiance_playlist_error(ctx, error):
    if isinstance(error, BaseException):
        await ctx.send('Unexpected error, try again. If the error persists,'
                       ' get help here https://discord.gg/9pS2JdC')
        logger.error(error, exc_info=True)

@client.command(name='Next Video',
                description="Gives the next video in the list of results from the most recent youtube search done in "
                            "discord chat",
                brief="Next video in list from most recent search",
                usage="",
                aliases=['nextvid', 'nxt', 'nvideo']
                )
async def next_video(ctx):
    response = Python.YouTube.search_next_video()
    await ctx.send("Next video: \n" + response)

@next_video.error
async def next_video_error(ctx, error):
    if isinstance(error, BaseException):
        await ctx.send('Unexpected error, try again. If the error persists,'
                       ' get help here https://discord.gg/9pS2JdC')
        logger.error(error, exc_info=True)

@client.command(name='Help',
                description='Bot purpose, and list of commands',
                brief='Help info',
                usage="<blank> or <command>",
                aliases=['hlp', 'H', '?']
                )
async def help(ctx, *, cmd=None):
        """Gives you info on bot's Commands."""
        if not cmd:
            halp = discord.Embed(title="Marvin",
                                 description="The Depressed Robot"
                                             "\n Here is a list of things I can do, but I wont be happy about:"
                                             "\n To use a command use '=command' ",
                                 color=0x6300D2)
            for x in client.commands:
                halp.add_field(name=x.name, value=f'{x.name}. {new_line} To use ={x.aliases} {x.usage} {new_line} {x.brief}', inline=False)
            halp.set_footer(text='For more detailed information about a command use =help <command>')
        else:
            halp = discord.Embed(title=f'{str(cmd)} Command Listing')
            for x in client.commands:
                y = str(cmd).casefold()
                if str(cmd).casefold() == str(x.name).casefold() or y in x.aliases:
                    halp.add_field(name=x.name, value=f'{x.name}{new_line} To use ={x.aliases} {x.usage}{new_line}{x.description}', inline=False)
        await ctx.send(embed=halp)


@client.event
async def on_ready():
    #for guild in client.guilds:
        # for channel in guild.channels:
        #     if str(channel.type) == 'text' and str(channel.name) == 'general':
        #         message = client.get_guild(guild.id).get_channel(channel.id)
        #         await message.send('Life? Dont talk to me about Life')
    print('Ready!')

async def list_servers():
    await client.wait_until_ready()
    while not client.is_closed():
        print("Current servers:")
        for guild in client.guilds:
            print(f'{guild.name} \nID: {guild.id}')
        await client.change_presence(activity=discord.Game(name=Python.BGG.random_owned_game("myersvx")))
        await asyncio.sleep(600)




client.loop.create_task(list_servers())
client.run(TOKEN)
