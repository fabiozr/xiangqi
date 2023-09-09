from tkinter import *
from tkmacosx import Button
from .settings import *


class ControlFrame:
    def __init__(self, root: Tk):
        self.frame = Frame(root, bg=BACKGROUND_COLOR)
        self.player_timer = self._initialize_timer(0.75)
        self.opponent_timer = self._initialize_timer(0.25)
        self.give_up_button = self._initialize_button()

    def _initialize_timer(self, rely: float):
        label = Label(
            self.frame,
            text="10:00",
            font=TIMER_FONT,
            bg=TIMER_COLOR,
            fg=TEXT_COLOR,
            padx=40,
            pady=15,
        )
        return label.place(relx=0.5, rely=rely, anchor=CENTER)

    def _initialize_button(self):
        give_up_button = Button(
            self.frame,
            text=GIVE_UP_TEXT,
            font=GIVE_UP_FONT,
            bg=GIVE_UP_COLOR,
            fg=TEXT_COLOR,
            activebackground=GIVE_UP_COLOR_ACTIVE,
            activeforeground=TEXT_COLOR,
            padx=20,
        )
        return give_up_button.place(relx=0.5, rely=0.5, anchor=CENTER)
