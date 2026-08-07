all_questions = [['Kalology', 'Study of beauty'], ['Vexillology', 'Study of flags'],
                 ['Ecophysiology', 'Study of the relationship between the physiology of organisms and their environment'],
                 ['Synecology', 'Study of ecological communities']]

possible_answers = []

for item in all_questions:
    # get the first item in each question/answer pair
    possible = item[0]

    # add the first thing in the pair (the 'ology') to the 'answers'
    possible_answers.append(possible)

print(possible_answers)

import random

print("before:", possible_answers)

answers = possible_answers

random.shuffle(possible_answers)
print(possible_answers)

random.shuffle(answers)
print("After shuffle : ")
print(answers)

random.shuffle(answers)
print("\nSecond shuffle : ")
print(answers)


string = "animal"

shuffled_string = "".join(random.sample(string, len(string)))

print(shuffled_string)