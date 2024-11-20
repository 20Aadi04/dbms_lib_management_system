import requests
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.font import Font
from RangeSlider.RangeSlider import RangeSliderH
from datetime import timedelta, datetime
import os
import psycopg2
from dotenv import load_dotenv
from tkcalendar import DateEntry
from collections import defaultdict

class windows(tk.Tk):
    data = {'stime': "", 'etime': "", 'cur_seat_info': {'location': "", 'seat_no': None, 'seat_id': None}, 'Book_logs': []}
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.wm_title("Library Seat Management App")
        self.geometry("600x800")

        self.style = ttk.Style()
        self.style.configure('TLabel', font=('Helvetica', 12), padding=5)
        self.style.configure('TButton', font=('Helvetica', 10), padding=5)
        self.style.configure('TEntry', font=('Helvetica', 10), padding=5)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Create the container frame
        container = tk.Frame(self)
        container.pack(side="top", fill="both")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        # Initialize frames
        for F in (LoginPage, BookingHistoryPage, BookingTimeSlotPage, RegistrationPage, BookingAddBookPage, BookingFinalizePage, HomePage):
            frame = F(container, self)
            self.frames[F] = frame

        # Show the LoginPage initially
        self.show_frame(LoginPage)

    def show_frame(self, cont):
        """Switch between frames."""
        frame = self.frames[cont]
        for i in self.frames.values():
            i.pack_forget()
        frame.refresh()
        frame.pack(fill="both", expand=True)
        

    def on_closing(self):
        """Close the application."""
        self.destroy()

    def request_api(self, endpoint, method='GET', data=None, params=None):
        """Send a request to the Flask backend."""
        base_url = "http://127.0.0.1:5000"
        try:
            if method == 'GET':
                response = requests.get(f"{base_url}{endpoint}", params=params)
            elif method == 'POST':
                response = requests.post(f"{base_url}{endpoint}", json=data)

            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"API request failed: {e}")
            return None


class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Title
        ttk.Label(self, text="Login", font=("Helvetica", 16, "bold")).pack(pady=20)

        # Student ID Entry
        ttk.Label(self, text="Student ID").pack(pady=5)
        self.student_id_entry = ttk.Entry(self)
        self.student_id_entry.pack(pady=5)

        # Password Entry
        ttk.Label(self, text="Password").pack(pady=5)
        self.password_entry = ttk.Entry(self, show="*")
        self.password_entry.pack(pady=5)

        # Login Button
        login_button = ttk.Button(self, text="Login", command=self.login)
        login_button.pack(pady=20)

        # re
        login_button = ttk.Button(self, text="Registartion", command=lambda :self.controller.show_frame(RegistrationPage) )
        login_button.pack(pady=20)

        # Error message
        self.error_label = ttk.Label(self, text="", foreground="red")
        self.error_label.pack()

    def login(self):
        """Attempt to log in the user."""
        student_id = self.student_id_entry.get()
        password = self.password_entry.get()

        if not student_id or not password:
            self.error_label.config(text="Both fields are required.")
            return

        # API request to log in
        response = self.controller.request_api(
            endpoint="/login",
            method="POST",
            data={"student_id": student_id, "password": password},
        )

        if response and response.get("success"):
            # Save user data to the controller
            self.controller.data.update(response["user_data"])
            self.controller.show_frame(HomePage)  # Navigate to HomePage
        else:
            self.error_label.config(
                text=response["error"] if response else "Login failed."
            )

    def refresh(self):
        """Clear the form and error message."""
        self.student_id_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.error_label.config(text="")

class RegistrationPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        ttk.Label(self, text="First Name: ").grid(row=0, column=0, pady=10, padx=10)
        self.first_name_entry = ttk.Entry(self)
        self.first_name_entry.grid(row=0, column=1, pady=10, padx=10)

        ttk.Label(self, text="Last Name: ").grid(row=1, column=0, pady=10, padx=10)
        self.last_name_entry = ttk.Entry(self)
        self.last_name_entry.grid(row=1, column=1, pady=10, padx=10)

        ttk.Label(self, text="Student ID: ").grid(row=2, column=0, pady=10, padx=10)
        self.student_id_entry_reg = ttk.Entry(self)
        self.student_id_entry_reg.grid(row=2, column=1, pady=10, padx=10)

        ttk.Label(self, text="Email: ").grid(row=3, column=0, pady=10, padx=10)
        self.email_entry = ttk.Entry(self)
        self.email_entry.grid(row=3, column=1, pady=10, padx=10)

        ttk.Label(self, text="Phone Number: ").grid(row=4, column=0, pady=10, padx=10)
        self.phone_number_entry = ttk.Entry(self)
        self.phone_number_entry.grid(row=4, column=1, pady=10, padx=10)

        ttk.Label(self, text="Graduation Type: ").grid(row=5, column=0, pady=10, padx=10)
        self.grad_type_var = tk.StringVar()
        self.grad_type_combobox = ttk.Combobox(self, textvariable=self.grad_type_var)
        self.grad_type_combobox['values'] = ('FIRST DEGREE', 'SECOND DEGREE')
        self.grad_type_combobox.current(0)
        self.grad_type_combobox.grid(row=5, column=1, pady=10, padx=10)

        ttk.Label(self, text="Date of Birth: ").grid(row=6, column=0, pady=10, padx=10)
        self.dob_entry = DateEntry(self, date_pattern="yyyy-mm-dd")
        self.dob_entry.grid(row=6, column=1, pady=10, padx=10)

        ttk.Label(self, text="Create a Password: ").grid(row=7, column=0, pady=10, padx=10)
        self.password_entry_reg = ttk.Entry(self, show="*")
        self.password_entry_reg.grid(row=7, column=1, pady=10, padx=10)

        ttk.Button(self, text="Submit", command=self.submit_registration).grid(row=8, column=1, pady=20)

    def submit_registration(self):
        """Submit the registration form to the backend."""
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        student_id = self.student_id_entry_reg.get()
        email = self.email_entry.get()
        phone_number = self.phone_number_entry.get()
        grad_type = self.grad_type_var.get()
        dob = self.dob_entry.get()
        password = self.password_entry_reg.get()
        password = str(hash(password))
        if first_name and last_name and student_id and email and phone_number and grad_type and dob and password:
            # Prepare payload for API
            payload = {
                "student_id": student_id,
                "fname": first_name,
                "lname": last_name,
                "dob": dob,
                "grad_type": grad_type,
                "email": email,
                "phone_num": phone_number,
                "password": password
            }

            # Call the backend API
            response = self.controller.request_api(endpoint="/register", method="POST", data=payload)

            if response and response.get("success"):
                messagebox.showinfo("Registration", "Registration Successful")
                self.controller.show_frame(LoginPage)
            else:
                messagebox.showerror("Error",  "Registration failed. Please try again.")
        else:
            messagebox.showerror("Error", "Please fill out all fields correctly.")

    def refresh(self):
        """Reset all input fields when the page is refreshed."""
        self.first_name_entry.delete(0, tk.END)
        self.last_name_entry.delete(0, tk.END)
        self.student_id_entry_reg.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.phone_number_entry.delete(0, tk.END)
        self.grad_type_combobox.current(0)
        self.dob_entry.set_date("2004-01-01")
        self.password_entry_reg.delete(0, tk.END)


class BookingTimeSlotPage(tk.Frame):
    max_time_span = 4 * 60  # minutes
    min_time_span = 60  # minutes

    max_time = 600
    min_time = 0

    left_pointer = min_time
    right_pointer = min_time + min_time_span

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.hLeft = tk.DoubleVar(value=self.left_pointer)
        self.hRight = tk.DoubleVar(value=self.right_pointer)
        self.slider = RangeSliderH(
            self, [self.hLeft, self.hRight], padX=16, step_size=5,
            min_val=self.min_time, max_val=self.max_time, show_value=False
        )
        self.hRight.trace_add('write', self.correct_slider)

        ttk.Label(self, text="Start Time: ").grid(row=0, column=0, pady=10, padx=10)

        self.time_start = tk.StringVar()
        start_time_label = ttk.Label(self, textvariable=self.time_start)
        start_time_label.grid(row=0, column=1, pady=10, padx=10)

        ttk.Label(self, text="End Time: ").grid(row=0, column=2, pady=10, padx=10)
        self.time_end = tk.StringVar()
        end_time_label = ttk.Label(self, textvariable=self.time_end)
        end_time_label.grid(row=0, column=3, pady=10, padx=10)

        ttk.Button(self, text="Search", command=self.search).grid(row=0, column=4, pady=10, padx=10)
        self.slider.grid(row=1, column=0, columnspan=5)
        self.update_time_labels()

        # Table for displaying seat data
        self.canvas = tk.Canvas(self, height = 600)
        self.scrollbar_y = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar_y.set)

        self.scrollable_frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.scrollbar_y.grid(row=3, column=5, sticky="ns")
        self.canvas.grid(row=3, column=0, columnspan=5, sticky="nsew", pady=10)

        ttk.Button(self, text="Back", command=lambda: controller.show_frame(HomePage)).grid(row=5, column=0, pady=10, padx=10)

        self.seat_vars = {}
        self.selected_seat = None

    def correct_slider(self, *args):
        lp = self.hLeft.get()
        rp = self.hRight.get()
        if rp != self.right_pointer:
            if rp <= self.min_time_span:
                rp = self.min_time_span
            elif abs(lp - rp) > self.max_time_span:
                lp = rp - self.max_time_span
            elif abs(lp - rp) < self.min_time_span:
                lp = rp - self.min_time_span
        else:
            if lp >= self.max_time - self.min_time_span:
                lp = self.max_time - self.min_time_span
            elif abs(lp - rp) > self.max_time_span:
                rp = lp + self.max_time_span
            elif abs(lp - rp) < self.min_time_span:
                rp = lp + self.min_time_span
        self.left_pointer = lp
        self.right_pointer = rp
        self.update_time_labels()
        self.slider.forceValues([lp, rp])

    def update_time_labels(self):
        tomorrow = datetime.now() - timedelta(days=1)
        tomorrow_at_8am = tomorrow.replace(hour=8, minute=0, second=0, microsecond=0)
        start_time = tomorrow_at_8am + timedelta(minutes=self.left_pointer)
        end_time = tomorrow_at_8am + timedelta(minutes=self.right_pointer)
        self.time_start.set(start_time.strftime("%H:%M"))
        self.time_end.set(end_time.strftime("%H:%M"))

    def search(self):
        tomorrow = datetime.now() + timedelta(days=1)
        tomorrow_at_8am = tomorrow.replace(hour=8, minute=0, second=0, microsecond=0)
        start_time = tomorrow_at_8am + timedelta(minutes=self.left_pointer)
        end_time = tomorrow_at_8am + timedelta(minutes=self.right_pointer)

        self.controller.data['stime'] = start_time.strftime("%Y-%m-%d %H:%M:%S")
        self.controller.data['etime'] = end_time.strftime("%Y-%m-%d %H:%M:%S")

        if not self.check_booking_conflict():
            messagebox.showerror("Time Slot Error", "Your time slot seems to be clashing with your other bookings. Please select a different time slot.")
            return

        # API Call to Fetch Available Seats
        response = self.controller.request_api(
            endpoint="/available-seats",
            method="GET",
            params={"start_time": self.controller.data['stime'], "end_time": self.controller.data['etime']}
        )

        if response and response.get("success"):
            seat_infos = response["seats"]
            self.update_seat_table(seat_infos)
        else:
            messagebox.showerror("Error", response.get("error", "Failed to fetch available seats."))

    def update_seat_table(self, seat_infos):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        headers = ["Seat ID", "Location", "Seat Number", "Select"]
        for col, header in enumerate(headers):
            label = ttk.Label(self.scrollable_frame, text=header, font=('Helvetica', 12, 'bold'))
            label.grid(row=0, column=col, padx=5, pady=5)

        self.seat_vars = {}

        for i, seat in enumerate(seat_infos, start=1):
            ttk.Label(self.scrollable_frame, text=seat['seat_id']).grid(row=i, column=0, padx=5, pady=5)
            ttk.Label(self.scrollable_frame, text=seat['location']).grid(row=i, column=1, padx=5, pady=5)
            ttk.Label(self.scrollable_frame, text=seat['seat_no']).grid(row=i, column=2, padx=5, pady=5)

            var = tk.IntVar()
            checkbox = ttk.Checkbutton(self.scrollable_frame, variable=var, command=lambda seat=seat: self.select_seat(seat))
            checkbox.grid(row=i, column=3, padx=5, pady=5)
            self.seat_vars[seat['seat_id']] = var

        self.scrollable_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def select_seat(self, seat):
        self.controller.data['cur_seat_info'] = seat
        self.controller.show_frame(BookingAddBookPage)

    def refresh(self):
        self.update_seat_table([])
        pass

    def check_booking_conflict(self):
        # API Call to Check Booking Conflict
        response = self.controller.request_api(
            endpoint="/check-booking-conflict",
            method="GET",
            params={
                "student_id": self.controller.data['student_id'],
                "start_time": self.controller.data['stime'],
                "end_time": self.controller.data['etime']
            }
        )

        if response and response.get("success"):
            return not response["conflict"]
        else:
            messagebox.showerror("Error", response.get("error", "Failed to check booking conflict."))
            return False



class BookingAddBookPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.selected_books = []
        self.book_widgets = []

        # Header
        header = ttk.Label(self, text="Select Books", font=("Helvetica", 14, "bold"))
        header.pack(pady=10)

        # Confirm Button
        self.confirm_button = ttk.Button(self, text="Confirm Selection", command=self.confirm_selection)
        self.confirm_button.pack(pady=10)
        self.back_button = ttk.Button(self, text="Back Selection", command=lambda: self.controller.show_frame(BookingTimeSlotPage))
        self.back_button.pack(pady=10)

        # Canvas and Scrollbar
        self.canvas = tk.Canvas(self, height=700, width=550)
        self.scrollbar_y = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar_y.set)

        # Scrollable Frame
        self.scrollable_frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # Pack canvas and scrollbar
        self.scrollbar_y.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        # Scroll functionality with the mouse wheel
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        # Display books
        self.display_books()

        # Update scrollregion dynamically
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

    def _on_mousewheel(self, event):
        """Enable scrolling with the mouse wheel."""
        self.canvas.yview_scroll(-1 * (event.delta // 120), "units")

    def display_books(self):
        """Display available books with checkboxes for selection."""
        # Clear previous widgets if refreshing
        for widget in self.book_widgets:
            widget.destroy()
        self.book_widgets.clear()

        # Retrieve books
        books = self.retrieve_books()
        self.check_vars = []

        for i, book in enumerate(books):
            # book_id, book_name, isbn, authors, publisher, category = book.values()
            book_id = book["b_id"]
            authors = book["authors"]
            book_name = book["b_name"]
            isbn = book["isbn"]
            publisher = book["pub"]
            category = book["category"]

            # Create a frame for each book
            book_frame = ttk.Frame(self.scrollable_frame, padding=10, borderwidth=2, relief="solid")
            book_frame.grid(row=i, column=0, columnspan=4, sticky="w", padx=20, pady=10)
            self.book_widgets.append(book_frame)

            # Create a frame for book details
            details_frame = ttk.Frame(book_frame)
            details_frame.grid(row=0, column=0, sticky="w", padx=5, pady=5)

            # Display book details
            authors_str = ", ".join(authors)  # Combine authors into a single string

            # Title Row
            title_label = ttk.Label(details_frame, text=f"Title: {book_name}", font=("Helvetica", 10, "bold"))
            title_label.grid(row=0, column=0, sticky="w", padx=5, pady=2)

            # Authors Row
            authors_label = ttk.Label(details_frame, text=f"by: {authors_str}", font=("Helvetica", 10))
            authors_label.grid(row=1, column=0, sticky="w", padx=5, pady=2)

            # ISBN and Publisher Row
            details_label = ttk.Label(
                details_frame,
                text=f"ISBN: {isbn}   Publisher: {publisher}",
                font=("Helvetica", 10)
            )
            details_label.grid(row=2, column=0, columnspan=4, sticky="w", padx=5, pady=2)

            # Checkbox for selecting the book
            var = tk.IntVar()
            checkbox = ttk.Checkbutton(
                self.scrollable_frame,
                text="",
                variable=var,
                command=lambda var=var, book=book: self.limit_selection(var, book)
            )
            checkbox.grid(row=i, column=5, padx=5, pady=10, sticky="e")
            self.book_widgets.append(checkbox)
            self.check_vars.append(var)

        self.scrollable_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def retrieve_books(self):
        """Retrieve books that are free during the selected timeslot via API."""
        data = self.controller.data
        start_time = data.get('stime')  # Expected format: "YYYY-MM-DD HH:MM:SS"
        end_time = data.get('etime')

        if not start_time or not end_time:
            return []

        # Make API call to fetch available books
        response = self.controller.request_api(
            endpoint="/available-books",
            method="GET",
            params={"start_time": start_time, "end_time": end_time}
        )

        if response and response.get("success"):
            print(response,response["books"])
            return response["books"]
        else:
            messagebox.showerror("Error", response.get("error", "Failed to fetch books."))
            return []

    def limit_selection(self, var, book):
        """Limit the number of selected books to 3."""
        if var.get() == 1:
            if len(self.selected_books) < 3:
                self.selected_books.append(book)
            else:
                var.set(0)
                messagebox.showwarning("Selection Limit", "You can only select up to 3 books.")
        else:
            self.selected_books.remove(book)

    def confirm_selection(self):
        """Confirm the book selection and proceed."""
        if not self.selected_books:
            messagebox.showinfo("No Selection", "Please select at least one book.")
        else:
            selected_titles = [book["b_name"] for book in self.selected_books]
            self.controller.data['selected_books'] = self.selected_books
            messagebox.showinfo("Books Selected", f"Selected books: {', '.join(selected_titles)}")
            self.controller.show_frame(BookingFinalizePage)

    def refresh(self):
        """Clear and refresh the book display."""
        self.selected_books = []
        self.display_books()



class BookingFinalizePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Title
        ttk.Label(self, text="Finalize Booking", font=("Helvetica", 16, "bold")).pack(pady=20)

        # Booking summary section
        self.summary_frame = ttk.Frame(self, borderwidth=2, relief="groove", padding=10)
        self.summary_frame.pack(fill="x", padx=20, pady=10)

        self.display_summary()

        # Buttons
        self.button_frame = ttk.Frame(self)
        self.button_frame.pack(pady=20)

        confirm_button = ttk.Button(self.button_frame, text="Confirm Booking", command=self.confirm_booking)
        confirm_button.grid(row=0, column=0, padx=10, pady=10)

        back_button = ttk.Button(self.button_frame, text="Back", command=lambda: controller.show_frame(BookingAddBookPage))
        back_button.grid(row=0, column=1, padx=10, pady=10)

    def display_summary(self):
        """Display the selected seat and book details."""
        booking_data = self.controller.data
        seat_info = booking_data.get("cur_seat_info", {})
        books = booking_data.get("selected_books", [])

        for widget in self.summary_frame.winfo_children():
            widget.destroy()

        # Seat information
        ttk.Label(self.summary_frame, text="Seat Information", font=("Helvetica", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=10)
        ttk.Label(self.summary_frame, text=f"Seat No: {seat_info.get('seat_no', 'N/A')}").grid(row=1, column=0, sticky="w")
        ttk.Label(self.summary_frame, text=f"Location: {seat_info.get('location', 'N/A')}").grid(row=2, column=0, sticky="w")
        ttk.Label(self.summary_frame, text=f"Start Time: {booking_data.get('stime', 'N/A')}").grid(row=3, column=0, sticky="w")
        ttk.Label(self.summary_frame, text=f"End Time: {booking_data.get('etime', 'N/A')}").grid(row=4, column=0, sticky="w")

        # Book information
        ttk.Label(self.summary_frame, text="Selected Books", font=("Helvetica", 14, "bold")).grid(row=5, column=0, columnspan=2, pady=10)

        if not books:
            ttk.Label(self.summary_frame, text="No books selected.").grid(row=6, column=0, sticky="w")
        else:
            for i, book in enumerate(books, start=7):
                ttk.Label(self.summary_frame, text=f"- {book['b_name']}").grid(row=i, column=0, sticky="w")

    def confirm_booking(self):
        """Confirm the booking and send data to the backend."""
        booking_data = self.controller.data
        payload = {
            "student_id": booking_data.get("student_id"),
            "seat_id": booking_data.get("cur_seat_info", {}).get("seat_id"),
            "start_time": booking_data.get("stime"),
            "end_time": booking_data.get("etime"),
            "books": [book["b_id"] for book in booking_data.get("selected_books", [])]
        }

        response = self.controller.request_api(endpoint="/create-booking", method="POST", data=payload)

        if response and response.get("success"):
            messagebox.showinfo("Success", "Booking confirmed successfully!")
            id = booking_data.get("student_id")
            self.controller.data = {'stime': "", 'etime': "", 'cur_seat_info': 
                                    {'location': "", 'seat_no': None, 'seat_id': None}, 'Book_logs': [],
                                    "student_id":id}
            self.controller.show_frame(HomePage)
        else:
            messagebox.showerror("Error", response["error"] if response else "Failed to confirm booking.")

    def refresh(self):
        """Refresh the summary section when accessed."""
        self.display_summary()

class BookingHistoryPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Create a canvas and a scrollbar for scrolling
        self.canvas = tk.Canvas(self, height=800, width=580)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Create a scrollable frame inside the canvas
        self.scrollable_frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # Pack canvas and scrollbar
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Bind scroll wheel events to the canvas
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)  # For Windows
        self.canvas.bind_all("<Button-4>", self._on_mousewheel)  # For Linux (scroll up)
        self.canvas.bind_all("<Button-5>", self._on_mousewheel)  # For Linux (scroll down)

        # Update the scrollable frame's size dynamically
        self.scrollable_frame.bind("<Configure>", self._on_frame_configure)

        # Title label
        ttk.Label(self.scrollable_frame, text="Booking History", font=("Helvetica", 16, "bold")).pack(pady=10)

        # Results area for booking history
        self.history_frame = ttk.Frame(self.scrollable_frame)
        self.history_frame.pack(fill="both", expand=True)

        # Back button
        ttk.Button(self.scrollable_frame, text="Back", command=lambda: controller.show_frame(HomePage)).pack(pady=20)

    def _on_mousewheel(self, event):
        """Handle mouse wheel scrolling."""
        if event.num == 4:  # Linux scroll up
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5:  # Linux scroll down
            self.canvas.yview_scroll(1, "units")
        else:  # Windows
            self.canvas.yview_scroll(-1 * (event.delta // 120), "units")

    def _on_frame_configure(self, event):
        """Update the canvas scroll region to fit the scrollable frame."""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def fetch_and_display_history(self):
        """Fetch and display booking history."""
        student_id = self.controller.data.get("student_id")

        response = self.controller.request_api(
            endpoint="/booking-history",
            method="GET",
            params={"student_id": student_id}
        )

        if response and response.get("success"):
            bookings = self.group_bookings(response["bookings"])
            self.display_history(bookings)
        else:
            messagebox.showerror("Error", response.get("error", "Failed to fetch booking history."))

    def group_bookings(self, rows):
        """Group rows by booking and aggregate book details."""
        bookings = {}

        for row in rows:
            key = (row["seat_no"], row["location"], row["start_time"], row["end_time"])
            if key not in bookings:
                bookings[key] = {
                    "seat_no": row["seat_no"],
                    "location": row["location"],
                    "start_time": row["start_time"],
                    "end_time": row["end_time"],
                    "books": []
                }
            if row["b_name"]:
                bookings[key]["books"].append({
                    "b_name": row["b_name"],
                    "isbn": row["isbn"],
                    "authors": row["authors"],
                    "pub": row["publisher"]
                })

        return list(bookings.values())

    def display_history(self, bookings):
        """Display the booking history in the scrollable frame."""
        for widget in self.history_frame.winfo_children():
            widget.destroy()

        if not bookings:
            ttk.Label(self.history_frame, text="No bookings found.", font=("Helvetica", 12)).pack(pady=10)
            return

        for booking in bookings:
            seat_info = {
                "seat_no": booking["seat_no"],
                "seat_loc": booking["location"],
                "start_time": booking["start_time"],
                "end_time": booking["end_time"]
            }
            books = booking["books"]

            booking_details = BookingDetailsWithoutScroll(self.history_frame, seat_info, books)
            booking_details.pack(fill="x", pady=10)

    def refresh(self):
        """Refresh the booking history when the page is accessed."""
        self.fetch_and_display_history()


class BookingDetails(tk.Frame):
    def __init__(self, parent, seat_info, books):
        super().__init__(parent)

        # Create canvas and scrollbar
        canvas = tk.Canvas(self)  # Set canvas width to make the frame wider
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        # Configure canvas
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Make the scrollable frame an attribute
        self.scrollable_frame = scrollable_frame

        # Bold font
        bold_font = Font(weight="bold", size=11)

        # Seat details
        ttk.Label(scrollable_frame, text="Seat Details", padding=10, font=bold_font).pack(side="top", anchor="w")
        seat_frame = ttk.Frame(scrollable_frame, padding=10, borderwidth=2, relief="solid")
        seat_frame.pack(side="top", fill="x", pady=10)

        ttk.Label(seat_frame, text=f"Seat No:", padding=(5, 5), font=bold_font).grid(row=0, column=0, sticky="w", padx=10)
        ttk.Label(seat_frame, text=f"{seat_info['seat_no']}", padding=(5, 5)).grid(row=0, column=1, sticky="w", padx=10)
        ttk.Label(seat_frame, text=f"Seat Location:", padding=(5, 5), font=bold_font).grid(row=1, column=0, sticky="w", padx=10)
        ttk.Label(seat_frame, text=f"{seat_info['seat_loc']}", padding=(5, 5)).grid(row=1, column=1, sticky="w", padx=10)
        ttk.Label(seat_frame, text=f"Start Time:", padding=(5, 5), font=bold_font).grid(row=2, column=0, sticky="w", padx=10)
        ttk.Label(seat_frame, text=f"{seat_info['start_time'].strip()}", padding=(5, 5)).grid(row=2, column=1, sticky="w", padx=10)
        ttk.Label(seat_frame, text=f"End Time:", padding=(5, 5), font=bold_font).grid(row=3, column=0, sticky="w", padx=10)
        ttk.Label(seat_frame, text=f"{seat_info['end_time'].strip()}", padding=(5, 5)).grid(row=3, column=1, sticky="w", padx=10)

        # Book details
        ttk.Label(scrollable_frame, text="Book Details", padding=10, font=bold_font).pack(side="top", anchor="w")
        for book in books:
            book_frame = ttk.Frame(scrollable_frame, padding=10, borderwidth=2, relief="solid")
            book_frame.pack(side="top", fill="x", pady=5)
            authours = f"{', '.join(book['authors'])}"
            if len(authours) >20 :authours = authours[:20]+"..."
            ttk.Label(book_frame, text=f"Book Name:", padding=(5, 5), font=bold_font).grid(row=0, column=0, sticky="w", padx=10)
            ttk.Label(book_frame, text=f"{book['b_name']}", padding=(5, 5)).grid(row=0, column=1, sticky="w", padx=10)
            ttk.Label(book_frame, text=f"ISBN:", padding=(5, 5), font=bold_font).grid(row=1, column=0, sticky="w", padx=10)
            ttk.Label(book_frame, text=f"{book['isbn']}", padding=(5, 5)).grid(row=1, column=1, sticky="w", padx=10)
            ttk.Label(book_frame, text=f"Publisher:", padding=(5, 5), font=bold_font).grid(row=2, column=0, sticky="w", padx=10)
            ttk.Label(book_frame, text=f"{book['pub']}", padding=(5, 5)).grid(row=2, column=1, sticky="w", padx=10)
            ttk.Label(book_frame, text=f"Authors:", padding=(5, 5), font=bold_font).grid(row=3, column=0, sticky="w", padx=10)
            ttk.Label(book_frame, text=authours, padding=(5, 5)).grid(row=3, column=1, sticky="w", padx=10)

    def refresh(self):
        pass

class BookingDetailsWithoutScroll(tk.Frame):
    def __init__(self, parent, seat_info, books):
        super().__init__(parent)

        # Create a frame for the seat and book details
        self.scrollable_frame = ttk.Frame(self, padding=10)

        # Bold font
        bold_font = Font(weight="bold", size=11)

        # Seat details
        ttk.Label(self.scrollable_frame, text="Seat Details", padding=10, font=bold_font).pack(side="top", anchor="w")
        seat_frame = ttk.Frame(self.scrollable_frame, padding=10, borderwidth=2, relief="solid")
        seat_frame.pack(side="top", fill="x", pady=10)

        ttk.Label(seat_frame, text=f"Seat No:", padding=(5, 5), font=bold_font).grid(row=0, column=0, sticky="w", padx=10)
        ttk.Label(seat_frame, text=f"{seat_info['seat_no']}", padding=(5, 5)).grid(row=0, column=1, sticky="w", padx=10)
        ttk.Label(seat_frame, text=f"Seat Location:", padding=(5, 5), font=bold_font).grid(row=1, column=0, sticky="w", padx=10)
        ttk.Label(seat_frame, text=f"{seat_info['seat_loc']}", padding=(5, 5)).grid(row=1, column=1, sticky="w", padx=10)
        ttk.Label(seat_frame, text=f"Start Time:", padding=(5, 5), font=bold_font).grid(row=2, column=0, sticky="w", padx=10)
        ttk.Label(seat_frame, text=f"{seat_info['start_time']}", padding=(5, 5)).grid(row=2, column=1, sticky="w", padx=10)
        ttk.Label(seat_frame, text=f"End Time:", padding=(5, 5), font=bold_font).grid(row=3, column=0, sticky="w", padx=10)
        ttk.Label(seat_frame, text=f"{seat_info['end_time']}", padding=(5, 5)).grid(row=3, column=1, sticky="w", padx=10)

        # Book details
        if books:
            ttk.Label(self.scrollable_frame, text="Book Details", padding=10, font=bold_font).pack(side="top", anchor="w")
        for book in books:
            book_frame = ttk.Frame(self.scrollable_frame, padding=10, borderwidth=2, relief="solid")
            book_frame.pack(side="top", fill="x", pady=5)
            authors = f"{', '.join(book['authors'])}"
            if len(authors) > 20:
                authors = authors[:20] + "..."
            ttk.Label(book_frame, text=f"Book Name:", padding=(5, 5), font=bold_font).grid(row=0, column=0, sticky="w", padx=10)
            ttk.Label(book_frame, text=f"{book['b_name']}", padding=(5, 5)).grid(row=0, column=1, sticky="w", padx=10)
            ttk.Label(book_frame, text=f"ISBN:", padding=(5, 5), font=bold_font).grid(row=1, column=0, sticky="w", padx=10)
            ttk.Label(book_frame, text=f"{book['isbn']}", padding=(5, 5)).grid(row=1, column=1, sticky="w", padx=10)
            ttk.Label(book_frame, text=f"Publisher:", padding=(5, 5), font=bold_font).grid(row=2, column=0, sticky="w", padx=10)
            ttk.Label(book_frame, text=f"{book['pub']}", padding=(5, 5)).grid(row=2, column=1, sticky="w", padx=10)
            ttk.Label(book_frame, text=f"Authors:", padding=(5, 5), font=bold_font).grid(row=3, column=0, sticky="w", padx=10)
            ttk.Label(book_frame, text=authors, padding=(5, 5)).grid(row=3, column=1, sticky="w", padx=10)

        # Pack the frame into the parent container
        self.scrollable_frame.pack(fill="x", pady=10)

    def refresh(self):
        pass

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Title
        ttk.Label(self, text="Welcome to Library Booking System", font=("Helvetica", 16, "bold")).pack(pady=20)

        # Current Booking Section
        self.current_booking_frame = ttk.Frame(self, borderwidth=2, relief="groove", padding=(10, 10))
        self.current_booking_frame.pack(fill="x", padx=20, pady=10)

        ttk.Label(self.current_booking_frame, text="Current Booking", font=("Helvetica", 14, "bold")).pack(side="top", pady=10)
        self.booking_details = None  # Placeholder for BookingDetails

        # Buttons Section
        self.button_frame = ttk.Frame(self)
        self.button_frame.pack(pady=20)

        ttk.Button(self.button_frame, text="View Booking History", command=self.view_booking_history).grid(row=0, column=0, padx=10, pady=10)
        ttk.Button(self.button_frame, text="Create New Booking", command=self.create_new_booking).grid(row=0, column=1, padx=10, pady=10)
        ttk.Button(self.button_frame, text="Logout", command=self.logout).grid(row=0, column=2, padx=10, pady=10)
        ttk.Button(self.button_frame, text="refresh", command=self.refresh).grid(row=0, column=3, padx=10, pady=10)
        self.flag = 0    

    def refresh(self):
        """Refreshes the HomePage to display the current booking."""
        self.fetch_current_booking()

    def fetch_current_booking(self):
        """Fetch the current booking details from the backend."""
        student_id = self.controller.data.get("student_id")
        response = self.controller.request_api(
            endpoint="/current-booking",
            method="GET",
            params={"student_id": student_id}
        )
        self.s = None
        if self.booking_details:
            self.booking_details.destroy()
        if self.s: 
            self.s.destroy()
        if response and response.get("success"):
            booking = response.get("current_booking")
            if booking:
                # Display current booking
                seat_info = {
                    "seat_no": booking["seat_no"],
                    "seat_loc": booking["location"],
                    "start_time": booking["start_time"],
                    "end_time": booking["end_time"]
                }
                books = [
                    {
                        "b_name": book["b_name"],
                        "isbn": book["isbn"],
                        "pub": book["publisher"],
                        "authors": book["authors"]
                    }
                    for book in booking["books"]
                ]
                self.booking_details = BookingDetails(self.current_booking_frame, seat_info, books)
                self.booking_details.pack(side="top", fill="x", padx=10, pady=10)
            else:
                if self.flag == 0:
                    self.s = ttk.Label(self.current_booking_frame, text="No current booking available.", font=("Helvetica", 12))
                    self.s.pack()
                    self.flag = 1
        else:
            messagebox.showerror("Error", response.get("error", "Failed to fetch current booking."))

    def view_booking_history(self):
        """Navigate to the BookingHistoryPage."""
        self.controller.show_frame(BookingHistoryPage)

    def create_new_booking(self):
        """Navigate to the BookingTimeSlotPage."""
        self.controller.show_frame(BookingTimeSlotPage)

    def logout(self):
        """Logs out the user and navigates to the LoginPage."""
        self.controller.data = {'stime': "", 'etime': "", 'cur_seat_info': {'location': "", 'seat_no': None, 'seat_id': None}, 'Book_logs': []}
        self.controller.show_frame(LoginPage)

if __name__ == "__main__":
    app = windows()
    app.mainloop()