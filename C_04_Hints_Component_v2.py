from tkinter import *
from functools import partial
# To prevent unwanted windows


class StartGame:
    """
    Initial Game interface (asks users how many rounds they
    would like to play)
    """

    def __init__(self):
        """
        Gets number of rounds from user
        """

        self.start_frame = Frame(padx=10, pady=10)
        self.start_frame.grid()

        # Create play button...
        self.play_button = Button(self.start_frame, font=("Arial", 16, "bold"),
                                  fg="#FFFFFF", bg="#0057D8", text="Play", width=10,
                                  command=self.check_rounds)
        self.play_button.grid(row=0, column=1, padx=20, pady=20)

    def check_rounds(self):
        """
        Checks users have entered 1 or more rounds
        """

        # Retrieve temperature to be converted
        rounds_wanted = 5
        self.to_play(rounds_wanted)

    def to_play(self, num_rounds):
        """
        Invokes Game GUI and takes across number of questions to be played.
        """
        Play(num_rounds)
        # Hide root window (ie:hide rounds choice window).
        root.withdraw()


class Play:
    """
    Interface for playing the quiz
    """

    def __init__ (self, how_many):
        # Integers / String Variables
        self.target_score = IntVar()

        # questions played - start with zero
        self.questions_played = IntVar()
        self.questions_played.set(0)

        self.questions_wanted = IntVar()
        self.questions_wanted.set(how_many)

        self.questions_won = IntVar()

        self.correct_ans = StringVar()

        # Study of list
        self.round_study_of = []

        self.play_box = Toplevel()

        self.game_frame = Frame(self.play_box)
        self.game_frame.grid(padx=10, pady=10)

        # If users press the 'x' on the game window, end the entire game!
        self.play_box.protocol('WM_DELETE_WINDOW', root.destroy)


        self.heading_label = Label(self.game_frame, text="Study of...? Quiz", font=("Arial", 16, "bold"),
                                   padx=5, pady=5)
        self.heading_label.grid(row=0)

        self.hints_button = Button(self.game_frame, font=("Arial", 14, "bold"),
                                   text="Hints", width=15, fg="#FFFFFF",
                                   bg="#FF8000", padx=10, pady=10, command=self.hints_button)
        self.hints_button.grid(row=1)

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

        that_answer = self.correct_ans.get()

    def hints_button(self):
        """
        Display hints for playing game
        :return:
        """
        DisplayHints(self)



class DisplayHints:
    """
    Displays hints for the quiz
    """


    def __init__(self, partner, answer_name):
        # setup dialogue box and background colour
        background = "#ffe6cc"
        self.help_box = Toplevel()

        # disable help button
        partner.hints_button.config(state=DISABLED)

        # If users press cross at top, closes help and
        # 'releases' help button
        self.help_box.protocol('WM_DELETE_WINDOW',
                               partial(self.close_help, partner))

        self.help_frame = Frame(self.help_box, width=300,
                                height=200)

        self.help_frame.grid()

        self.help_heading_label = Label(self.help_frame,
                                        text="Help",
                                        font=("Arial", 14, "bold"))
        self.help_heading_label.grid(row=0)

        help_text = (f"The answer is {answer_name}")

        self.help_text_label = Label(self.help_frame,
                                     text=help_text, wraplength=350,
                                     justify="left")
        self.help_text_label.grid(row=1, padx=10)

        self.dismiss_button = Button(self.help_frame,
                                     font=("Arial", 12, "bold"),
                                     text="Dismiss", bg="#CC6600",
                                     fg="#FFFFFF",
                                     command=partial(self.close_help, partner))
        self.dismiss_button.grid(row=2, padx=10, pady=10)

        # List and loop to set background colour on
        # everything except the buttons

        recolour_list = [self.help_frame, self.help_heading_label,
                         self.help_text_label]

        for item in recolour_list:
            item.config(bg=background)

    def close_help(self, partner):
        """
        Close help dialogue box (and enables help button)
        """
        # Put help button back to normal...
        partner.hints_button.config(state=NORMAL)
        self.help_box.destroy()



# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Quiz")
    StartGame()
    root.mainloop()