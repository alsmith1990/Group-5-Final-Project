import tkinter as tk
from tkinter import messagebox, simpledialog

# CLASS 1: Represents the data object
class Appointment:
    def __init__(self, date, client_name, job_type, description):
        self.date = date
        self.client_name = client_name
        self.job_type = job_type
        self.description = description
        
        # Collection 1: Tuple (used here to store immutable summary data)
        self.summary_data = (self.date, self.client_name, self.job_type)

    def __str__(self):
        return f"[{self.job_type}] {self.client_name} - {self.description}"


# CLASS 2: Manages the data logic and collections
class ScheduleManager:
    def __init__(self):
        # Collection 2: Dictionary (maps a date string to a list of appointments)
        self.schedule = {}
        
        # Collection 3: Tuple of valid job categories for painting contractors
        self.job_categories = ("Estimate", "Interior Painting", "Exterior Painting", "Touch-up", "Consultation")

    def add_appointment(self, appointment):
        # Collection 4: List (stores multiple appointments on the same day)
        if appointment.date not in self.schedule:
            self.schedule[appointment.date] = []
        
        self.schedule[appointment.date].append(appointment)

    def get_appointments_for_day(self, date):
        # Returns the list of appointments for a specific date, or an empty list if none exist
        return self.schedule.get(date, [])


# CLASS 3: Handles the Graphical User Interface
class TrackerGUI:
    def __init__(self, root, manager):
        self.root = root
        self.manager = manager
        
        self.root.title("Painting Contractor Scheduler")
        self.root.geometry("350x250")
        self.root.eval('tk::PlaceWindow . center')

        # GUI Elements
        self.lbl_title = tk.Label(root, text="Daily Appointment Tracker", font=("Arial", 14, "bold"))
        self.lbl_title.pack(pady=20)

        # Button for Main Function 1: Scheduling
        self.btn_schedule = tk.Button(root, text="Schedule New Appointment", width=25, command=self.schedule_appt)
        self.btn_schedule.pack(pady=10)

        # Button for Main Function 2: Checking
        self.btn_check = tk.Button(root, text="Check Daily Schedule", width=25, command=self.check_appts)
        self.btn_check.pack(pady=10)

        # Exit Button
        self.btn_exit = tk.Button(root, text="Exit Program", width=25, command=root.quit)
        self.btn_exit.pack(pady=10)

    def schedule_appt(self):
        # Gather data via simple GUI dialogs
        date = simpledialog.askstring("Input", "Enter Date (YYYY-MM-DD):", parent=self.root)
        if not date: return
        
        client = simpledialog.askstring("Input", "Enter Client Name:", parent=self.root)
        if not client: return
        
        job_type = simpledialog.askstring("Input", f"Enter Job Type\nOptions: {', '.join(self.manager.job_categories)}", parent=self.root)
        if not job_type: return
        
        desc = simpledialog.askstring("Input", "Enter Job Description/Notes:", parent=self.root)
        if not desc: return

        # Instantiate Appointment and add to Manager
        new_appt = Appointment(date, client, job_type, desc)
        self.manager.add_appointment(new_appt)
        
        messagebox.showinfo("Success", f"Appointment successfully booked for {client} on {date}!")

    def check_appts(self):
        # Query the schedule
        date = simpledialog.askstring("Input", "Enter Date to check (YYYY-MM-DD):", parent=self.root)
        if not date: return

        appts = self.manager.get_appointments_for_day(date)
        
        if not appts:
            messagebox.showinfo("Schedule", f"No appointments currently booked for {date}.")
        else:
            result_str = f"Appointments for {date}:\n" + ("-"*30) + "\n"
            for appt in appts:
                result_str += f"{str(appt)}\n"
            
            messagebox.showinfo(f"Schedule for {date}", result_str)

# Application Entry Point
if __name__ == "__main__":
    # Initialize the core tkinter window
    root = tk.Tk()
    
    # Instantiate the backend manager and the frontend GUI
    contractor_manager = ScheduleManager()
    app = TrackerGUI(root, contractor_manager)
    
    # Start the GUI event loop
    root.mainloop()