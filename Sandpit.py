import csv
import random
from tkinter import *
from functools import partial # To prevent unwanted windows



def get_questions():
    """
    Retrieves answers from csv file
    :return: list of questions which where each list item has the
    question, answer and foreground colour for the text
    """

    file = open("study_of.csv", "r")
    all_questions = list(csv.reader(file, delimiter=","))
    file.close()

    # remove the first row
    all_questions.pop(0)


    return all_questions

def get_question_answers():
    """
    Choose four answers from larger list ensuring that the answers are different
    :return: list of answers
    """

    all_question_list = get_questions()

    question_answers = []

    # loop until we have four colours with different scores...
    while len(question_answers) < 4:
        potential_question = random.choice(all_question_list)

        # colour scores are being read as a string,
        # change them to an integer to compare / when adding to score list
        if potential_question[1] not in question_answers:
            question_answers.append(potential_question)

    print("question_answers: ", question_answers)

    return question_answers

all_questions = get_question_answers()

print("=== Question and right answer ===")

print(all_questions[0][0])
print(all_questions[0][1])

print("Wrong Answers...")

print()
print("Ology mode...")
for item in all_questions[1:]:
    print(item[0])

print()
print("Definition mode...")
for item in all_questions[1:]:
    print(item[1])
