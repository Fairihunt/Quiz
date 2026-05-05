from tkinter import *
from functools import partial # To prevent unwanted windows


class StartGame:
    """
    Initial Game Interface (asks users how many questions
    they would like to answer
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
        choose_string = "How many questions would you like to answer?"

        # List of labels to be made (text | font | fg)
        start_labels_list = [
            ["Study of...?", ("Arial", 16, "bold"), None],
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
                                  fg="#FFFFFF", bg="#000000", text="Play", width=10,
                                  command=self.check_questions)
        self.play_button.grid(row=0, column=1)

    def check_questions(self):
        """
        Checks users have entered 1 or more questions
        """

        # Retrieve temperature to be converted
        questions_wanted = self.num_questions_entry.get()

        # Reset label and entry box (for when users come back to home screen)
        self.choose_label.config(fg="#009900", font=("Arial", 12, "bold"))
        self.num_questions_entry.config(bg="#FFFFFF")

        error = "Oops - Please choose a whole number more than zero."
        has_errors = "no"

        # checks that amount to be converted is a number above absolute zero
        try:
            questions_wanted = int(questions_wanted)
            if questions_wanted > 0:
                # Invoke Play Class (and take across number of questions)
                Play(questions_wanted)
                # Hide root window (ie: hide questions choice window
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
    Interface for playing Colour Quest game
    """

    def __init__(self, how_many):
        self.rounds_won = IntVar()

        self.play_box = Toplevel()

        self.game_frame = Frame(self.play_box)
        self.game_frame.grid(padx=10, pady=10)

        self.heading_label = Label(self.game_frame, text="Colour Quest", font=("Arial", 16, "bold"),
                                   padx=5, pady=5)
        self.heading_label.grid(row=0)

        self.stats_button = Button(self.game_frame, font=("Arial", 14, "bold"),
                                   text="Stats", width=15, fg="#FFFFFF",
                                   bg="#FF8000", padx=10, pady=10, command=self.to_stats)
        self.stats_button.grid(row=1)


    def to_stats(self):
        """
        Retrieve everything we need to display the game / round statistics
        """



class Stats:
    """
    Displays stats for Colour Quest Game
    """

    def __init__(self, partner, all_stats_info):
        # Extract information from master list...
        rounds_won = all_stats_info[0]
        user_scores = all_stats_info[1]
        high_scores = all_stats_info[2]

        # sort user scores to find high score...
        user_scores.sort()

        self.stats_box = Toplevel()

        # disable help button
        partner.stats_button.config(state=DISABLED)

        # If users press cross at top, closes help and
        # 'releases' help button
        self.stats_box.protocol('WM_DELETE_WINDOW',
                                partial(self.close_stats, partner))

        self.stats_frame = Frame(self.stats_box, width=350)
        self.stats_frame.grid()

        # Math to populate Stats dialogue
        rounds_played = len(user_scores)

        success_rate = rounds_won / rounds_played * 100
        total_score = sum(user_scores)
        max_possible = sum(high_scores)

        best_score = user_scores[-1]
        average_score = total_score / rounds_played

        # Strings for Stats label...

        success_string = (f"Success Rate: {rounds_won} / {rounds_played}"
                          f" ({success_rate:.0f}%")
        total_score_string = f"Total Score: {total_score}"
        max_possible_string = f"Maximum Possible Score: {max_possible}"
        best_score_string = f"Best Score: {best_score}"

        # custom comment text and formatting
        if total_score == max_possible:
            comment_string = ("Amazing! You got the highest "
                              "possible score!")
            comment_colour = "#D5E8D4"

        elif total_score == 0:
            comment_string = ("Oops - You've lost every round! "
                             )
            comment_colour = "#F8CECH"
            best_score_string = f"Best Score: n/a"
        else:
            comment_string = ""
            comment_colour = "#F0F0F0"

        average_score_string = f"Average Score: {average_score:.0f}\n"
        heading_font = ("Arial", 16, "bold")
        normal_font = ("Arial", 14)
        comment_font = ("Arial", 13)

        # Label list (text | font | 'Sticky')
        all_stats_strings = [
            ["Statistics", heading_font, ""],
            [success_string, normal_font, "W"],
            [total_score_string, normal_font, "W"],
            [max_possible_string, normal_font, "W"],
            [comment_string, comment_font, "W"],
            ["\nRound Stats", heading_font, ""],
            [best_score_string, normal_font, "W"],
            [average_score_string, normal_font, "W"]
        ]

        stats_label_ref_list = []
        for count, item in enumerate(all_stats_strings):
            self.stats_label = Label(self.stats_frame, text=item[0], font=item[1],
                                     anchor="w", justify="left",
                                     padx=30, pady=5)
            self.stats_label.grid(row=count, sticky=item[2], padx=10)
            stats_label_ref_list.append(self.stats_label)

        # Configure comment label background for all won / lost
        stats_comment_label = stats_label_ref_list[4]
        stats_comment_label.config(bg=comment_colour)

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