import tkinter as tk
from tkinter import ttk, messagebox
from datetime import timedelta, datetime

# Initialize main application window
root = tk.Tk()
root.title("Library Seat Management System")
root.geometry("500x650")

# Style configuration for UI elements
style = ttk.Style()
style.configure('TLabel', font=('Helvetica', 11), padding=5)
style.configure('TButton', font=('Helvetica', 10), padding=5)
style.configure('TEntry', font=('Helvetica', 11), padding=5)

def go_to_time_booking():
    login_frame.pack_forget()
    time_booking_frame.pack(pady=20)

def login_user():
    student_id = student_id_entry.get()
    password = password_entry.get()
    
    if student_id == "admin" and password == "password":
        messagebox.showinfo("Login", "Login successful!")
        go_to_time_booking()
    else:
        messagebox.showerror("Login", "Invalid Student ID or Password")

def go_to_seat_booking():
    time_booking_frame.pack_forget()
    seat_booking_frame.pack(pady=20)

def submit_booking():
    seat_number = seat_number_combo.get()
    seat_location = seat_location_combo.get()
    if seat_number and seat_location:
        messagebox.showinfo("Submission", "Booking submitted successfully!")
    else:
        messagebox.showerror("Submission", "Please fill all fields.")

def update_time_labels(*args):
    # Update live time values from slider positions
    start_time_minutes = start_slider.get()
    end_time_minutes = end_slider.get()

    # Convert slider values to time strings
    start_time = (datetime(1, 1, 1, 8, 0) + timedelta(minutes=start_time_minutes)).time()
    end_time = (datetime(1, 1, 1, 8, 0) + timedelta(minutes=end_time_minutes)).time()
    
    start_time_label.config(text=f"Start Time: {start_time.strftime('%H:%M')}")
    end_time_label.config(text=f"End Time: {end_time.strftime('%H:%M')}")

    # Restrict max time gap to 2 hours
    if end_time_minutes - start_time_minutes > 120:
        end_slider.set(start_time_minutes + 120)

# Login Frame
login_frame = ttk.Frame(root)
ttk.Label(login_frame, text="StudentID:").grid(row=0, column=0, pady=10, padx=10)
student_id_entry = ttk.Entry(login_frame)
student_id_entry.grid(row=0, column=1, pady=10, padx=10)
ttk.Label(login_frame, text="Password:").grid(row=1, column=0, pady=10, padx=10)
password_entry = ttk.Entry(login_frame, show="*")
password_entry.grid(row=1, column=1, pady=10, padx=10)
login_button = ttk.Button(login_frame, text="Login", command=login_user)
login_button.grid(row=2, column=1, pady=20)
login_frame.pack(pady=20)

# Time Booking Frame with Slider
time_booking_frame = ttk.Frame(root)
ttk.Label(time_booking_frame, text="Time Booking").grid(row=0, column=0, columnspan=2, pady=10)

start_time_label = ttk.Label(time_booking_frame, text="Start Time: 08:00")
start_time_label.grid(row=1, column=0, pady=10, padx=10)
end_time_label = ttk.Label(time_booking_frame, text="End Time: 08:30")
end_time_label.grid(row=1, column=1, pady=10, padx=10)

# Time range sliders (values are minutes from 8:00)
start_slider = tk.Scale(time_booking_frame, from_=0, to=920, orient="horizontal", command=update_time_labels)
start_slider.set(0)
start_slider.grid(row=2, column=0, padx=10, pady=10)
end_slider = tk.Scale(time_booking_frame, from_=30, to=960, orient="horizontal", command=update_time_labels)
end_slider.set(30)
end_slider.grid(row=2, column=1, padx=10, pady=10)

# Proceed to Seat Booking
next_button = ttk.Button(time_booking_frame, text="Next", command=go_to_seat_booking)
next_button.grid(row=3, column=0, columnspan=2, pady=20)

# Seat Booking Frame
seat_booking_frame = ttk.Frame(root)
ttk.Label(seat_booking_frame, text="Seat Booking").grid(row=0, column=0, columnspan=2, pady=10)

# Seat Number Dropdown (1 to 100)
ttk.Label(seat_booking_frame, text="Seat Number:").grid(row=1, column=0, pady=10, padx=10)
seat_number_combo = ttk.Combobox(seat_booking_frame, values=[str(i) for i in range(1, 101)], state="readonly")
seat_number_combo.grid(row=1, column=1, pady=10, padx=10)
seat_number_combo.set("Select Seat Number")

# Seat Location Dropdown (Lower/Upper)
ttk.Label(seat_booking_frame, text="Seat Location:").grid(row=2, column=0, pady=10, padx=10)
seat_location_combo = ttk.Combobox(seat_booking_frame, values=["Lower", "Upper"], state="readonly")
seat_location_combo.grid(row=2, column=1, pady=10, padx=10)
seat_location_combo.set("Select Seat Location")

# Submit Button
submit_button = ttk.Button(seat_booking_frame, text="Submit", command=submit_booking)
submit_button.grid(row=3, column=0, columnspan=2, pady=20)

# Initially show the login frame only
seat_booking_frame.pack_forget()
time_booking_frame.pack_forget()

root.mainloop()
