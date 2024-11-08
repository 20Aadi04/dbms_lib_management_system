import tkinter as tk
from tkinter import ttk, messagebox
from datetime import timedelta, datetime
import sys
sys.setrecursionlimit(2000)

def login():
    login_frame.pack_forget()
    time_slot_frame.pack(pady=40)

def register():
    login_frame.pack_forget()
    register_frame.pack(pady=20)

def submit_registration():
    first_name = first_name_entry.get()
    last_name = last_name_entry.get()
    student_id = student_id_entry_reg.get()
    email = email_entry.get()
    phone_number = phone_number_entry.get()
    grad_type = grad_type_entry.get()
    dob = dob_entry.get()

    if (first_name and last_name and student_id and email and phone_number and grad_type and dob):
        messagebox.showinfo("Registration", "Registration Successful")
        register_frame.pack_forget()
        login_frame.pack(pady=40)
    else:
        messagebox.showerror("Error", "Please Enter data properly")

def select_time_slot():
    time_slot_frame.pack_forget()
    seat_booking_frame.pack(pady=40)

def submit_booking():
    seat_number = seat_number_dropdown.get()
    seat_location = seat_location_dropdown.get()

    if (seat_number and seat_location):
        messagebox.showinfo("Booking", "Seat booked successfully!")
        root.destroy()
    else:
        messagebox.showerror("Error", "Choose a Valid Seat Number and Seat Location")

def update_time_labels(event=None):
    """Update the time labels as user adjusts the sliders."""
    # Ensure slider values are multiples of 5
    start_minutes = round(start_time_slider.get()) * 5
    end_minutes = round(end_time_slider.get()) * 5

    # Calculate time for each slider based on the starting hour (8:00 AM)
    tomorrow = datetime.now() + timedelta(days=1)
    tomorrow_at_8am = tomorrow.replace(hour=8, minute=0, second=0, microsecond=0)
    start_time = tomorrow_at_8am + timedelta(minutes=start_minutes)
    end_time = tomorrow_at_8am + timedelta(minutes=end_minutes)

    max_time_minutes = 900
    
    # Check if time difference is at least 30 minutes
    if (start_minutes > 900-30 ):
        start_time_slider.set((900-30) //5)
    elif (end_time - start_time).total_seconds() < 1800:
        end_time_slider.set((start_minutes // 5) + 6)  # Set end time 30 minutes ahead
    elif (end_time - start_time).total_seconds() > 7200:
        end_time_slider.set((start_minutes // 5) + 24)  # Limit to 2 hours max
    else:
        start_time_label.config(text=start_time.strftime("%H:%M"))
        end_time_label.config(text=end_time.strftime("%H:%M"))

root = tk.Tk()
root.title("Library Seat Management System")
root.geometry("600x600")

style = ttk.Style()
style.configure('TLabel', font=('Helvetica', 12), padding=5)
style.configure('TButton', font=('Helvetica', 10), padding=5)
style.configure('TEntry', font=('Helvetica', 10), padding=5)

# Login Frame
login_frame = ttk.Frame(root)

ttk.Label(login_frame, text="Student ID: ").grid(row=0, column=0, pady=20, padx=10)
student_id_entry = ttk.Entry(login_frame)
student_id_entry.grid(row=0, column=1, pady=20, padx=10)

ttk.Label(login_frame, text="Password: ").grid(row=1, column=0, pady=20, padx=10)
password_entry = ttk.Entry(login_frame, show="*")
password_entry.grid(row=1, column=1, pady=20, padx=10)

ttk.Button(login_frame, text="Login", command=login).grid(row=2, column=1, pady=20, padx=10)
ttk.Button(login_frame, text="Register", command=register).grid(row=3, column=1, pady=20, padx=10)

login_frame.pack(pady=40)

# Register Frame
register_frame = ttk.Frame(root)

ttk.Label(register_frame, text="First Name: ").grid(row=0, column=0, pady=10, padx=10)
first_name_entry = ttk.Entry(register_frame)
first_name_entry.grid(row=0, column=1, pady=10, padx=10)

ttk.Label(register_frame, text="Last Name: ").grid(row=1, column=0, pady=10, padx=10)
last_name_entry = ttk.Entry(register_frame)
last_name_entry.grid(row=1, column=1, pady=10, padx=10)

ttk.Label(register_frame, text="Student ID: ").grid(row=2, column=0, pady=10, padx=10)
student_id_entry_reg = ttk.Entry(register_frame)
student_id_entry_reg.grid(row=2, column=1, pady=10, padx=10)

ttk.Label(register_frame, text="Email: ").grid(row=3, column=0, pady=10, padx=10)
email_entry = ttk.Entry(register_frame)
email_entry.grid(row=3, column=1, pady=10, padx=10)

ttk.Label(register_frame, text="Phone Number: ").grid(row=4, column=0, pady=10, padx=10)
phone_number_entry = ttk.Entry(register_frame)
phone_number_entry.grid(row=4, column=1, pady=10, padx=10)

ttk.Label(register_frame, text="Graduation Type: ").grid(row=5, column=0, pady=10, padx=10)
grad_type_entry = ttk.Entry(register_frame)
grad_type_entry.grid(row=5, column=1, pady=10, padx=10)

ttk.Label(register_frame, text="Date of Birth: ").grid(row=6, column=0, pady=10, padx=10)
dob_entry = ttk.Entry(register_frame)
dob_entry.grid(row=6, column=1, pady=10, padx=10)

ttk.Label(register_frame, text="Create a Password: ").grid(row=7, column=0, pady=10, padx=10)
password_entry_reg = ttk.Entry(register_frame, show="*")
password_entry_reg.grid(row=7, column=1, pady=10, padx=10)

ttk.Button(register_frame, text="Submit", command=submit_registration).grid(row=8, column=1, pady=20)

# Time Slot Frame
time_slot_frame = ttk.Frame(root)

ttk.Label(time_slot_frame, text="Select Start Time: ").grid(row=0, column=0, pady=10, padx=10)
start_time_slider = ttk.Scale(time_slot_frame, from_=0, to=180, orient="vertical", command=update_time_labels, length=400)
start_time_slider.grid(row=1, column=0, pady=10, padx=10)
start_time_label = ttk.Label(time_slot_frame, text="08:00")
start_time_label.grid(row=2, column=0, pady=10, padx=10)

ttk.Label(time_slot_frame, text="Select End Time: ").grid(row=0, column=2, pady=10, padx=10)
end_time_slider = ttk.Scale(time_slot_frame, from_=6, to=180, orient="vertical", command=update_time_labels, length=400)
end_time_slider.grid(row=1, column=2, pady=10, padx=10)
end_time_label = ttk.Label(time_slot_frame, text="08:30")
end_time_label.grid(row=2, column=2, pady=10, padx=10)

ttk.Button(time_slot_frame, text="Select Time Slot", command=select_time_slot).grid(row=1, column=1, pady=20)

# Seat Booking Frame
seat_booking_frame = ttk.Frame(root)

ttk.Label(seat_booking_frame, text="Seat Number: ").grid(row=0, column=0, pady=10, padx=10)
seat_number_dropdown = ttk.Combobox(seat_booking_frame, values=[str(i) for i in range(1, 101)], state="readonly")
seat_number_dropdown.grid(row=0, column=1, pady=10, padx=10)

ttk.Label(seat_booking_frame, text="Seat Location: ").grid(row=1, column=0, pady=10, padx=10)
seat_location_dropdown = ttk.Combobox(seat_booking_frame, values=["Upper", "Lower"], state="readonly")
seat_location_dropdown.grid(row=1, column=1, pady=10, padx=10)

ttk.Button(seat_booking_frame, text="Submit Booking", command=submit_booking).grid(row=2, column=1, pady=20)

root.mainloop()
