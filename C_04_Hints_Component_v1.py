import csv
from tkinter import *
import random
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

    # loop until we have four colours...
    while len(question_answers) < 4:
        potential_question = random.choice(all_question_list)

        # colour scores are being read as a string,
        # change them to an integer to compare / when adding to score list
        if potential_question[1] not in question_answers:
            question_answers.append(potential_question)

    print("question_answers: ", question_answers)

    return question_answers



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

        # Create play button...
        self.play_button = Button(self.start_frame, font=("Arial", 16, "bold"),
                                  fg="#FFFFFF", bg="#9957D8", text="Hint", width=10,
                                  command=self.check_questions)
        self.play_button.grid(row=0, column=1, padx=20, pady=20)

    def check_questions(self):
        """
        Check users have entered 1 or more questions
        """

        # Retrieve temperature to be converted
        questions_wanted= 5
        self.to_play(questions_wanted)

    def to_play(self, num_questions):
        """
        Invokes Game GUI and takes across number of questions to be played
        """
        Play(num_questions)
        # Hide root window (ie:hide rounds choice window).
        root.withdraw()


class Play:

    """
    Interface for playing the Quiz Game
    """

    def __init__(self, how_many):
        self.hints_button = Button(font=("Arial", 14, "bold"),
                                   text="Hints", width=15, fg="#FFFFFF",
                                   bg="#FF8000", padx=10, pady=10, command=self.hints_button)
        self.hints_button.grid(row=1)

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

        # Retrieve Labels so they can be configured later
        self.heading_label = play_labels_ref[0]
        self.target_label = play_labels_ref[1]
        self.choose_label = play_labels_ref[2]
        self.results_label = play_labels_ref[2]

        # set up answer buttons...
        self.answer_frame = Frame(self.game_frame)
        self.answer_frame.grid(row=3)

        self.answer_button_ref = []
        self.button_colours_list = []

        # create four buttons in a 2 x 2 grid
        for item in range(0, 4):
            self.answer_button = Button(self.answer_frame, font=("Arial", 12),
                                        text="Answer Name", width=15,
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
                [self.game_frame, "End", "#990000", self.close_play, 21, 7, None],
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
            self.end_game_button = control_ref_list[2]

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
        print("questions wanted", questions_wanted)

        all_questions = get_question_answers()

        possible_answers = []

        for item in all_questions:
            # get the first item in each question/answer pair
            possible = item[0]

            # add the first thing in the pair (the 'ology') to the 'answers'
            possible_answers.append(possible)

        # Update heading to beat labels. Hide results label
        self.heading_label.config(text=f"Round {questions_played + 1} of {questions_wanted}")
        self.target_label.config(text=f"What's the {all_questions[0][1]}? \n\n"
                                      "Choose the answer below.")
        self.results_label.config(text=f"{'=' * 7}", bg="#F0F0F0")

        # Adding the answer labels into the button frames
        self.answer_button.config(text=f"{all_questions[0][0]}")

        print("study of...", self.round_study_of)
        print("all questions", all_questions)

        # configure buttons using foreground and background colours from list
        # enable colour buttons (disabled at the end of the last round)
        for count, item in enumerate(self.answer_button_ref):
            item.config(text=possible_answers[count], state=NORMAL)

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
        answer_name = self.answer_button_ref[user_choice].cget('text')

    # enable stats & next buttons, disable colour buttons
        self.next_button.config(state=NORMAL)

        # check to see if game is over
        questions_wanted = self.questions_wanted.get()

        # Code for when the game ends!
        if questions_played == questions_wanted:


            # work out success rate
            success_rate = questions_won / questions_played * 100
            success_string = (f"Success Rate: "
                              f"({questions_won} / {questions_played} "
                              f"({success_rate:.0f}%)")

            # Configure 'end game' labels /buttons
            self.heading_label.config(text="Game Over")
            self.target_label.config(text=success_string)
            self.choose_label.config(text="Please click the stats "
                                          "button for more info.")
            self.next_button.config(state=DISABLED, text="Game Over")
            self.end_game_button.config(text="Play Again", bg="#006600",
                                        compound="right", width=25)

        for item in self.answer_button_ref:
            item.config(state=DISABLED)

    def close_play(self):
        # reshow root (ie:choose questions) and end current
        # game / allow new game to start
        root.deiconify()
        self.play_box.destroy()

    def to_hints(self):
        """
        Display hints for playing game. Prevents users from accessing
        dialogues that could lead to the program crashing
        :return:
        """
        # checks we have played at least one round so that
        # stats button is not enabled in error.
        questions_played = self.questions_played.get()


    def hints_button(self):
        """
        Display hints for playing game
        :return:
        """
        DisplayHints(self)

class DisplayHints:
    """
    Disable two answers upon clicking on it.
    """

    def __init__(self, partner, rounds_played):
        # setup dialogue box and background colour
        self.rounds_played = rounds_played
        background = "#ffe6cc"
        self.help_box = Toplevel()

        # disable help, stats AND end game buttons to prevent users
        # from leaving a dialogue open and then going back to the rounds dialogue
        partner.hints_button.config(state=DISABLED)
        partner.end_game_button.config(state=DISABLED)
        partner.stats_button.config(state=DISABLED)

        # If users press cross at top, closes help and
        # 'releases' help button
        self.help_box.protocol('WM_DELETE_WINDOW',
                               partial(self.close_help, partner))

        self.help_frame = Frame(self.help_box, width=300,
                                height=200)

        self.help_frame.grid()

        self.help_heading_label = Label(self.help_frame,
                                        text="Help / Info",
                                        font=("Arial", 14, "bold"))
        self.help_heading_label.grid(row=0)

    # When triggered button, it would disable two incorrect answers for a 50-50 chance for the player.

    def close_help(self, partner):
        # Put help button back to normal...
        partner.hints_button.config(state=NORMAL)
        partner.end_game_button.config(state=NORMAL)
        partner.stats_button.config(state=NORMAL)

        self.help_box.destroy()


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Quiz")
    StartGame()
    root.mainloop()