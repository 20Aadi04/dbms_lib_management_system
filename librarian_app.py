import tkinter as tk
from tkinter import ttk, messagebox
from datetime import timedelta, datetime
import sys

class Window:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")
        self.root.geometry("400x400")

        self.style = ttk.Style()
        self.style.configure('TLabel', font=('Helvetica', 12), padding=5)
        self.style.configure('TButton', font=('Helvetica', 10), padding=5)
        self.style.configure('TEntry', font=('Helvetica', 10), padding=5)

        self.Main_screen = MainScreen(self)
        self.add_seats = AddSeats(self)
        self.change_seats = ChangeSeats(self)
        self.add_books = AddBooks(self)
        self.change_books = ChangeBooks(self)

        self.Main_screen.pack_frame()

    def show_frame(self, frame_name):
        for current_frame in [self.Main_screen, self.add_seats, self.change_seats, self.add_books, self.change_books]:
            current_frame.frame.pack_forget()
        getattr(self, frame_name).pack_frame()

class MainScreen:
    def __init__(self, controller):
        self.controller = controller
        self.frame = ttk.Frame(controller.root)

        ttk.Label(self.frame, text="Librarian Controls").grid(row=0, column=0)
        ttk.Button(self.frame, text="Add Seat", command=self.increase_seat).grid(row=1, column=0)
        ttk.Button(self.frame, text="Modify Seat", command=self.change_seat).grid(row=1, column=1)
        ttk.Button(self.frame, text="Add Book", command=self.increase_book).grid(row=2, column=0)
        ttk.Button(self.frame, text="Modify Book", command=self.change_book).grid(row=2, column=1)

    def increase_seat(self):
        self.controller.show_frame('add_seats')

    def change_seat(self):
        self.controller.show_frame('change_seats')

    def increase_book(self):
        self.controller.show_frame('add_books')

    def change_book(self):
        self.controller.show_frame('change_books')

    def pack_frame(self):
        self.frame.pack()

class AddSeats:
    def __init__(self, controller):
        self.controller = controller
        self.frame = ttk.Frame(controller.root)

    def pack_frame(self):
        self.frame.pack()

class ChangeSeats:
    def __init__(self, controller):
        self.controller = controller
        self.frame = ttk.Frame(controller.root)

    def pack_frame(self):
        self.frame.pack()

class AddBooks:
    def __init__(self, controller):
        self.controller = controller
        self.frame = ttk.Frame(controller.root)

    def pack_frame(self):
        self.frame.pack()

class ChangeBooks:
    def __init__(self, controller):
        self.controller = controller
        self.frame = ttk.Frame(controller.root)

    def pack_frame(self):
        self.frame.pack()

if __name__ == '__main__':
    root = tk.Tk()
    Window(root)
    root.mainloop()
