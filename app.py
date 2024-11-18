import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.font import Font
from RangeSlider.RangeSlider import RangeSliderH
from datetime import timedelta, datetime
import os
import psycopg2
from dotenv import load_dotenv
from tkcalendar import DateEntry


## template
# class MainPage(tk.Frame):
#     def __init__(self, parent, controller):
#         tk.Frame.__init__(self, parent)
#         self.controller = controller
#         label = tk.Label(self, text="Main Page")
#         label.pack(padx=10, pady=10)
#         # We use the switch_window_button in order to call the show_frame() method as a lambda function
#         switch_window_button = tk.Button(
#             self,
#             text="Go to the Side Page",
#             command=lambda: controller.show_frame(SidePage),
#         )
#         switch_window_button.pack(side="bottom", fill=tk.X)

class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        ttk.Label(self, text="Student ID: ").grid(row=0, column=0, pady=20, padx=10)
        self.student_id_entry = ttk.Entry(self)
        self.student_id_entry.insert(0,"20220007")
        self.student_id_entry.grid(row=0, column=1, pady=20, padx=10)
        
        ttk.Label(self, text="Password: ").grid(row=1, column=0, pady=20, padx=10)
        self.password_entry = ttk.Entry(self, show="*")
        self.password_entry.grid(row=1, column=1, pady=20, padx=10)

        ttk.Button(self, text="Login", command=self.login).grid(row=2, column=1, pady=20, padx=10)
        ttk.Button(self, text="Register", command=lambda: controller.show_frame(RegistrationPage)).grid(row=3, column=1, pady=20, padx=10)
    def login(self):
        if(self.student_id_entry.get() == ''):
            messagebox.showerror("Error", "user id cannot be empty")
            return
        with self.controller.conn.cursor() as cur:
            cur.execute(f"select * from student where student_id = '{self.student_id_entry.get()}'")
            user_data = cur.fetchone()
            if(user_data):
                self.controller.data['user_data'] = user_data
                self.controller.data['student_id'] = self.student_id_entry.get()
                self.controller.show_frame(HomePage)
            else :
                messagebox.showerror("Error", "user id not found")
    def refresh(self):
        pass
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

        ttk.Label(self, text="Graduation Type: ").grid(row=5, column=0,  pady=10, padx=10)
        self.grad_type_var = tk.StringVar() 
        self.grad_type_combobox = ttk.Combobox(self,textvariable = self.grad_type_var)
        # self.grad_type_entry = ttk.Entry(self)
        self.grad_type_combobox['values'] = ('FIRST DEGREE','SECOND DEGREE')
        self.grad_type_combobox.current(0)
        self.grad_type_combobox.grid(row=5, column=1, pady=10, padx=10)

        ttk.Label(self, text="Date of Birth: ").grid(row=6, column=0, pady=10, padx=10)
        # self.dob_entry = ttk.Entry(self)
        self.dob_entry = DateEntry(self,date_pattern="yyyy-mm-dd")
        self.dob_entry.grid(row=6, column=1, pady=10, padx=10)

        ttk.Label(self, text="Create a Password: ").grid(row=7, column=0, pady=10, padx=10)
        self.password_entry_reg = ttk.Entry(self, show="*")
        self.password_entry_reg.grid(row=7, column=1, pady=10, padx=10)

        ttk.Button(self, text="Submit", command=self.submit_registration).grid(row=8, column=1, pady=20)
    def submit_registration(self):
        first_name = self.first_name_entry.get()
        last_name =  self.last_name_entry.get()
        student_id =  self.student_id_entry_reg.get()
        email =  self.email_entry.get()
        phone_number =  self.phone_number_entry.get()
        grad_type =  self.grad_type_var.get()
        dob =  self.dob_entry.get()
        if (first_name and last_name and student_id and email and phone_number and grad_type and dob):
            # regitster query
            with self.controller.conn.cursor() as cur:
                cur.execute(f"insert into student(student_id,fname,lname,dob,grad_type,email,phone_num) values ('{student_id}','{first_name}','{last_name}','{dob}','{grad_type}','{email}','{phone_number}')")
            self.controller.conn.commit()
            messagebox.showinfo("Registration", "Registration Successful")
            self.controller.show_frame(LoginPage)
        else:
            messagebox.showerror("Error", "Please Enter data properly")
    def refresh(self):
        pass

class SeatInfo(tk.Frame):
    """
    parent = parent frame \n
    callback = func(seat_info) to callback when button is clicked \n
    seat_info = {'location' : 'upper'/'lower' ,'seat_no' : 12,'seat_id' :13 }
    """
    def __init__(self,parent,_callback,seat_info ):
        tk.Frame.__init__(self, parent,highlightbackground="black",highlightthickness=1)
        ttk.Label(self,text= "location :").pack(side="left")
        ttk.Label(self,text= f"{seat_info['location']}").pack(side="left")
        ttk.Label(self,text= "seat no :").pack(side="left")
        ttk.Label(self,text= f"{seat_info['seat_no']}").pack(side="left")
        ttk.Button(self,text="select" ,command=lambda :_callback(seat_info)).pack(side='left')
    def refresh(self):
        pass
    
class ScrollableTable(tk.Frame):
    def __init__(self,parent,Widget,callback,infos):

        self.Widget = Widget
        self.callback = callback
        tk.Frame.__init__(self, parent)

        self.canvas = tk.Canvas(self,width=550,height=700)
        
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.widgets = []
        self.update(infos)

    def update(self,infos):
        for i in self.widgets: 
            print('removed')
            i.destroy()
        self.widgets = []
        for info in infos:
            print('added ' ,info)
            self.widgets.append(self.Widget(self.scrollable_frame,self.callback,info))
            self.widgets[-1].pack(side=tk.TOP, fill="x")
        self.tkraise()
    def refresh(self):
        pass

class BookingTimeSlotPage(tk.Frame):
    max_time_span = 4*60 #minutes
    min_time_span = 60 #minutes

    max_time = 600
    min_time = 0

    left_pointer = min_time
    right_pointer = min_time + min_time_span
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.hLeft = tk.DoubleVar(value = self.left_pointer)  
        self.hRight = tk.DoubleVar(value = self.right_pointer) 
        self.slider = RangeSliderH( self , [self.hLeft, self.hRight] , padX = 16,step_size=5,min_val=self.min_time,max_val=self.max_time,show_value=False) 
        self.hRight.trace_add('write',self.correct_slider)
        
        ttk.Label(self, text="Start Time: ").grid(row=0, column=0, pady=10, padx=10)

        self.time_start = tk.StringVar()
        start_time_label = ttk.Label(self,textvariable=self.time_start)
        start_time_label.grid(row=0, column=1, pady=10, padx=10)

        ttk.Label(self, text="End Time: ").grid(row=0, column=2, pady=10, padx=10)
        self.time_end = tk.StringVar()
        end_time_label = ttk.Label(self, textvariable= self.time_end)  
        end_time_label.grid(row=0, column=3, pady=10, padx=10)
        ttk.Button(self,text="search",command=self.search ).grid(row = 0 , column=4, pady=10, padx=10)
        self.slider.grid(row=1, column=0,columnspan=5)
        self.update_time_labels()
        # hLeft.trace_add('w',self.correct_lslider)
        self.table = ScrollableTable(self,SeatInfo,self.select_seat,[])
        self.table.grid(row = 3 , column=0, pady=10, padx=10,columnspan=5)
        ttk.Button(self,text="back",command=lambda : controller.show_frame(HomePage) ).grid(row = 5 , column=0, pady=10, padx=10)
    
    def select_seat(self,info):
        self.controller.data['cur_seat_info'] = info
        self.controller.show_frame(BookingAddBookPage)



    def correct_slider(self,*args):
        lp = self.hLeft.get()
        rp = self.hRight.get()
        if rp != self.right_pointer:
            if rp <= self.min_time_span:
                rp = self.min_time_span
            elif abs(lp-rp) > self.max_time_span:
                lp =rp-self.max_time_span
            elif abs(lp-rp) < self.min_time_span:
                lp = rp-self.min_time_span
        else :
            if lp >= self.max_time - self.min_time_span:
                lp = self.max_time - self.min_time_span
            elif abs(lp-rp) > self.max_time_span:
                rp =lp+self.max_time_span
            elif abs(lp-rp) < self.min_time_span:
                rp = lp+self.min_time_span
        self.left_pointer = lp 
        self.right_pointer = rp
        self.update_time_labels()
        self.slider.forceValues([lp, rp])
    def update_time_labels(self):
        tomorrow = datetime.now() + timedelta(days=1)
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

        windows.data['stime'] = start_time.strftime("\t%Y-%m-%d \t%H:%M")
        windows.data['etime'] = end_time.strftime("\t%Y-%m-%d \t%H:%M")
 
        with self.controller.conn.cursor() as cur:
            cur.execute( f"""SELECT seat_id ,location ,seat_no
                FROM seat
                WHERE seat_id NOT IN (
                    SELECT seat_id
                    FROM booking
                    WHERE (start_time < '{end_time.strftime("%Y-%m-%d %H:%M:%S")}' AND end_time > '{start_time.strftime("%Y-%m-%d %H:%M:%S")}'));"""
            )
            l = cur.fetchall()
            infos = [{'seat_id':seat_id,'location':location,'seat_no':seat_no} for (seat_id,location,seat_no) in l]
            self.table.update(infos)
    

    def place(self):
        tomorrow = datetime.now() + timedelta(days=1)
        tomorrow_at_8am = tomorrow.replace(hour=8, minute=0, second=0, microsecond=0)
        start_time = tomorrow_at_8am + timedelta(minutes=self.left_pointer)
        end_time = tomorrow_at_8am + timedelta(minutes=self.right_pointer)
        seat_id = int(input("enter seat no :"))

        insert_query = """
        INSERT INTO booking (student_id, seat_id, start_time, end_time)
        VALUES (%s, %s, %s, %s)
        """
        with self.controller.conn.cursor() as cur:
            cur.execute(insert_query, (self.controller.data['student_id'], seat_id, start_time, end_time))
        self.controller.conn.commit()
    def refresh(self):
        pass

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

        # Canvas and Scrollbar
        self.canvas = tk.Canvas(self, height= 700,width=550)
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
        # Clear previous widgets if refreshing
        for widget in self.book_widgets:
            widget.destroy()
        self.book_widgets.clear()

        books = self.retrieve_books()
        self.check_vars = []

        for i, book in enumerate(books):
            book_id, b_name, isbn, authors, publisher, category = book

            # Create a frame for each book (book details and checkbox are in separate sections)
            book_frame = ttk.Frame(self.scrollable_frame, padding=10, borderwidth=2, relief="solid")
            book_frame.grid(row=i, column=0, columnspan=4, sticky="w", padx=20, pady=10)
            self.book_widgets.append(book_frame)

            # Create a frame for book details
            details_frame = ttk.Frame(book_frame)
            details_frame.grid(row=0, column=0, sticky="w", padx=5, pady=5)

            # Display book details in the book frame
            authors_str = ", ".join(authors)  # Combine authors into a single string

            # Title Row
            title_label = ttk.Label(details_frame, text=f"Title: {b_name}", font=("Helvetica", 10, "bold"))
            title_label.grid(row=0, column=0, sticky="w", padx=5, pady=2)

            # Authors Row (on a new line)
            authors_label = ttk.Label(details_frame, text=f"by: {authors_str}", font=("Helvetica", 10))
            authors_label.grid(row=1, column=0, sticky="w", padx=5, pady=2)

            # ISBN and Publisher Row
            details_label = ttk.Label(
                details_frame,
                text=f"ISBN: {isbn}   Publisher: {publisher}",
                font=("Helvetica", 10)
            )
            details_label.grid(row=2, column=0, columnspan=4, sticky="w", padx=5, pady=2)

            # Create a checkbox for selecting the book (in column 5, outside the book frame)
            var = tk.IntVar()
            checkbox = ttk.Checkbutton(
                self.scrollable_frame,
                text="",
                variable=var,
                command=lambda var=var, book=book: self.limit_selection(var, book)
            )
            checkbox.grid(row=i, column=5, padx=5, pady=10, sticky="e")
            self.check_vars.append(var)

        self.scrollable_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def retrieve_books(self):
        # Mock database retrieval; replace with your actual DB query
        with self.controller.conn.cursor() as cur:
            cur.execute("SELECT DISTINCT * FROM book;")
            books = cur.fetchall()
            return books

    def limit_selection(self, var, book):
        if var.get() == 1:
            if len(self.selected_books) < 3:
                self.selected_books.append(book)
            else:
                var.set(0)
                messagebox.showwarning("Selection Limit", "You can only select up to 3 books.")
        else:
            self.selected_books.remove(book)

    def confirm_selection(self):
        if not self.selected_books:
            messagebox.showinfo("No Selection", "Please select at least one book.")
        else:
            selected_titles = [book[1] for book in self.selected_books]
            self.controller.data['selected_books'] = self.selected_books
            messagebox.showinfo("Books Selected", f"Selected books: {', '.join(selected_titles)}")
            self.controller.show_frame(BookingFinalizePage)

    def refresh(self):
        """Clear and refresh the book display."""
        self.display_books()
        self.selected_books = []








class BookingDetails(tk.Frame):
    def __init__(self, parent, seat_info, books):
        super().__init__(parent)

        # Create canvas and scrollbar
        canvas = tk.Canvas(self, width=530,height= 600)  # Set canvas width to make the frame wider
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
            ttk.Label(book_frame, text=f"{book['book_name']}", padding=(5, 5)).grid(row=0, column=1, sticky="w", padx=10)
            ttk.Label(book_frame, text=f"ISBN:", padding=(5, 5), font=bold_font).grid(row=1, column=0, sticky="w", padx=10)
            ttk.Label(book_frame, text=f"{book['isbn']}", padding=(5, 5)).grid(row=1, column=1, sticky="w", padx=10)
            ttk.Label(book_frame, text=f"Publisher:", padding=(5, 5), font=bold_font).grid(row=2, column=0, sticky="w", padx=10)
            ttk.Label(book_frame, text=f"{book['pub']}", padding=(5, 5)).grid(row=2, column=1, sticky="w", padx=10)
            ttk.Label(book_frame, text=f"Authors:", padding=(5, 5), font=bold_font).grid(row=3, column=0, sticky="w", padx=10)
            ttk.Label(book_frame, text=authours, padding=(5, 5)).grid(row=3, column=1, sticky="w", padx=10)

    def refresh(self):
        pass

    
class BookingFinalizePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.display_summary()

    def refresh(self):
        for i in list(self.children.values()):
            i.destroy()
        self.display_summary()

    def display_summary(self):
        bold_font = Font(weight="bold")
        ttk.Label(self, text="Booking Summary", font=bold_font).pack(pady=20)

        # Extract seat and book details from controller data
        seat_info = self.controller.data.get('cur_seat_info', {})
        seat_info_formatted = {
            "seat_no": seat_info.get('seat_no', 'N/A'),
            "start_time": self.controller.data.get('stime', 'N/A'),
            "end_time": self.controller.data.get('etime', 'N/A'),
            "seat_loc": seat_info.get('location', 'N/A')
        }

        selected_books = self.controller.data.get('selected_books', [])
        print(selected_books)
        books_formatted = [
            {
                "book_name": book[1],
                "isbn": book[2],
                "pub": book[4],
                "authors": book[3]
            }
            for book in selected_books
        ]
        print(seat_info,books_formatted)
        # Create and display the BookingDetails frame
        booking_details = BookingDetails(self, seat_info_formatted, books_formatted)
        booking_details.pack(fill="both", expand=True, pady=10, padx=10)

        # Add action buttons
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=20)

        ttk.Button(button_frame, text="Discard Booking", command=self.discard).grid(row=0, column=0, padx=10)
        ttk.Button(button_frame, text="Finish Booking", command=self.finish).grid(row=0, column=1, padx=10)

    def discard(self):
        dump = messagebox.askyesno("CONFIRM", "BOOKING WILL BE CANCELLED, DO YOU WANT TO PROCEED?")
        if dump:
            self.controller.data.clear()
            self.controller.show_frame(LoginPage)

    def finish(self):
        try:
            self.send_booking_data()
            messagebox.showinfo("SUCCESS", "BOOKING SUCCESSFUL")
            self.controller.data = {'stime':"",'etime':"",'cur_seat_info':{'location' : "" ,'seat_no' : None,'seat_id' :None },'Book_logs':[]}
            self.controller.show_frame(HomePage)
        except Exception as e:
            messagebox.showerror("ERROR", f"An error occurred: {e}")

    def send_booking_data(self):
        booking_data = {
            "start_time": self.controller.data['stime'],
            "end_time": self.controller.data['etime'],
            "seat_info": self.controller.data['cur_seat_info'],
            "selected_books": [
                {
                    "name": book[1],
                    "isbn": book[2],
                    "authors": book[3],
                    "publisher": book[4]
                }
                for book in self.controller.data.get('selected_books', [])
            ]
        }

        # Simulate sending data (replace this with actual sending logic)
        print("Sending booking data...")
        print(booking_data)

class BookingHistoryPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Title
        bold_font = Font(weight="bold", size=14)
        ttk.Label(self, text="Booking History", font=bold_font).pack(pady=20)

        # Scrollable area
        self.canvas = tk.Canvas(self,width=550,height=700)
        self.scrollbar_y = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar_y.set)

        self.scrollable_frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.scrollbar_y.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.refresh()

        # Back button
        ttk.Button(self, text="Back to Home", command=lambda: controller.show_frame(HomePage)).pack(pady=20)

    def refresh(self):
        """Displays booking history dynamically."""
        history = self.controller.data.get("booking_history", [])

        if not history:
            ttk.Label(self.scrollable_frame, text="No booking history available.", foreground="red").pack(pady=10)
            return

        bold_font = Font(weight="bold")
        for i, booking in enumerate(history):
            # Add a separator for each booking
            if i > 0:
                ttk.Separator(self.scrollable_frame, orient="horizontal").pack(fill="x", pady=10)

            seat_info = booking.get("seat_info", {})
            books = booking.get("books", [])

            # Booking Details
            ttk.Label(self.scrollable_frame, text=f"Booking {i + 1}", font=bold_font).pack(anchor="w", pady=5)
            ttk.Label(self.scrollable_frame, text=f"Seat No: {seat_info.get('seat_no', 'N/A')}").pack(anchor="w", padx=10)
            ttk.Label(self.scrollable_frame, text=f"Location: {seat_info.get('seat_loc', 'N/A')}").pack(anchor="w", padx=10)
            ttk.Label(self.scrollable_frame, text=f"Start Time: {seat_info.get('start_time', 'N/A')}").pack(anchor="w", padx=10)
            ttk.Label(self.scrollable_frame, text=f"End Time: {seat_info.get('end_time', 'N/A')}").pack(anchor="w", padx=10)

            # Books
            ttk.Label(self.scrollable_frame, text="Books:", font=bold_font).pack(anchor="w", padx=10, pady=(5, 0))
            if books:
                for book in books:
                    book_details = f"- {book['book_name']} (ISBN: {book['isbn']}, Publisher: {book['pub']})"
                    ttk.Label(self.scrollable_frame, text=book_details).pack(anchor="w", padx=20)
            else:
                ttk.Label(self.scrollable_frame, text="No books selected.").pack(anchor="w", padx=20)

        # Update the canvas scroll region
        self.scrollable_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))




class BookingInformationPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller    

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Title
        bold_font = Font(weight="bold", size=14)
        ttk.Label(self, text="Welcome to Booking System", font=bold_font).pack(pady=20)

        # Current Booking Section
        self.current_booking_frame = ttk.Frame(self, borderwidth=2, relief="groove", padding=(10, 10))
        self.current_booking_frame.pack(fill="x", padx=20, pady=10)

        ttk.Label(self.current_booking_frame, text="Current Booking", font=bold_font).pack(side="top", pady=10)
        self.booking_details = None  # Placeholder for the BookingDetails frame

        # Buttons
        self.button_frame = ttk.Frame(self)
        self.button_frame.pack(pady=20)

        ttk.Button(self.button_frame, text="View Booking History", command=self.show_booking_history).grid(row=0, column=0, padx=10, pady=10)
        ttk.Button(self.button_frame, text="Create New Booking", command=self.create_new_booking).grid(row=0, column=1, padx=10, pady=10)

    def refresh(self):
        """Updates the current booking display dynamically."""
        current_booking = self.controller.data.get("current_booking", None)

        if self.booking_details:
            self.booking_details.destroy()  # Remove the previous BookingDetails frame

        if current_booking:
            seat_info = current_booking.get("seat_info", {})
            seat_info_formatted = {
                "seat_no": seat_info.get("seat_no", "N/A"),
                "start_time": seat_info.get("start_time", "N/A"),
                "end_time": seat_info.get("end_time", "N/A"),
                "seat_loc": seat_info.get("seat_loc", "N/A")
            }

            books_formatted = [
                {
                    "book_name": book["book_name"],
                    "isbn": book["isbn"],
                    "pub": book["pub"],
                    "authors": book["authors"]
                }
                for book in current_booking.get("books", [])
            ]

            # Instantiate and pack BookingDetails
            self.booking_details = BookingDetails(self.current_booking_frame, seat_info_formatted, books_formatted)
            self.booking_details.pack(side="top", fill="x", padx=10, pady=10)

    def show_booking_history(self):
        """Navigates to the booking history page."""
        self.controller.show_frame(BookingHistoryPage)

    def create_new_booking(self):
        """Navigates to the new booking page."""
        self.controller.show_frame(BookingTimeSlotPage)



class windows(tk.Tk):
    data = {'stime':"",'etime':"",'cur_seat_info':{'location' : "" ,'seat_no' : None,'seat_id' :None },'Book_logs':[]}
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        # Adding a title to the window
        self.wm_title("Library Seat Management app")
        self.geometry("600x800")
        
        self.style = ttk.Style()
        self.style.configure('TLabel', font=('Helvetica', 12), padding=5)
        self.style.configure('TButton', font=('Helvetica', 10), padding=5)
        self.style.configure('TEntry', font=('Helvetica', 10), padding=5)

        # self.wm_minsize = (1280,720)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        # creating a frame and assigning it to container
        container = tk.Frame(self)
        # specifying the region where the frame is packed in root
        container.pack(side="top", fill="both")

        # configuring the location of the container using grid
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        # We will now create a dictionary of frames
        self.frames = {}

        load_dotenv()
        database_url = os.getenv('DATABASE_URL')
        self.conn = psycopg2.connect(database_url)
        # we'll create the frames themselves later but let's add the components to the dictionary.
        for F in (LoginPage,BookingHistoryPage,BookingTimeSlotPage,RegistrationPage,BookingAddBookPage,BookingFinalizePage,BookingInformationPage,HomePage):
            frame = F(container, self)

            # the windows class acts as the root window for the frames.
            self.frames[F] = frame
            # frame.grid(row=0, column=0)

   

        # Using a method to switch frames
        self.show_frame(LoginPage)
    def show_frame(self, cont):
        frame = self.frames[cont]
        # raises the current frame to the top
        for i in self.frames.values():
            i.pack_forget()
        frame.refresh()
        if(cont ==BookingAddBookPage):
            frame.pack(fill ='both')
        else :
            frame.pack()
        

    def on_closing(self): 
        self.conn.close()
        self.destroy()
    

if __name__ == "__main__":
    app = windows()
    app.mainloop()