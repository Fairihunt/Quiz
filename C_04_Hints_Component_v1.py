from tkinter import *
from functools import partial # To prevent unwanted windows


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
                                  fg="#FFFFFF", bg="#9957D8", text="Play", width=10,
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








# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Quiz")
    StartGame()
    root.mainloop()