import tkinter as tk
from tkinter import ttk, messagebox
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
#         label = tk.Label(self, text="Main Page")
#         label.pack(padx=10, pady=10)

#         # We use the switch_window_button in order to call the show_frame() method as a lambda function
        # switch_window_button = tk.Button(
        #     self,
        #     text="Go to the Side Page",
        #     command=lambda: controller.show_frame(SidePage),
        # )
#         switch_window_button.pack(side="bottom", fill=tk.X)

class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        ttk.Label(self, text="Student ID: ").grid(row=0, column=0, pady=20, padx=10)
        self.student_id_entry = ttk.Entry(self)
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
                self.controller.show_frame(BookingPage)
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

        ttk.Label(self, text="Graduation Type: ").grid(row=5, column=0, pady=10, padx=10)
        self.grad_type_entry = ttk.Entry(self)
        self.grad_type_entry.grid(row=5, column=1, pady=10, padx=10)

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
        grad_type =  self.grad_type_entry.get()
        dob =  self.dob_entry.get()
        if (first_name and last_name and student_id and email and phone_number and grad_type and dob):
            # regitster query
            with self.controller.conn.cursor() as cur:
                cur.execute(f"insert into student(student_id,fname,lname,dob,grad_type,email,phone_num) values ('{student_id}','{first_name}','{last_name}','{dob}','{grad_type}','{email}','{phone_number}')")
            self.controller.conn.commit()
            messagebox.showinfo("Registration", "Registration Successful")
        else:
            messagebox.showerror("Error", "Please Enter data properly")
    




    
class BookingPage(tk.Frame):
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
 
        with self.controller.conn.cursor() as cur:
            cur.execute( f"""SELECT seat_id
                FROM seat
                WHERE seat_id NOT IN (
                    SELECT seat_id
                    FROM booking
                    WHERE (start_time < '{end_time.strftime("%Y-%m-%d %H:%M:%S")}' AND end_time > '{start_time.strftime("%Y-%m-%d %H:%M:%S")}'));"""
            )
            l = cur.fetchall()
            print(l)
            

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

class windows(tk.Tk):
    data= dict()
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        # Adding a title to the window
        self.wm_title("Library Seat Management app")
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
        # we'll create the frames themselves later but let's add the components to the dictionary.
        for F in (LoginPage,BookingPage,RegistrationPage):
            frame = F(container, self)

            # the windows class acts as the root window for the frames.
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")


        load_dotenv()
        database_url = os.getenv('DATABASE_URL')
        self.conn = psycopg2.connect(database_url)

        # Using a method to switch frames
        self.show_frame(LoginPage)
    def show_frame(self, cont):
        frame = self.frames[cont]
        # raises the current frame to the top
        frame.tkraise()

    def on_closing(self): 
        self.conn.close()
        self.destroy()
    

if __name__ == "__main__":
    app = windows()
    app.mainloop()