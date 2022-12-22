from functions import *

score = 0
print("working")

username = input("Which user do you want to quiz on? ")
user_df = produce_completed_df(username)
num_questions = int(input("How many questions do you want? "))
num_options = int(input("How many options do you want? "))

for i in range(num_questions):
    print("")
    if question(username, user_df, num_options) == True:
        score += 1
        
print(f'you got {score} out of {num_questions} correct')


