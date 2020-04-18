import boardgamegeek
import random
import urllib.parse 



bgg = boardgamegeek.BGGClient()
def make_game_url (bgg_game):
    try:
        bgg_type = bgg_game.type
    except:
        bgg_type = "bla bla"
    bgg_id = bgg_game.id
    link_url = "http://boardgamegeek.com/" + urllib.parse.quote("{}/{}".format(bgg_type, bgg_id))
    link_name = bgg_game.name
    return link_url


def game_lookup(string):
    '''Return description_text, title, image, url'''
    need_retry = False
    try:
        game = bgg.game(string, choose="first", exact=True)
    except boardgamegeek.BGGItemNotFoundError:
        need_retry = True
    except Exception as e:
        return("Unknown exception: "+str(e), "", "", "")
    if need_retry:
        try:
            game = bgg.game(string, choose="first", exact=False)
        except boardgamegeek.BGGItemNotFoundError:
            return("Game not found: {}".format(string), "", "", "")
        except Exception as e:
            return("Unknown exception: "+str(e), "", "", "")
    heart_count = int(game.rating_average)
    heart_emoji = '\U00002665'
    sad_heart_emoji = '\U00002661'
    heart_string = ""
    for x in range(0, 10):
        if x < 10-heart_count:
            heart_string += sad_heart_emoji
        else:
            heart_string += heart_emoji
    heart_string += " (" + str(int(game.rating_average)) + " / 10)"
    gameid = str(game.id)
    description = str(game.description.strip()[0:1000] + "...")
    gamerank = str(game.boardgame_rank)
    categories = game.categories
    number_of_players = str(game.min_players) + "-" + str(game.max_players)
    weight = str( round(game.rating_average_weight,2))
    categories_list = ', '.join(categories)
    description_text =('BoardGameGeek Id: ' +gameid
            + "\nGame Rating for " + str(string).capitalize() + " is: " + heart_string
            + "\nBoardGameGeek Rank: " + gamerank
            + "\nNumber of players: " + number_of_players
            + "\nCategories: " + categories_list
            + "\nComplexity Rank: " + weight + '/5'
            + "\nExpected game length: " +str(game.min_playing_time) + ' - ' + str(game.max_playing_time) + " minutes"
            + "\n\nDescription: " + description);
    return(description_text, game.name, str(game.image), make_game_url(game))

# def image_lookup(string):
    # try:
        # game = bgg.game(string,choose="first")
    # except Exception as e:
        # return( "error") 
    # return(str(game.image))

def game_expansion(string):
    try:
        game = bgg.game(string)
    except Exception as e:
            return( "Game not found, are you sure that's the correct title? Check for any possible errors.")   
    returned_string = "Here are the expansions for " + string + ":\n"
    expansion = game.expansions
    if not expansion:
            return("There are no expansions for " + str(game.name))
    for item in expansion:
        returned_string = returned_string + item.name + '\n'
    return returned_string


def user_lookup(name):
    try:
        user = bgg.collection(name)
    except Exception as e:
            return("User not found, are you sure that's the correct username? Check for any possible errors.")
    games_string = ""
    for item in user.items:
        if item.owned:
            games_string = games_string + item.name + '\n'
    return(games_string)


def random_owned_game(name):
        try:
                user = bgg.collection(name)
        except Exception as e:
                return("User not found, are you sure that's the correct username? Check for any possible errors.")
        games_list = []
        for item in user.items:
                if item.owned:
                        games_list.append(item.name)
        random_game = random.choice(games_list)
        return(random_game)

def what_games_can_we_play(name, numberofplayers = 1):
        try:
                user = bgg.collection(name)
        except Exception as e:
            return("User not found, are you sure that's the correct username? Check for any possible errors.")
        gamesString = ""
        for item in user.items:
                if item.owned:
                        if numberofplayers >= item.min_players and numberofplayers <= item.max_players:
                                gamesString =  gamesString + item.name + ' - Average Playtime:  ' + str(item.playing_time) + ' minutes ' + '\n\n'
        return("With "+ str(numberofplayers) + " players you can play these games from " + name + "'s collection \n\n" + gamesString)


def hot_games():
        hot_games_list = bgg.hot_items('boardgame')
        returned_string = "The current hot games are: \n\n"
        for item in hot_games_list:
                returned_string = returned_string + item.name + '\n'
        return returned_string

def hot_companies():
        hot_companies_list = bgg.hot_items('boardgamecompany')
        returned_string = "The current hot board game companies are: \n"
        for item in hot_companies_list:
                returned_string = returned_string + item.name + '\n'
        return returned_string

