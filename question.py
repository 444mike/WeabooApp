from produce_completed_df import *
import random
import numpy
import pandas

notanom_df = produce_completed_df("notanom")

shows = {} # dictionary of shows
num_options = 4


df_rows = notanom_df.shape[0] # gets all the rows

while len(shows) < num_options: # while we have less shows than what the question requires

    randomNumber = random.randint(df_rows) # generate a random int based on number of rows in dataframe
    show = notanom_df.iloc[randomNumber] # get a show's row based on random number generated
    title = show.get('media.title.romaji') # get title of said show
    score = show.get('score') # get score of said show
    if score not in shows.values():
        shows[title] = score # adds a key of title and a value of score to the dictionary of shows

print(shows)


