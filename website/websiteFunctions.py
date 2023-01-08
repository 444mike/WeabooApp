import random
import numpy as np
import pandas as pd
import requests
import sys


# Function for the character guessing mechanics
def character_guess(filtered_df, num_options, favorites_threshold):
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

    titles = []
    characters = []
    for index in random_indices:
        row = filtered_df.iloc[index]
        title = row.get('title_eng')

        # adjusts favorites threshold if not enough characters available
        num_characters = len(row.get('characters'))
        if num_characters < favorites_threshold:
            favorites_threshold = num_characters
        try:
            character = row.get('characters')[np.random.randint(favorites_threshold)]
        except:
            print(row, row.get("characters"))
        titles.append(title)
        characters.append(character)
    
    # selects a random show as the correct answer
    selected_show_index = np.random.randint(num_options)
    selected_show_title = titles[selected_show_index]
    selected_show_character = characters[selected_show_index]

    prompt = f"Which of these {num_options} characters is from {selected_show_title}?\n"
    option_number = 1

    #print(characters)

    for character in characters:
        prompt += f"{option_number}: {character}\n"
        option_number += 1
    prompt += '\n'

    # commented this part out because i didnt want the response input -michael
    response = 1
    #response = int(input(prompt))

    if response == selected_show_index + 1:
        print("pog\n")
        #return True
    else:
        """
        print("Correct answer:", selected_show_character)
        print("selected show title: ", selected_show_title)
        print("titles: ", titles)
        print("characters: ", characters)
        print()
        #return False
        """

    return selected_show_title, characters, (selected_show_index + 1)

# Function for the character guessing game
def character_guess_game(username, num_questions, num_options, score_threshold, favorites_threshold): # which database, number options
    """username = "444mike"
    num_questions = 4
    num_options = 4
    score_threshold = 7
    favorites_threshold = 3"""
    
    """username = input("Which user do you want to quiz on? ")
    num_questions = int(input("How many questions do you want? "))
    num_options = int(input("How many options do you want? "))
    score_threshold = float(input("What do you want the minimum show rating to be? "))
    if score_threshold > 10: sys.exit("Choose a better number bozo ")
    favorites_threshold = int(input("How far down the favorites list do you wanna go? "))"""
    user_df = produce_completed_df(username)
    user_df_filtered = user_df[user_df.get('score') >= score_threshold]

    if user_df_filtered.shape[0] >= 90:
        raise ValueError("Must use less than 90 shows")

    stripped_user_df = user_df_filtered.get(["media.title.english", "media.idMal"])\
        .rename(columns = {"media.title.english": "title_eng", "media.idMal": "id_MAL"})\
        .reset_index().drop(columns = 'index')

    num_rows = stripped_user_df.shape[0]
    character_list_column = []

    for title in range(num_rows):
        row = stripped_user_df.iloc[title]
        id_MAL = int(row.get('id_MAL'))

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
        else:
            stripped_user_df.drop()
    #print(f"expected_rows: {num_rows}")
    #print(character_list_column)
    character_list_series = pd.Series(character_list_column)
    #print(character_list_series)
    final_df = stripped_user_df.reset_index().assign(characters = character_list_series)\
                               .drop(columns = 'index')
    #print(final_df)

    score = 0

    # this section is michael doing some unholy shit trying to piece this shit together
    titles = []
    characters = []
    correct_answers = []

    for i in range(num_questions):
        return_tuple = character_guess(final_df, num_options, favorites_threshold)
        titles += [return_tuple[0]]
        characters.append(return_tuple[1])
        correct_answers += [return_tuple[2]]
        """if character_guess(final_df, num_options, favorites_threshold) == True:
            score += 1"""
    
    """
    print(f"You got {score} out of {num_questions} right!")
    print("check in character_guess_game")
    print("titles:", titles)
    print("characters:", characters)
    print("correct answer:", correct_answers)
    """
    return titles, characters, correct_answers

        


    
    






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
        print("pog\n")
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

def write_df():
    username = input("Whose dataframe do you want? ")
    dataframe = produce_completed_df(username)
    dataframe = dataframe.to_string()
    with open("dataframe.txt", "w") as f:
        f.write(dataframe)

def check_score(correct_characters, answers, questions):
    score = 0
    for i in range(questions):
        if int(correct_characters[i]) == int(answers[i]):
            score += 1
    return score
