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
