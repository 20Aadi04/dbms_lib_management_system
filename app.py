import tkinter as tk
from tkinter import ttk
from RangeSlider.RangeSlider import RangeSliderH

## template
# class MainPage(tk.Frame):
#     def __init__(self, parent, controller):
#         tk.Frame.__init__(self, parent)
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
        self.student_id_entry.grid(row=0, column=1, pady=20, padx=10)
        
        ttk.Label(self, text="Password: ").grid(row=1, column=0, pady=20, padx=10)
        self.password_entry = ttk.Entry(self, show="*")
        self.password_entry.grid(row=1, column=1, pady=20, padx=10)

        ttk.Button(self, text="Login", command=self.login).grid(row=2, column=1, pady=20, padx=10)
        ttk.Button(self, text="Register", command=self.reg).grid(row=3, column=1, pady=20, padx=10)
    def login(self):
        if(self.student_id_entry.get() =='loki' and self.password_entry.get() == 'admin'):
            self.student_id_entry.selection_clear()
        else : 
            self.student_id_entry.selection_clear()
            print("wrong password")
        self.controller.show_frame(BookingPage)

    def reg(self):
        pass

class BookingPage(tk.Frame):
    max_time_span = 4*60 #minutes
    min_time_span = 60 #minutes
    left_pointer = 0
    right_pointer = 30
    max_time = 600
    min_time = 0 
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.hLeft = tk.DoubleVar(value = self.left_pointer)  
        self.hRight = tk.DoubleVar(value = self.right_pointer) 
        self.slider = RangeSliderH( self , [self.hLeft, self.hRight] , padX = 16,step_size=5,min_val=self.min_time,max_val=self.max_time,show_value=False) 
        self.hRight.trace_add('write',self.correct_slider)
        self.slider.pack()
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
        self.slider.forceValues([lp, rp])
    def update_time_labels():
        pass
class windows(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        # Adding a title to the window
        self.wm_title("Test Application")
        # self.wm_minsize = (1280,720)
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
        for F in (LoginPage,BookingPage):
            frame = F(container, self)

            # the windows class acts as the root window for the frames.
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Using a method to switch frames
        self.show_frame(LoginPage)
    def show_frame(self, cont):
        frame = self.frames[cont]
        # raises the current frame to the top
        frame.tkraise()

if __name__ == "__main__":
    app = windows()
    app.mainloop()