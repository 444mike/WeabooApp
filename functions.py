import random
import numpy
import pandas

def question(username, user_df, options):

    shows = {} # dictionary of shows
    num_options = options # however many options you want

    df_rows = user_df.shape[0] # gets all the rows

    while len(shows) < num_options: # while we have less shows than what the question requires

        randomNumber = random.randint(0, df_rows - 1) # generate a random int based on number of rows in dataframe
        show = user_df.iloc[randomNumber] # get a show's row based on random number generated
        title = show.get('media.title.english') # get title of said show
        score = show.get('score') # get score of said show
        if score not in shows.values():
            shows[title] = score # adds a key of title and a value of score to the dictionary of shows

    sorted_shows = sorted(shows.items(), key = lambda x: x[1], reverse = True) # sorts dict in descending order
    highest_rated = sorted_shows[0][0] # name of the highest rated show

    prompt = f"Which of these {num_options} shows did {username} rate the highest?\n"
    answer = None

    # for each index in shows, add the index and the name of the show to prompt, also check if the show is the correct answer
    for i in range(len(shows.keys())):
        show_name = list(shows.keys())[i] # reduces ugly formatting :p
        prompt += f'{i+1}. {show_name}\n'
        if show_name == highest_rated:
            answer = i + 1 # sets correct answer choice

    # user response with more newlines because it looks nicer
    prompt += '\n'
    response = int(input(f'{prompt}')) 
    print()

    if response == answer:
        print("naisuuuuuu")
        return True
    else:
        print("reatard")
        print("Highest scored show:", highest_rated)
        return False



def produce_completed_df(username):
    """
    Returns a DataFrame of the user's scored completed shows.
    ---
    Parameters:
    username: the username of the desired profile (str)
    """
    import pandas as pd
    import json
    from pandas import json_normalize
    import requests

    variables = {
        'username': username,
        'type': 'ANIME'
    }

    url = 'https://graphql.anilist.co'

    query = '''
query ($username: String, $type: MediaType) {
MediaListCollection(userName: $username, type: $type) {
    lists {
    name
    entries {
        id
        status
        score(format: POINT_10_DECIMAL)
        progress
        notes
        repeat
        media {
        chapters
        volumes
        idMal
        episodes
        title { english }
        }
    }
    name
    isCustomList
    isSplitCompletedList
    status
    }
}
}
'''

    # posts a request to the anilist graph ql
    response = requests.post(url, json={'query': query, 'variables': variables})
    jsonData = response.json()

    # checks if username is valid
    if username == '':
        raise NameError("Could not execute, username field left blank.")
    elif ('errors' in jsonData):
        raise NameError('Entered username may be invalid, or Anilist might be down.')

    # slams the shit into a dictionary based on type (0 = completed, 1 = planning, etc.)
    completed_entries = jsonData['data']['MediaListCollection']['lists'][0]['entries']
    df = json_normalize(completed_entries)
    scored_only = df[df.get('score') > 0]

    return scored_only