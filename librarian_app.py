import tkinter as tk
from tkinter import ttk, messagebox
from datetime import timedelta, datetime
import psycopg2
from dotenv import load_dotenv
import os
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
        ttk.Button(self.frame, text="Remove Seat", command=self.change_seat).grid(row=1, column=1)
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

        ttk.Label(self.frame, text = "Location").grid(row = 0, column = 0, padx = 10, pady = 40)
        ttk.Label(self.frame, text = "Seat Number").grid(row = 1, column = 0, padx = 10, pady = 40)

        self.selected_location = tk.StringVar()
        self.selected_location.set("Select Seat Location")
        
        dropdown = ttk.Combobox(self.frame, textvariable=self.selected_location, values=["UP","FRONT","LEFT","RIGHT","BACK","CENTRE"], state="readonly")
        dropdown.grid(row=0, column=1, padx=10, pady=40)

        self.seat_number_var = tk.StringVar()
        self.seat_number_var.set("")
        ttk.Label(self.frame, textvariable=self.seat_number_var).grid(row = 1, column = 1,padx = 10, pady = 10)
        self.selected_location.trace("w", self.update_seat_number)

        ttk.Button(self.frame, text = "Back",command = self.go_back).grid(row = 2, column = 0, padx = 10, pady = 10)
        ttk.Button(self.frame, text = "Insert Seat", command = self.insert_seat).grid(row = 2,column = 1, padx = 10, pady = 20)
       

    def update_seat_number(self, *args):
        with conn.cursor() as cur:            
            cur.execute(f"""
                SELECT number from (select generate_series(1,100) as number)
                WHERE number NOT IN (SELECT seat_no from seat
                WHERE location = '{self.selected_location.get()}')        
                ORDER BY number;           
            """)
            self.valid_seat_num = cur.fetchone()[0]
            self.seat_number_var.set(self.valid_seat_num)

    def insert_seat(self):
        if self.selected_location.get() == "Select Seat Location":
            messagebox.showerror("Error","Chose a Seat Location")
            return None
        with conn.cursor() as cur:
            cur.execute(f"Insert into seat (location,seat_no) VALUES {self.selected_location.get(),self.valid_seat_num}")
        conn.commit()
        messagebox.showinfo("Message","Added the Seat")
        self.update_seat_number(self)

    def go_back(self):
        self.controller.show_frame('Main_screen')

    def pack_frame(self):
        self.frame.pack()

import tkinter as tk
from tkinter import ttk, messagebox

class ChangeSeats:
    def __init__(self, controller):
        self.controller = controller
        self.frame = ttk.Frame(controller.root)

        ttk.Label(self.frame, text="Location").grid(row=0, column=0, padx=10, pady=40)

        self.selected_location = tk.StringVar()
        self.selected_location.set("Select a Location")
        self.dropdown = ttk.Combobox(self.frame, textvariable=self.selected_location, values=["UP", "FRONT", "LEFT", "RIGHT", "BACK", "CENTRE"], state="readonly")
        self.dropdown.grid(row=0, column=1, padx=10, pady=40)
        self.selected_location.trace("w", self.update_seat_values)

        ttk.Label(self.frame, text="Seat Number").grid(row=1, column=0, padx=10, pady=40)
        self.seat_value = tk.StringVar()
        self.seat_dropdown = ttk.Combobox(self.frame, textvariable=self.seat_value, state="readonly")
        self.seat_dropdown.grid(row=1, column=1, padx=10, pady=10)

        ttk.Button(self.frame, text="Back", command=self.go_back).grid(row=2, column=0, padx=10, pady=10)
        ttk.Button(self.frame, text="Confirm", command=self.delete_seat).grid(row=2, column=1, padx=10, pady=10)

    def update_seat_values(self, *args):
        location = self.selected_location.get()
        with conn.cursor() as cur:
            cur.execute(f"SELECT seat_no FROM seat WHERE location = '{location}';")
            seat_values = [row[0] for row in cur.fetchall()]

        seat_values.sort()
        self.seat_dropdown['values'] = seat_values
        if seat_values == []:
            self.seat_value.set("NULL")
            messagebox.showinfo("Message","All Seats corresponding to this location are deleted")
        else:
            self.seat_value.set(seat_values[-1])

    def delete_seat(self):
        if self.selected_location.get() == "Select a Location":
            messagebox.showerror("Error","Select a Location")
            return None
        
        if self.seat_value.get() == "NULL":
            messagebox.showinfo("Message","Chose Another Location to proceed")
            return None
        
        ok = messagebox.askokcancel("Confirmation", "Do you want to confirm")
        if not ok:
            return
        with conn.cursor() as cur:
            cur.execute(f"DELETE FROM seat WHERE location = '{self.selected_location.get()}' AND seat_no = '{self.seat_value.get()}';")
        conn.commit()
        messagebox.showinfo("Info", "Seat deleted successfully.")
        self.controller.show_frame('Main_screen')

    def go_back(self):
        self.controller.show_frame('Main_screen')

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
    load_dotenv()
    database_url = os.getenv('DATABASE_URL')
    print(database_url)
    conn = psycopg2.connect(database_url)
    
    root = tk.Tk()
    Window(root)
    root.mainloop()
