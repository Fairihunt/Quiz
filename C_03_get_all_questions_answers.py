import csv
import random

# Retrieve colours from csv file and put them in a list
file = open("study_of.csv", "r")
all_questions = list(csv.reader(file, delimiter=","))
file.close()

# remove the first row
all_questions.pop(0)

round_questions = []

random_question = random.choice(all_questions)
print(random_question)
print(random_question[0])
print(random_question[1])
print(random_question[2])

