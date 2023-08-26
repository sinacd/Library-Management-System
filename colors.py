import tkinter
from tkinter import *

lightBlue = '#04fefd'
lightBlue2 = '#4796d0'
darkBlue = '#232438'
darkBlue2 = '#293744'
lightWhite = '#f3f3f3'
font1 = (0, 9, "bold")


class Button1(Button):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial()
        self.bind("<Enter>", self.enter)
        self.bind("<Leave>", self.leave)

    def enter(self, e):
        self['bg'] = lightBlue2

    def leave(self, e):
        self['bg'] = darkBlue2

    def initial(self):
        self['bg'] = darkBlue2
        self['fg'] = lightWhite


class EntryWithPlaceholder(Entry):
    def __init__(self, placeholder, color=darkBlue2, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self['fg']

        self.bind("<FocusIn>", self.foc_in)
        self.bind("<FocusOut>", self.foc_out)

        self.put_placeholder()

    def put_placeholder(self):
        # print(self.get())
        # if self.get() != '':
        self.insert(0, self.placeholder)
        self['fg'] = self.placeholder_color

    def foc_in(self, *args):
        if self['fg'] == self.placeholder_color:
            self.delete('0', 'end')
            self['fg'] = self.default_fg_color

    def foc_out(self, *args):
        if not self.get():
            self.put_placeholder()
