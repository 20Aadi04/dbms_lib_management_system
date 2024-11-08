import tkinter as tk
from tkinter import ttk
from tkSliderWidget import Slider


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
            self.controller.show_frame(BookingPage)
        else : 
            self.student_id_entry.selection_clear()
            
            print("wrong password")
    def reg(self):
        pass

class BookingPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        slider = Slider(
            self,
            width=400,
            height=60,
            min_val=0,
            max_val=900,
            init_lis=[0,30],
            show_value=True,
            # removable=True,
            # addable=True,
        )

        # optionally add a callback on value change
        slider.setValueChangeCallback(lambda vals: print(vals))

        slider.pack()
    def correct_slider():
        pass
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