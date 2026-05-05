from tkinter import *
from functools import partial # To prevent unwanted windows


class StartGame:
    """
    Initial Game interface (asks users how many rounds they
    would like to play
    """

    def __init__(self):
        """
        Gets number of rounds from user
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
            ["Study  of...? Quiz", ("Arial", 16, "bold"), None],
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

        self.num_rounds_entry = Entry(self.entry_area_frame, font=("Arial", 20, "bold"),
                                      width=10)
        self.num_rounds_entry.grid(row=0, column=0, padx=10, pady=10)

        # Create play button...
        self.play_button = Button(self.entry_area_frame, font=("Arial", 16, "bold"),
                                  fg="#FFFFFF", bg="#000000", text="Play", width=10,
                                  command=self.check_questions)
        self.play_button.grid(row=0, column=1)

    def check_questions(self):
        """
        Check users have entered 1 or more rounds
        """

        # Retrieve temperature to be converted
        rounds_wanted = self.num_rounds_entry.get()

        # Reset label and entry box (for when users come back to home screen)
        self.choose_label.config(fg="#009900", font=("Arial", 12, "bold"))
        self.num_rounds_entry.config(bg="#000000")

        error = "Oops - Please choose a whole number more than zero"
        has_errors = "no"

        # checks that amount to be converted is a number above absolute zero
        try:
            rounds_wanted = int(rounds_wanted)
            if rounds_wanted > 0:
                # Invoke Play Class (and take across number of rounds)
                Play(rounds_wanted)
                # Hide root window (ie: hide rounds choice window)
                root.withdraw()
            else:
                has_errors = "yes"

        except ValueError:
            has_errors = "yes"

        # display the error if necessary
        if has_errors == "yes":
            self.choose_label.config(text=error, fg="#990000",
                                     font=("Arial", 10, "bold"))
            self.num_rounds_entry.config(bg="#F4CCCC")
            self.num_rounds_entry.delete(0, END)


class Play:
    """
    Interface for playing the Colour Quest Game
    """

    def __init__ (self, how_many):
        self.play_box = Toplevel()

        self.game_frame = Frame(self.play_box)
        self.game_frame.grid(padx=10, pady=10)

        self.heading_label = Label(self.game_frame, text="Colour Quest", font=("Arial", 16, "bold"),
                                   padx=5, pady=5)
        self.heading_label.grid(row=0)

        self.end_game_button = Button(self.game_frame, text="End Game",
                                      font=("Arial", 16, "bold"),
                                      fg="#FFFFFF", bg="#990000", width="10",
                                      command=self.close_play)
        self.end_game_button.grid(row=1)

    def close_play(self):
        # reshow root (ie: choose rounds) and end current)
        # game / allow new game to start
        root.deiconify()
        self.play_box.destroy()





# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Colour Quest")
    StartGame()
    root.mainloop()