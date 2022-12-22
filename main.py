from functions import *

pick_game_prompt = """
Which game do you want to play?

1: Guess the user rating!

"""
pick_game_response = input(pick_game_prompt)
print('') # whitespace looks so much nicer but code looks so dumb ;-;

if pick_game_response == '1':
    guess_user_rating()
elif pick_game_response == '2':
    print("We don't have another game yet 4head -.-")
else:
    print("Invalid response.")