import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import font
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
                self.controller.show_frame(BookingTimeSlotPage)
            else :
                messagebox.showerror("Error", "user id not found")
    
        

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
                cur.execute(f"insert into student(student_id,fname,lname,dob,grad_type,permitted_book_count,email,phone_num) values ('{student_id}','{first_name}','{last_name}','{dob}','{grad_type}',3,'{email}','{phone_number}')")
            self.controller.conn.commit()
            messagebox.showinfo("Registration", "Registration Successful")
            self.controller.show_frame(LoginPage)
        else:
            messagebox.showerror("Error", "Please Enter data properly")

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
    
class ScrollableTable(tk.Frame):
    def __init__(self,parent,Widget,callback,infos):

        self.Widget = Widget
        self.callback = callback
        tk.Frame.__init__(self, parent)

        self.canvas = tk.Canvas(self)
        
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
        ttk.Button(self,text="back",command=lambda : controller.show_frame(LoginPage) ).grid(row = 5 , column=0, pady=10, padx=10)
    
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

class BookingAddBookPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.selected_books = []
        self.confirm_button = ttk.Button(self, text="Confirm Selection", command=self.confirm_selection)
        self.confirm_button.pack(pady=10)

        self.canvas = tk.Canvas(self)
        self.scrollbar_y = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar_y.set)
        
        # self.scrollbar_x = ttk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)
        # self.canvas.configure(xscrollcommand=self.scrollbar_x.set)

        self.scrollable_frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.scrollbar_y.pack(side="right", fill="y")
        # self.scrollbar_x.pack(side="bottom", fill="x")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.create_table_headers()
        self.display_books()
        
        # Create a separate frame for the button and use grid on it
        

    def create_table_headers(self):
        headers = ["Book Name", "Author", "ISBN", "Publisher", "Select"]
        for col, header in enumerate(headers):
            label = ttk.Label(self.scrollable_frame, text=header, font=('Helvetica', 12, 'bold'), anchor="center")
            label.grid(row=0, column=col, padx=5, pady=10)

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
                label.grid(row=i, column=col, padx=5, pady=5)

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
        with self.controller.conn.cursor() as cur:
            cur.execute("SELECT * FROM book;")
            return cur.fetchall()

    def confirm_selection(self):
        if not self.selected_books:
            messagebox.showinfo("No Selection", "Please select at least one book.")
        else:
            windows.data['Book_logs'] = self.selected_books
            selected_titles = [book[1] for book in self.selected_books]
            self.controller.data['selected_books'] =self.selected_books
            messagebox.showinfo("Books Selected", f"Selected books: {', '.join(selected_titles)}")
            self.controller.show_frame(BookingFinalizepage)
            # Implement save or further processing of selected_books here

        
class BookingFinalizepage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.display_summary()

    def display_summary(self):
        print(self.controller.data)
        bold_font = font.Font(weight="bold")

        summary = ttk.Label(self, text="Summary",font = bold_font)
        summary.grid(row=0, column=0, pady=20, padx=0)
        ttk.Label(self, text="Start Time:").grid(row=1, column=0, pady=0, padx=0)
        ttk.Label(self, text=self.controller.data['stime'].strip()).grid(row=1, column=1, pady=0, padx=0)
        ttk.Label(self, text="End Time:").grid(row=2, column=0, pady=0, padx=0)
        ttk.Label(self, text=self.controller.data['etime'].strip()).grid(row=2, column=1, pady=0, padx=0)

        ttk.Label(self,text = "Seat Number: ").grid(row = 3, column = 0, padx = 0, pady = 0)
        ttk.Label(self,text = self.controller.data['cur_seat_info']['seat_no']).grid(row = 3, column = 1, padx = 0, pady = 0)
        ttk.Label(self,text = "Seat location: ").grid(row = 4, column = 0, padx = 0, pady = 0)
        ttk.Label(self,text = self.controller.data['cur_seat_info']['location']).grid(row = 4, column = 1, padx = 0, pady = 0)

        ttk.Label(self, text="Book Logs", font=bold_font).grid(row=5, column=0, padx=0, pady=0)
        # ttk.Label(self, text="Book ID", font=bold_font).grid(row=6, column=0, padx=0, pady=0)
        ttk.Label(self, text="Book Name", font=bold_font).grid(row=6, column=0, padx=0, pady=0)
        ttk.Label(self, text="ISBN", font=bold_font).grid(row=6, column=1, padx=0, pady=0)
        ttk.Label(self, text="Authors", font=bold_font).grid(row=6, column=2, padx=0, pady=0)
        ttk.Label(self, text="Publication", font=bold_font).grid(row=6, column=3, padx=0, pady=0)
        # ttk.Label(self, text="Category", font=bold_font).grid(row=6, column=4, padx=0, pady=0)

        row_count = 7
        for i in self.controller.data['Book_logs']:
            for j in range(1,len(i)-1):
                ttk.Label(self,text = str(i[j])).grid(row = row_count, column = j-1,padx = 0, pady = 0)
            row_count += 1  

        discard_button = ttk.Button(self, text="Discard Booking", command=self.discard)
        discard_button.grid(row=row_count + 1, column=0, pady=20, padx=0)

        finish_registration = ttk.Button(self, text="Finish Booking", command=self.finish)
        finish_registration.grid(row=row_count + 1, column=1, pady=20, padx=0)

    def discard(self):
        dump = messagebox.askyesno("CONFIRM","BOOKING WILL BE CANCELLED, DO YOU WANT TO PROCEED ?")
        if dump == True:
            self.controller.data.clear()
            # Type the required query here
            self.controller.show_frame(LoginPage)
    
    def finish(self):
        messagebox.showinfo("SUCCESS","BOOKING SUCCESSFUL")
        # Type the required query here
        self.controller.destroy()
            




class BookingInformationPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller


class windows(tk.Tk):
    data = dict()
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        # Adding a title to the window
        self.wm_title("Library Seat Management app")
        self.geometry("550x500")
        
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
        for F in (LoginPage,BookingTimeSlotPage,RegistrationPage,BookingAddBookPage,BookingFinalizepage,BookingInformationPage,HomePage):
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
        if(cont ==BookingAddBookPage):
            frame.pack(fill ='both')
        else :
            frame.pack( )

    def on_closing(self): 
        self.conn.close()
        self.destroy()
    

if __name__ == "__main__":
    app = windows()
    app.mainloop()