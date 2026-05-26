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

print("Wrong Answers...")

print()
print("Ology mode...")
for item in all_questions[1:]:
    print(item[0])

print()
print("Definition mode...")
for item in all_questions[1:]:
    print(item[1])





def round_ans(val):
    """
    Rounds numbers to nearest integer
    :param val: number to be rounded.
    :return: Rounded number (an integer)
    """
    var_rounded = (val * 2 +1) // 2
    raw_rounded = "{:.0f}".format(var_rounded)
    return int(raw_rounded)


# Classes start here


class StartGame:
    """
    Initial Game interface (asks users how many questions they
    would like to play
    """

    def __init__(self):
        """
        Gets number of questions from user
        """

        self.start_frame = Frame(padx=10, pady=10)
        self.start_frame.grid()

        # Strings for labels
        intro_string = ("This quiz will ask questions about the study of certain topics. "
                        "There is no goal but to improve your knowledge and revision on the "
                        "words of each topic. \n\n"
                        "Try your best and good luck!")

        # choose_string = "Oops - Please choose a whole number more than zero."
        choose_string = "How many questions do you want to answer?"

        # List of labels to be made (text | font | fg)
        start_labels_list = [
            ["Study of...? Quiz", ("Arial", 16, "bold"), None],
            [intro_string, ("Arial", 12), None],
            [choose_string, ("Arial", 12, "bold"), "#000000"]
        ]

        # Create labels and add them to the reference list

        start_label_ref = []
        for count, item in enumerate(start_labels_list):
            make_label = Label(self.start_frame, text=item[0], font=item[1],
                               fg=item[2],
                               wraplength=350, justify="left", pady=10, padx=20)
            make_label.grid(row=count)

            start_label_ref.append(make_label)

        # extract choice label so that it can be changed to an
        # error message if necessary
        self.choose_label = start_label_ref[2]

        # Frame so that the entry box and button can be in the same row.
        self.entry_area_frame = Frame(self.start_frame)
        self.entry_area_frame.grid(row=3)

        self.num_questions_entry = Entry(self.entry_area_frame, font=("Arial", 20, "bold"),
                                      width=10)
        self.num_questions_entry.grid(row=0, column=0, padx=10, pady=10)

        # Create play button...
        self.play_button = Button(self.entry_area_frame, font=("Arial", 16, "bold"),
                                  fg="#FFFFFF", bg="#000000", text="Play", width=15,
                                  command=self.check_questions)
        self.play_button.grid(row=1, column=0)

    def check_questions(self):
        """
        Check users have entered 1 or more questions
        """

        # Retrieve temperature to be converted
        questions_wanted = self.num_questions_entry.get()

        # Reset label and entry box (for when users come back to home screen)
        self.choose_label.config(fg="#009900", font=("Arial", 12, "bold"))
        self.num_questions_entry.config(bg="#FFFFFF")

        error = "Oops - Please choose a whole number more than zero"
        has_errors = "no"

        # checks that amount to be converted is a number above absolute zero
        try:
            questions_wanted = int(questions_wanted)
            if questions_wanted > 0:
                # Clear entry box and reset instruction label so
                # that when users play a new game, they don't see an error message.
                self.num_questions_entry.delete(0, END)
                self.choose_label.config(text="How many questions do you want to play?")

                # Invoke Play Class (and take across number of questions)
                Play(questions_wanted)
                # Hide root window (ie: hide questions choice window)
                root.withdraw()
            else:
                has_errors = "yes"

        except ValueError:
            has_errors = "yes"

        # display the error if necessary
        if has_errors == "yes":
            self.choose_label.config(text=error, fg="#990000",
                                     font=("Arial", 10, "bold"))
            self.num_questions_entry.config(bg="#F4CCCC")
            self.num_questions_entry.delete(0, END)


class Play:
    """
    Interface for doing the quiz
    """

    def __init__(self, how_many):

        # Integers / String Variables
        self.target_score = IntVar()

        # questions played - start with zero
        self.questions_played = IntVar()
        self.questions_played.set(0)

        self.questions_wanted = IntVar()
        self.questions_wanted.set(how_many)

        self.questions_won = IntVar()

        # Colour lists and score list
        self.round_study_of = []

        self.play_box = Toplevel()

        self.game_frame = Frame(self.play_box)
        self.game_frame.grid(padx=10, pady=10)

        # If users press the 'x' on the game window, end the entire game!
        self.play_box.protocol('WM_DELETE_WINDOW', root.destroy)

        # body font for most labels...
        body_font = ("Arial", 12)

        # List for label details (text | font | background | row
        play_labels_list = [
            ["Round # of #, #/# right", ("Arial", 16, "bold"), None, 0],
            ["Answer the question below. Good luck. 🍀", body_font, "#D5E8D4", 2],
            ["You chose, result", body_font, "#D5E8D4", 4],

        ]

        play_labels_ref = []
        for item in play_labels_list:
            print("item", item)
            self.make_label = Label(self.game_frame, text=item[0], font=item[1],
                                    bg=item[2], wraplength=300, justify="left")
            self.make_label.grid(row=item[3], pady=10, padx=10)

            play_labels_ref.append(self.make_label)




        # set up answer buttons...
        self.answer_frame = Frame(self.game_frame)
        self.answer_frame.grid(row=3)

        self.answer_button_ref = []
        self.button_colours_list = []

        # create four buttons in a 2 x 2 grid
        for item in range(0, 4):
            self.answer_button = Button(self.answer_frame, font=("Arial", 12),
                                        text="Placeholder", width=15,
                                        command=partial(self.question_results, item))
            self.answer_button.grid(row=item // 4,
                                    column=item % 4,
                                    padx=5, pady=5)




            self.answer_button_ref.append(self.answer_button)

            # Frame to hold hints and stats buttons
            self.hints_stats_frame = Frame(self.game_frame)
            self.hints_stats_frame.grid(row=6)

            # list for buttons (frame | text | bg | command | width | row | column)
            control_button_list = [
                [self.game_frame, "Next Round", "#B9BCCC", self.new_question, 20, 5, None],
                [self.hints_stats_frame, "Hints", "#D9CD94", self.to_hints, 15, 0, 0],
                [self.hints_stats_frame, "Stats", "#B5C7AA", self.to_stats, 15, 0, 1],
                [self.game_frame, "End", "#000000", self.close_play, 21, 7, None],
            ]

            # create buttons and add to list
            control_ref_list = []
            for item in control_button_list:
                make_control_button = Button(item[0], text=item[1], bg=item[2],
                                             command=item[3], font=("Arial", 16, "bold"),
                                             fg="#FFFFFF", width=item[4])
                make_control_button.grid(row=item[5], column=item[6], padx=5, pady=5)

                control_ref_list.append(make_control_button)

            # Retrieve next, stats and end button so that they can be configured
            self.next_button = control_ref_list[0]
            self.hints_button = control_ref_list[1]
            self.stats_button = control_ref_list[2]
            self.end_game_button = control_ref_list[3]


        # disable stats button at start so that users can't
        # generate stats if they have not played any rounds
        self.stats_button.config(state=DISABLED)

        # Once interface has been created, invoke new
        # round function for first round.



        self.new_question()

    def new_question(self):
        """
        Chooses four buttons, works out median for score to beat. Configures
        buttons with chosen colours
        """

        print("you pushed the next button")

        # retrieve number of questions played , add one to it and configure heading
        questions_played = self.questions_played.get()
        self.questions_played.set(questions_played)

        questions_wanted = self.questions_wanted.get()








    def close_play(self):
        # reshow root (ie:choose questions) and end current
        # game / allow new game to start
        root.deiconify()
        self.play_box.destroy()

        # configure buttons using foreground and background colours from list
        # enable colour buttons (disabled at the end of the last round)
        for count, item in enumerate(self.answer_button_ref):
            item.config(fg=self.round_study_of[count][2],
                        bg=self.round_study_of[count][0],
                        text=self.round_study_of[count][0], state=NORMAL)


        self.next_button.config(state=DISABLED)


    def question_results(self, user_choice):
        """
        Retrieves which button was pushed (index 0 - 3), retrieves
        score and then compares it with median, updates results and
        adds results to stats list.
        """


        # Add one to the number of rounds played and retrieve
        # the number of rounds won
        questions_played = self.questions_played.get()
        questions_played += 1
        self.questions_played.set(questions_played)

        questions_won = self.questions_won.get()

        # alternate way to get button name. Good for if buttons have been scrambled!
        colour_name = self.answer_button_ref[user_choice].cget('text')



        questions_won = self.questions_won.get()
        questions_won += 1
        self.questions_won.set(questions_won)




        # check to see if game is over
        questions_wanted = self.questions_wanted.get()

        # Code for when the game ends!
        if questions_played == questions_wanted:


            # work out success rate
            success_rate = questions_won / questions_played * 100
            success_string = (f"Success Rate: "
                              f"({questions_won} / {questions_played} "
                              f"({success_rate:.0f}%)")


        for item in self.answer_button_ref:
            item.config(state=NORMAL)



    def to_hints(self):
        """
        Display hints for playing game. Prevents users from accessing
        dialogues that could lead to the program crashing
        :return:
        """
        # checks we have played at least one round so that
        # stats button is not enabled in error.
        questions_played = self.questions_played.get()

    def to_stats(self):
        """
        Retrieves everything we need to display the game / round statistics"""

        # IMPORTANT: retrieve number of rounds
        # won as a number rather than the 'self' container
        questions_won = self.questions_won.get()
        questions_played = self.questions_played.get()



# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Quiz")
    StartGame()
    root.mainloop()
