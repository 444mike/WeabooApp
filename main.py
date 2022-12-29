from functions import *

pick_game_prompt = """
Which game do you want to play?

1: Guess the user rating!
2: Character guessing game
3: Write a dataframe to a file

"""
pick_game_response = input(pick_game_prompt)
print('') # whitespace looks so much nicer but code looks so dumb ;-;

if pick_game_response == '1':
    guess_user_rating_game()
elif pick_game_response == '2':
    character_guess_game()
elif pick_game_response == '3':
    write_df()
else:
    print("Invalid response.")