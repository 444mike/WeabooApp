from functions import *

pick_game_prompt = """
Which game do you want to play?

1: Guess the user rating!
2: Character guessing game
3: Loop testing on character guessing game

"""
pick_game_response = input(pick_game_prompt)
print('') # whitespace looks so much nicer but code looks so dumb ;-;

if pick_game_response == '1':
    guess_user_rating_game()
elif pick_game_response == '2':
    character_guess_game()
elif pick_game_response == '3':
    user_df = produce_completed_df("notanom")
    stripped_user_df = user_df.get(["media.idMal", "media.title.english", "media.title.romaji"]).rename\
    (columns = {"media.idMal": "idMal", "media.title.english": "english title", "media.title.romaji": "romaji title"})
    for i in range(100):
        try:
            character_guess(stripped_user_df, 3)
        except: 
            break

else:
    print("Invalid response.")