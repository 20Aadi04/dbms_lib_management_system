import tkinter as tk
from tkinter import ttk, messagebox
from datetime import timedelta, datetime
import os
import psycopg2
from dotenv import load_dotenv
import sys



class LibrarySeatManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Seat Management System")
        self.root.geometry("600x600")
        
        # Style
        self.style = ttk.Style()
        self.style.configure('TLabel', font=('Helvetica', 12), padding=5)
        self.style.configure('TButton', font=('Helvetica', 10), padding=5)
        self.style.configure('TEntry', font=('Helvetica', 10), padding=5)

        # Initialize frames
        self.login_frame = LoginFrame(self)
        self.register_frame = RegisterFrame(self)
        self.time_slot_frame = TimeSlotFrame(self)
        self.seat_booking_frame = SeatBookingFrame(self)
        self.books_frame = BooksFrame(self)

        self.login_frame.pack_frame()



    def show_frame(self, frame_name):
        # Hide all frames
        for frame in [self.login_frame, self.register_frame, self.time_slot_frame, self.seat_booking_frame]:
            frame.hide_frame()
        # Show the specified frame
        getattr(self, frame_name).pack_frame()

class LoginFrame:
    def __init__(self, app):
        self.app = app
        self.frame = ttk.Frame(app.root)

        ttk.Label(self.frame, text="Student ID: ").grid(row=0, column=0, pady=20, padx=10)
        self.student_id_entry = ttk.Entry(self.frame)
        self.student_id_entry.grid(row=0, column=1, pady=20, padx=10)

        ttk.Label(self.frame, text="Password: ").grid(row=1, column=0, pady=20, padx=10)
        self.password_entry = ttk.Entry(self.frame, show="*")
        self.password_entry.grid(row=1, column=1, pady=20, padx=10)

        ttk.Button(self.frame, text="Login", command=self.login).grid(row=2, column=1, pady=20, padx=10)
        ttk.Button(self.frame, text="Register", command=lambda: self.app.show_frame("register_frame")).grid(row=3, column=1, pady=20, padx=10)



    def login(self):
        self.app.show_frame("time_slot_frame")

    def pack_frame(self):
        self.frame.pack(pady=40)

    def hide_frame(self):
        self.frame.pack_forget()

class RegisterFrame:
    def __init__(self, app):
        self.app = app
        self.frame = ttk.Frame(app.root)

        self.first_name_entry = self.add_label_and_entry("First Name:", 0)
        self.last_name_entry = self.add_label_and_entry("Last Name:", 1)
        self.student_id_entry_reg = self.add_label_and_entry("Student ID:", 2)
        self.email_entry = self.add_label_and_entry("Email:", 3)
        self.phone_number_entry = self.add_label_and_entry("Phone Number:", 4)
        self.grad_type_entry = self.add_label_and_entry("Graduation Type:", 5)
        self.dob_entry = self.add_label_and_entry("Date of Birth:", 6)
        self.password_entry_reg = ttk.Entry(self.frame, show="*")
        
        ttk.Label(self.frame, text="Create a Password: ").grid(row=7, column=0, pady=10, padx=10)
        self.password_entry_reg.grid(row=7, column=1, pady=10, padx=10)
        
        ttk.Button(self.frame, text="Submit", command=self.submit_registration).grid(row=8, column=1, pady=20)

    def add_label_and_entry(self, text, row):
        ttk.Label(self.frame, text=text).grid(row=row, column=0, pady=10, padx=10)
        entry = ttk.Entry(self.frame)
        entry.grid(row=row, column=1, pady=10, padx=10)
        return entry

    def submit_registration(self):
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        student_id = self.student_id_entry_reg.get()
        email = self.email_entry.get()
        phone_number = self.phone_number_entry.get()
        grad_type = self.grad_type_entry.get()
        dob = self.dob_entry.get()
        password = self.password_entry_reg.get()

        if (first_name and last_name and student_id and email and phone_number and grad_type and dob):

            # Insert Values into the student table
            try:
                with conn.cursor() as cur:
                    cur.execute(f"INSERT INTO student (student_id, fname, lname, dob, grad_type, email, phone_num) VALUES ({student_id}, '{first_name}', '{last_name}', '{dob}', '{grad_type}', '{email}', {phone_number});")
                    conn.commit()
                    messagebox.showinfo("Registration", "Registration Successful")
                    self.app.show_frame("login_frame")
            except Exception as e:
                print(e)
                messagebox.showerror("Error","Values Do not match required datatypes")
        else:
            messagebox.showerror("Error", "Please Enter data properly")

    def pack_frame(self):
        self.frame.pack(pady=20)

    def hide_frame(self):
        self.frame.pack_forget()

class TimeSlotFrame:
    def __init__(self, app):
        self.app = app
        self.frame = ttk.Frame(app.root)

        ttk.Label(self.frame, text="Select Start Time: ").grid(row=0, column=0, pady=10, padx=10)
        self.start_time_slider = ttk.Scale(self.frame, from_=0, to=180, orient="vertical", command=self.update_time_labels, length=400)
        self.start_time_slider.grid(row=1, column=0, pady=10, padx=10)
        self.start_time_label = ttk.Label(self.frame, text="08:00")
        self.start_time_label.grid(row=2, column=0, pady=10, padx=10)

        ttk.Label(self.frame, text="Select End Time: ").grid(row=0, column=2, pady=10, padx=10)
        self.end_time_slider = ttk.Scale(self.frame, from_=6, to=180, orient="vertical", command=self.update_time_labels, length=400)
        self.end_time_slider.grid(row=1, column=2, pady=10, padx=10)
        self.end_time_label = ttk.Label(self.frame, text="08:30")
        self.end_time_label.grid(row=2, column=2, pady=10, padx=10)

        ttk.Button(self.frame, text="Select Time Slot", command=lambda: self.app.show_frame("seat_booking_frame")).grid(row=1, column=1, pady=20)

    def update_time_labels(self, event=None):
        start_minutes = round(self.start_time_slider.get()) * 5
        end_minutes = round(self.end_time_slider.get()) * 5

        tomorrow = datetime.now() + timedelta(days=1)
        tomorrow_at_8am = tomorrow.replace(hour=8, minute=0, second=0, microsecond=0)
        start_time = tomorrow_at_8am + timedelta(minutes=start_minutes)
        end_time = tomorrow_at_8am + timedelta(minutes=end_minutes)

        if start_minutes > 870:
            self.start_time_slider.set(174)
        elif (end_time - start_time).total_seconds() < 1800:
            self.end_time_slider.set((start_minutes // 5) + 6)
        elif (end_time - start_time).total_seconds() > 7200:
            self.end_time_slider.set((start_minutes // 5) + 24)
        else:
            self.start_time_label.config(text=start_time.strftime("%H:%M"))
            self.end_time_label.config(text=end_time.strftime("%H:%M"))

    def pack_frame(self):
        self.frame.pack(pady=40)

    def hide_frame(self):
        self.frame.pack_forget()

class SeatBookingFrame:
    def __init__(self, app):
        self.app = app
        self.frame = ttk.Frame(app.root)

        ttk.Label(self.frame, text="Seat Number: ").grid(row=0, column=0, pady=10, padx=10)
        self.seat_number_dropdown = ttk.Combobox(self.frame, values=[str(i) for i in range(1, 101)], state="readonly")
        self.seat_number_dropdown.grid(row=0, column=1, pady=10, padx=10)

        ttk.Label(self.frame, text="Seat Location: ").grid(row=1, column=0, pady=10, padx=10)
        self.seat_location_dropdown = ttk.Combobox(self.frame, values=["Upper", "Lower"], state="readonly")
        self.seat_location_dropdown.grid(row=1, column=1, pady=10, padx=10)

        ttk.Button(self.frame, text="Submit Booking", command=self.submit_booking).grid(row=2, column=1, pady=20)

    def submit_booking(self):
        seat_number = self.seat_number_dropdown.get()
        seat_location = self.seat_location_dropdown.get()

        if seat_number and seat_location:
            messagebox.showinfo("Booking", "Seat booked successfully!")
            self.app.show_frame("books_frame")
            # self.app.root.destroy()
        else:
            messagebox.showerror("Error", "Choose a Valid Seat Number and Seat Location")

    def pack_frame(self):
        self.frame.pack(pady=40)

    def hide_frame(self):
        self.frame.pack_forget()

class BooksFrame:
    def __init__(self, app):
        self.app = app
        self.selected_books = []
        
        self.frame = ttk.Frame(app.root)

        self.canvas = tk.Canvas(self.frame, width=1000, height=600)
        self.scrollbar_y = ttk.Scrollbar(self.frame, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar_y.set)
        
        self.scrollbar_x = ttk.Scrollbar(self.frame, orient="horizontal", command=self.canvas.xview)
        self.canvas.configure(xscrollcommand=self.scrollbar_x.set)

        self.scrollable_frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.scrollbar_y.pack(side="right", fill="y")
        self.scrollbar_x.pack(side="bottom", fill="x")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.create_table_headers()
        self.display_books()
        
        self.confirm_button = ttk.Button(self.frame, text="Confirm Selection", command=self.confirm_selection)
        self.confirm_button.pack(pady=10)

    def create_table_headers(self):
        headers = ["Book Name", "Author", "ISBN", "Publisher", "Select"]
        for col, header in enumerate(headers):
            label = ttk.Label(self.scrollable_frame, text=header, font=('Helvetica', 12, 'bold'), anchor="center")
            label.grid(row=0, column=col, padx=5, pady=10, sticky="nsew")

    def display_books(self):
        books = self.retrieve_books()
        self.check_vars = []

        for i, book in enumerate(books, start=1):
            book_id, b_name, isbn, author, publisher, category = book

            cells = [
                b_name,
                author,
                isbn,
                publisher
            ]

            for col, text in enumerate(cells):
                label = ttk.Label(self.scrollable_frame, text=text, font=('Helvetica', 10), anchor="w")
                label.grid(row=i, column=col, padx=5, pady=5, sticky="w")

            var = tk.IntVar()
            checkbox = ttk.Checkbutton(self.scrollable_frame, variable=var, command=lambda var=var, book=book: self.limit_selection(var, book))
            checkbox.grid(row=i, column=4, padx=5, pady=5)
            self.check_vars.append(var)

        self.scrollable_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def limit_selection(self, var, book):
        if var.get() == 1:
            if len(self.selected_books) < 3:
                self.selected_books.append(book)
            else:
                var.set(0)
                messagebox.showwarning("Selection Limit", "You can only select up to 3 books.")
        else:
            self.selected_books.remove(book)

    def retrieve_books(self):
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM book;")
            return cur.fetchall()

    def confirm_selection(self):
        if not self.selected_books:
            messagebox.showinfo("No Selection", "Please select at least one book.")
        else:
            selected_titles = [book[1] for book in self.selected_books]
            messagebox.showinfo("Books Selected", f"Selected books: {', '.join(selected_titles)}")
            # Implement save or further processing of selected_books here

    def pack_frame(self):
        self.frame.pack(pady=40)

    def hide_frame(self):
        self.frame.pack_forget()


# Initialize and run the application
root = tk.Tk()

load_dotenv()
database_url = os.getenv('DATABASE_URL')
print(database_url)
conn = psycopg2.connect(database_url)
app = LibrarySeatManagementSystem(root)
root.mainloop()
