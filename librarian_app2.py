import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from psycopg2 import sql
from dotenv import load_dotenv
import os

# Main application window
class LibraryApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.wm_title("Library Management System")
        self.geometry("700x700")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        load_dotenv()
        database_url = os.getenv('DATABASE_URL')
        self.conn = psycopg2.connect(database_url)
        self.frames = {}
        for F in (MainScreen, AddBook, RemoveBook, AddSeat, RemoveSeat, UserStatistics):
            frame = F(container, self)
            self.frames[F] = frame
            

            

        self.show_frame(MainScreen)

    def show_frame(self, cont):
        self.hide_all()
        frame = self.frames[cont]
        frame.pack()
    def hide_all(self):
        for f in self.frames.values():f.pack_forget()
    def get_db_connection(self):
     
        return self.conn

# Main menu screen
class MainScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = ttk.Label(self, text="Library Management", font=("Helvetica", 16))
        label.pack(pady=10)

        # Button to navigate to Add Book
        btn_add_book = ttk.Button(self, text="Add Book", command=lambda: controller.show_frame(AddBook))
        btn_add_book.pack(pady=5)

        # Button to navigate to Remove Book
        btn_remove_book = ttk.Button(self, text="Remove Book", command=lambda: controller.show_frame(RemoveBook))
        btn_remove_book.pack(pady=5)

        # Button to navigate to Add Seat
        btn_add_seat = ttk.Button(self, text="Add Seat", command=lambda: controller.show_frame(AddSeat))
        btn_add_seat.pack(pady=5)

        # Button to navigate to Remove Seat
        btn_remove_seat = ttk.Button(self, text="Remove Seat", command=lambda: controller.show_frame(RemoveSeat))
        btn_remove_seat.pack(pady=5)

        btn_user_statistics =  ttk.Button(self, text="User Statistics", command=lambda: controller.show_frame(UserStatistics))
        btn_user_statistics.pack(pady=5)


# Frame for adding a new book
class AddBook(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        ttk.Label(self, text="Add a New Book", font=("Helvetica", 14)).grid(row=0, column=0, columnspan=2, pady=10)

        # Book fields
        ttk.Label(self, text="Book Name:").grid(row=1, column=0, padx=10, pady=5)
        self.book_name = tk.StringVar()
        ttk.Entry(self, textvariable=self.book_name).grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(self, text="ISBN:").grid(row=2, column=0, padx=10, pady=5)
        self.isbn = tk.StringVar()
        ttk.Entry(self, textvariable=self.isbn).grid(row=2, column=1, padx=10, pady=5)

        ttk.Label(self, text="Authors (comma-separated):").grid(row=3, column=0, padx=10, pady=5)
        self.authors = tk.StringVar()
        ttk.Entry(self, textvariable=self.authors).grid(row=3, column=1, padx=10, pady=5)

        ttk.Label(self, text="Publisher:").grid(row=4, column=0, padx=10, pady=5)
        self.publisher = tk.StringVar()
        ttk.Entry(self, textvariable=self.publisher).grid(row=4, column=1, padx=10, pady=5)

        ttk.Label(self, text="Category:").grid(row=5, column=0, padx=10, pady=5)
        self.category = tk.StringVar()
        ttk.Entry(self, textvariable=self.category).grid(row=5, column=1, padx=10, pady=5)

        # Buttons for adding a book and going back
        ttk.Button(self, text="Add Book", command=self.add_book).grid(row=6, column=0, columnspan=2, pady=10)
        ttk.Button(self, text="Back", command=lambda: controller.show_frame(MainScreen)).grid(row=7, column=0, columnspan=2, pady=10)

    def add_book(self):
        # Inserting a new book
        book_name = self.book_name.get()
        isbn = self.isbn.get()
        authors = "ARRAY["+ ",".join([ "'"+ i +"'" for i in self.authors.get().split(',')]) +"]"
        publisher = self.publisher.get()
        category = self.category.get()

        if not all([book_name, isbn, publisher, category]):
            messagebox.showerror("Error", "All fields except authors are required.")
            return

        with self.controller.get_db_connection() as conn:
            with conn.cursor() as cur:
                query = f"""
                    INSERT INTO Book (B_Name, ISBN, Authors, Pub, Category)
                    VALUES (%s, %s,{authors} , %s, %s)
                """
                print(query)
                cur.execute(query, (book_name, isbn, publisher, category))
            conn.commit()
        messagebox.showinfo("Success", "Book added successfully.")
        self.clear_entries()

    def clear_entries(self):
        self.book_name.set("")
        self.isbn.set("")
        self.authors.set("")
        self.publisher.set("")
        self.category.set("")

# Frame for removing a book
class RemoveBook(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        ttk.Label(self, text="Remove a Book", font=("Helvetica", 14)).grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Label(self, text="Book ID:").grid(row=1, column=0, padx=10, pady=5)
        self.book_id = tk.StringVar()
        ttk.Entry(self, textvariable=self.book_id).grid(row=1, column=1, padx=10, pady=5)

        ttk.Button(self, text="Remove Book", command=self.remove_book).grid(row=2, column=0, columnspan=2, pady=10)
        ttk.Button(self, text="Back", command=lambda: controller.show_frame(MainScreen)).grid(row=3, column=0, columnspan=2, pady=10)

    def remove_book(self):
        book_id = self.book_id.get()

        if not book_id.isdigit():
            messagebox.showerror("Error", "Please enter a valid Book ID.")
            return

        with self.controller.get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM Book WHERE B_ID = %s", (book_id,))
            conn.commit()
        
        if cur.rowcount > 0:
            messagebox.showinfo("Success", "Book removed successfully.")
            self.book_id.set("")
        else:
            messagebox.showwarning("Warning", "No book found with the given ID.")

# Frame for adding a seat
class AddSeat(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        ttk.Label(self, text="Location").grid(row=0, column=0, padx=10, pady=10)
        ttk.Label(self, text="Seat Number").grid(row=1, column=0, padx=10, pady=10)

        self.selected_location = tk.StringVar()
        self.selected_location.set("Select Seat Location")
        
        # Dropdown for seat locations
        self.dropdown = ttk.Combobox(self, textvariable=self.selected_location, values=["UP", "FRONT", "LEFT", "RIGHT", "BACK", "CENTRE"], state="readonly")
        self.dropdown.grid(row=0, column=1, padx=10, pady=10)

        self.seat_number_var = tk.StringVar()
        self.seat_number_var.set("")
        ttk.Label(self, textvariable=self.seat_number_var).grid(row=1, column=1, padx=10, pady=10)
        
        self.selected_location.trace("w", self.update_seat_number)

        ttk.Button(self, text="Insert Seat", command=self.insert_seat).grid(row=2, column=0, columnspan=2, pady=10)
        ttk.Button(self, text="Back", command=lambda: controller.show_frame(MainScreen)).grid(row=3, column=0, columnspan=2, pady=10)

    def update_seat_number(self, *args):
    
        location = self.selected_location.get()
        with self.controller.get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(f"""
                    SELECT number FROM (SELECT generate_series(1,(SELECT get_seat_count('{location}')+1)) AS number) AS series
                    WHERE number NOT IN (SELECT seat_no FROM Seat WHERE location = '{location}')
                    ORDER BY number LIMIT 1;
                """)
                row = cur.fetchone()
                print(row)
                if row:
                    self.seat_number_var.set(row[0])
                else:
                    self.seat_number_var.set("No available seats")

    def insert_seat(self):
        location = self.selected_location.get()
        seat_no = self.seat_number_var.get()
        
        if location == "Select Seat Location" or not seat_no.isdigit():
            messagebox.showerror("Error", "Please select a valid seat location and number.")
            return
        with self.controller.get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO Seat (location, seat_no) VALUES (%s, %s)", (location, seat_no))
            conn.commit()
        
        messagebox.showinfo("Success", "Seat added successfully.")
        self.update_seat_number()

# Frame for removing a seat
class RemoveSeat(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        ttk.Label(self, text="Location").grid(row=0, column=0, padx=10, pady=10)

        self.selected_location = tk.StringVar()
        self.selected_location.set("Select Seat Location")

        self.dropdown = ttk.Combobox(self, textvariable=self.selected_location, values=["UP", "FRONT", "LEFT", "RIGHT", "BACK", "CENTRE"], state="readonly")
        self.dropdown.grid(row=0, column=1, padx=10, pady=10)
        self.selected_location.trace("w", self.update_seat_values)

        ttk.Label(self, text="Seat Number").grid(row=1, column=0, padx=10, pady=10)
        self.seat_value = tk.StringVar()
        self.seat_dropdown = ttk.Combobox(self, textvariable=self.seat_value, state="readonly")
        self.seat_dropdown.grid(row=1, column=1, padx=10, pady=10)

        ttk.Button(self, text="Remove Seat", command=self.delete_seat).grid(row=2, column=0, columnspan=2, pady=10)
        ttk.Button(self, text="Back", command=lambda: controller.show_frame(MainScreen)).grid(row=3, column=0, columnspan=2, pady=10)

    def update_seat_values(self, *args):
        location = self.selected_location.get()
        with self.controller.get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT seat_no FROM Seat WHERE location = %s ORDER BY seat_no", (location,))
                seat_values = [row[0] for row in cur.fetchall()]
            
        self.seat_dropdown['values'] = seat_values
        if seat_values:
            self.seat_value.set(seat_values[0])
        else:
            self.seat_value.set("No seats available")
            messagebox.showinfo("Info", "No seats available for this location.")

    def delete_seat(self):
        location = self.selected_location.get()
        seat_no = self.seat_value.get()

        if location == "Select Seat Location" or seat_no == "No seats available":
            messagebox.showerror("Error", "Please select a valid seat location and number.")
            return
        with self.controller.get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM Seat WHERE location = %s AND seat_no = %s", (location, seat_no))
            conn.commit()

        messagebox.showinfo("Success", "Seat removed successfully.")
        self.update_seat_values()

class UserStatistics(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Buttons
        self.show_graphs_button = ttk.Button(self, text="Show Graphs", command=self.show_graphs)
        self.show_graphs_button.pack(pady=10)

        self.back_button = ttk.Button(self, text="Back", command=self.hide_graphs_and_go_back)
        self.back_button.pack(pady=10)

        # Canvas and scrollable frame for graphs
        self.canvas = tk.Canvas(self, height=600, width=650)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        
        self.graph_widgets = []

    def show_graphs(self):
        """Show all graphs on the scrollable frame."""
        self.clear_graphs()

        self.create_location_graph()
        self.create_book_graph()

    def hide_graphs_and_go_back(self):
        self.clear_graphs()
        self.controller.show_frame(MainScreen)

    def clear_graphs(self):
        for widget in self.graph_widgets:
            widget.destroy()
        self.graph_widgets.clear()

    def create_location_graph(self):
        with self.controller.get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT location, COUNT(location) FROM seat GROUP BY location;")
                location_stats = cur.fetchall()
                location, location_count = zip(*location_stats)

        fig = plt.Figure(figsize=(6, 6))
        ax = fig.add_subplot(111)
        ax.bar(location, location_count, color="skyblue")
        ax.set_title("Preferred Locations")
        ax.set_xlabel("Location")
        ax.set_ylabel("Count")
        ax.set_xticks(location)
        ax.set_xticklabels(location, rotation=90, ha="right")
        fig.tight_layout()

        canvas_plot = FigureCanvasTkAgg(fig, self.scrollable_frame)
        graph_widget = canvas_plot.get_tk_widget()
        graph_widget.pack(pady=10)


        self.graph_widgets.append(graph_widget)

    def create_book_graph(self):
        """Create and display the book graph."""
        with self.controller.get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT b_name, COUNT(b_name), isbn FROM book GROUP BY isbn, b_name;")
                book_stats = cur.fetchall()
                book_name, book_count, isbn = zip(*book_stats)


        book_name = [name[:20] + "..." if len(name) > 20 else name for name in book_name]

        fig = plt.Figure(figsize=(6, 6))
        ax = fig.add_subplot(111)
        ax.bar(book_name, book_count, color="lime")
        ax.set_title("Preferred Books")
        ax.set_xlabel("Book Names")
        ax.set_ylabel("Count")
        ax.set_xticks(book_name)
        ax.set_xticklabels(book_name, rotation=90, ha="right")
        fig.tight_layout()

        canvas_plot = FigureCanvasTkAgg(fig, self.scrollable_frame)
        graph_widget = canvas_plot.get_tk_widget()
        graph_widget.pack(pady=10)

        self.graph_widgets.append(graph_widget)
 


if __name__ == "__main__":
    app = LibraryApp()
    app.mainloop()
