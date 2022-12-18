import random
import numpy
import pandas

def question(username, options):
    df = produce_completed_df(username)

    shows = {} # dictionary of shows
    num_options = options # however many options you want

    df_rows = df.shape[0] # gets all the rows

    while len(shows) < num_options: # while we have less shows than what the question requires

        randomNumber = random.randint(0, df_rows) # generate a random int based on number of rows in dataframe
        show = df.iloc[randomNumber] # get a show's row based on random number generated
        title = show.get('media.title.romaji') # get title of said show
        score = show.get('score') # get score of said show
        if score not in shows.values():
            shows[title] = score # adds a key of title and a value of score to the dictionary of shows

    max_value = max(shows.values())
    correct_answer = max(shows, key=shows.get) # name of highest rated show

    prompt = "Which one of these shows is scored the highest?\n"
    answer = None

    # for each index in shows, add the index and the name of the show to prompt, also check if the show is the correct answer
    for i in range(len(shows.keys())):
        prompt += f'{i+1}. {list(shows.keys())[i]}\n'
        if list(shows.keys())[i] == correct_answer:
            answer = i

    # user response
    response = int(input(f'{prompt}'))

    if response - 1 == answer:
        print("naisuuuuuu")
        return True
    else:
        print("reatard")
        print("Highest scored show:", correct_answer)
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
        title { romaji }
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
    # slams the shit into a dictionary based on type (0 = completed, 1 = planning, etc.)
    completed_entries = jsonData['data']['MediaListCollection']['lists'][0]['entries']
    df = json_normalize(completed_entries)
    scored_only = df[df.get('score') > 0]

    return scored_only






