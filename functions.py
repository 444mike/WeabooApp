import random
import numpy as np
import pandas
import requests

# Function for the character guessing mechanics
def character_guess(filtered_df, num_options, favorites_threshold = 2):
    """
    Outputs a question in which the user determines which listed character 
    belongs to a randomly selected show.
    ---
    Parameters:
    filtered_df: a DataFrame with two columns, those being 'idMal' (integer ids 
    corresponding to MAL listings) and 'title' (titles of each show, in english, 
    as strings)
    num_options: the number of answer choices to be provided (int)
    favorites_threshold: the maximum distance a selected character can be from 
    the top of a show's favorites list, defaulted to three (i.e. only the top 
    three most-favorited characters from each show may be selected)
    """
    # pulls [num_options] amount of randomly selected shows
    df_rows = filtered_df.shape[0]
    random_indices = np.random.randint(df_rows, size = num_options)

    shows = []
    for index in random_indices:
        show = dict(filtered_df.iloc[index]) # converts selected row to dictionary
        shows.append(show)

    
    # pulls a highly-favorited character from each show as an answer option
    characters = []
    for show in shows:
        # GraphQL query to pull each character
        query= """
query Query($sort: [CharacterSort], $search: String) {
  Media(search: $search) {
    characters(sort: $sort) {
      nodes {
        name {
          full
        }
      }
    }
  }
}
"""
        variables = {"search": show["romaji title"], "sort": "FAVOURITES_DESC"}
        url = 'https://graphql.anilist.co'

        response = requests.post(url, json={'query': query, 'variables': variables})
        print()


        jsonData = response.json()

        # strips json file to only character nodes
        character_list = jsonData['data']['Media']['characters']['nodes']
        
        show_characters = []
        if len(character_list) == 0:
            variables = {"search": show["english title"], "sort": "FAVOURITES_DESC"}
            response = requests.post(url, json={'query': query, 'variables': variables})

            jsonData = response.json()

            # strips json file to only character nodes
            character_list = jsonData['data']['Media']['characters']['nodes']

        print()
        print(show["romaji title"], character_list, '\n"')
        for i in range(favorites_threshold):
            show_characters.append(character_list[i]['name']['full'])
        
        selected_character = show_characters[np.random.randint(favorites_threshold)]
        characters.append(selected_character)

    # selects a random show as the correct answer
    selected_show_index = np.random.randint(num_options)
    selected_show = shows[selected_show_index]

    prompt = f"Which of these {num_options} characters is from {selected_show['english title']}?\n"
    option_number = 1

    for character in characters:
        prompt += f"{option_number}: {character}\n"
        option_number += 1
    prompt += '\n'

    response = 1 # int(input(prompt))

    if response == selected_show_index + 1:
        print("pog")
        return True
    else:
        print("pepesadge")
        print("Correct answer:", characters[selected_show_index])
        return False

# Function for the character guessing game
def character_guess_game(): # which database, number options
    username = input("Which user do you want to quiz on? ")
    score_threshold = input("What do you want the minimum show rating to be?")
    favorites_threshold = int(input("How far down the favorites list do you wanna go?"))
    user_df = produce_completed_df(username)
    user_df_filtered = user_df[user_df.get('score') >= score_threshold]

    if user_df_filtered.shape[0] >= 90:
        raise ValueError("Must use less than 90 shows")

    stripped_user_df = user_df_filtered.get(["media.title.english", "media.idMal"])\
        .rename(columns = {"media.title.english": "title_eng", "media.idMal": "id_MAL"})

    num_rows = stripped_user_df.shape[0]
    character_list_column = []

    for title in range(num_rows):
        row = stripped_user_df.iloc[title]
        id_MAL = int(row[1])

        query= """
query Query($idMal: Int, $type: MediaType, $sort: [CharacterSort]) {
Media(idMal: $idMal, type: $type) {
title {
    english
    romaji
}
characters(sort: $sort) {
    nodes {
    name {
        full
    }
    }
}
}
}
"""
        variables = {"idMal": id_MAL, "type": "ANIME", "sort": "FAVOURITES_DESC"}
        url = 'https://graphql.anilist.co'

        response = requests.post(url, json={'query': query, 'variables': variables})
        try:
            jsonData = response.json()
        except Exception as e:
            print(f"title: {row[0]}, error: {e}")
            print(f"response: {response}")
            print(f"json: {jsonData}")

        # strips json file to only character nodes
        try:
            character_list = jsonData['data']['Media']['characters']['nodes']
        except:
            print(f"title: {title}")
            print(f"json: {jsonData}")

        if len(character_list) >= favorites_threshold:
            threshold_characters = []
            for character in range(favorites_threshold):
                name_only = character_list[character]['name']['full']
                threshold_characters.append(name_only)
            character_list_column.append(threshold_characters)
    print(f"expected_rows: {num_rows}")
    return character_list_column
    






def guess_user_rating(username, user_df, options):

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
        print("pog")
        return True
    else:
        print("pepesadge")
        print("Highest scored show:", highest_rated)
        return False


def guess_user_rating_game():
    score = 0

    username = input("Which user do you want to quiz on? ")
    user_df = produce_completed_df(username) # takes df only once for efficiency
    num_questions = int(input("How many questions do you want? "))
    num_options = int(input("How many options do you want? "))

    for i in range(num_questions):
        print("")
        if guess_user_rating(username, user_df, num_options) == True:
            score += 1
    
    print(f'you got {score} out of {num_questions} correct')


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
        title { english romaji }
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

    # posts a request to the Anilist GraphQL
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