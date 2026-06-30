from tkinter import *
from functools import partial # To prevent unwanted windows



class StartGame:
    """
    Initial Game interface (asks users how many questions they want to answer
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
        choose_string = "How many question do you want to answer?"

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
                self.choose_label.config(text="How many questions do you want to answer?")

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
    Interface for playing the round
    """

    def __init__(self, how_many):
        self.questions_won = IntVar()

        # Lists for stats component

        # Highest Score Test Data...
        # self.all_scores_list = [20, 20, 20, 16, 19]
        # self.all_high_score_list = [20, 20, 20, 16, 19]
        # self.questions_won.set(5)

        # Lowest Score Test Data...
        # self.all_scores_list = [0, 0, 0, 0, 0]
        # self.all_high_score_list = [20 ,20, 20, 16, 19]
        # self.questions_won.set(0)

        # Random Score Test Data...
        self.all_scores_list = [0, 15, 16, 0, 16]
        self.all_high_score_list = [20, 19, 18, 20, 20]
        self.questions_won.set(3)

        self.play_box = Toplevel()

        self.game_frame = Frame(self.play_box)
        self.game_frame.grid(padx=10, pady=10)

        self.heading_label = Label(self.game_frame, text="Study of..? Quiz", font=("Arial", 16, "bold"),
                                   padx=5, pady=5)
        self.heading_label.grid(row=0)

        self.stats_button = Button(self.game_frame, font=("Arial", 14, "bold"),
                                   text="Stats", width=15, fg="#FFFFFF",
                                   bg="#FF8000", padx=10, pady=10, command=self.to_stats)
        self.stats_button.grid(row=1)

    def to_stats(self):
        """
        Retrieve everything we need to display the game / question statistics"""

        # IMPORTANT: retrieve number of questions
        # won as a number (rather than the self container)
        questions_won = self.questions_won.get()
        stats_bundle = [questions_won, self.all_scores_list,
                        self.all_high_score_list]

        Stats(self, stats_bundle)


class Stats:
    """
    Displays stats for the rounds
    """

    def __init__(self, partner, all_stats_info):

        self.stats_box = Toplevel()

        # disable help button
        partner.stats_button.config(state=DISABLED)

        # If users press cross at top, closes help and
        # 'releases' help button
        self.stats_box.protocol('WM_DELETE_WINDOW',
                                partial(self.close_stats, partner))

        self.stats_frame = Frame(self.stats_box, width=350)
        self.stats_frame.grid()


        self.dismiss_button = Button(self.stats_frame,
                                     font=("Arial", 16, "bold"),
                                     text="Dismiss", bg="#333333",
                                     fg="#FFFFFF", width=20,
                                     command=partial(self.close_stats,
                                                     partner))
        self.dismiss_button.grid(row=8, padx=10, pady=10)

        # closes help dialogue (used by button and x at the top of dialogue

    def close_stats(self, partner):
        partner.stats_button.config(state=NORMAL)
        self.stats_box.destroy()


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Colour Quest")
    StartGame()
    root.mainloop()

