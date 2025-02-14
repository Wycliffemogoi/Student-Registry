import customtkinter as ctk
from tkinter import messagebox, ttk
import json
import os

# Set appearance mode and color theme
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# File to store user and student data
USERS_FILE = "users.json"
STUDENTS_FILE = "students.json"

# Load data from JSON files
def load_data(file):
    if os.path.exists(file):
        with open(file, "r") as f:
            return json.load(f)
    return {}

# Save data to JSON files
def save_data(data, file):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)

# Initialize data files if they don't exist
if not os.path.exists(USERS_FILE):
    save_data({}, USERS_FILE)
if not os.path.exists(STUDENTS_FILE):
    save_data({}, STUDENTS_FILE)

# User registration function
def register_user():
    username = entry_username.get()
    password = entry_password.get()
    if username and password:
        users = load_data(USERS_FILE)
        if username in users:
            messagebox.showerror("Error", "Username already exists!")
        else:
            users[username] = password
            save_data(users, USERS_FILE)
            messagebox.showinfo("Success", "User registered successfully!")
    else:
        messagebox.showerror("Error", "Please fill all fields!")

# User login function
def login_user():
    username = entry_username.get()
    password = entry_password.get()
    users = load_data(USERS_FILE)
    if username in users and users[username] == password:
        messagebox.showinfo("Success", "Login successful!")
        login_window.destroy()
        open_student_system()
    else:
        messagebox.showerror("Error", "Invalid username or password!")

# Function to clear form fields
def clear_form(entry_name, entry_admission, entry_phone, entry_residence, course_var, entry_date):
    entry_name.delete(0, "end")
    entry_admission.delete(0, "end")
    entry_phone.delete(0, "end")
    entry_residence.delete(0, "end")
    course_var.set("ICT")  # Reset dropdown to default value
    entry_date.delete(0, "end")

# Open student registration system
def open_student_system():
    student_window = ctk.CTk()
    student_window.title("Student Registration System")
    student_window.geometry("1000x600")

    # Frame for student registration form
    form_frame = ctk.CTkFrame(student_window)
    form_frame.pack(pady=10, padx=10, fill="x")

    # Labels and entries for student details
    ctk.CTkLabel(form_frame, text="Name:").grid(row=0, column=0, padx=10, pady=10)
    entry_name = ctk.CTkEntry(form_frame)
    entry_name.grid(row=0, column=1, padx=10, pady=10)

    ctk.CTkLabel(form_frame, text="Admission Number:").grid(row=1, column=0, padx=10, pady=10)
    entry_admission = ctk.CTkEntry(form_frame)
    entry_admission.grid(row=1, column=1, padx=10, pady=10)

    ctk.CTkLabel(form_frame, text="Phone Number:").grid(row=2, column=0, padx=10, pady=10)
    entry_phone = ctk.CTkEntry(form_frame)
    entry_phone.grid(row=2, column=1, padx=10, pady=10)

    ctk.CTkLabel(form_frame, text="Residence:").grid(row=3, column=0, padx=10, pady=10)
    entry_residence = ctk.CTkEntry(form_frame)
    entry_residence.grid(row=3, column=1, padx=10, pady=10)

    ctk.CTkLabel(form_frame, text="Course:").grid(row=4, column=0, padx=10, pady=10)
    course_var = ctk.StringVar(value="ICT")
    course_dropdown = ctk.CTkOptionMenu(form_frame, values=["ICT", "Electrical", "Plumbing", "Automotive"], variable=course_var)
    course_dropdown.grid(row=4, column=1, padx=10, pady=10)

    ctk.CTkLabel(form_frame, text="Date of Admission:").grid(row=5, column=0, padx=10, pady=10)
    entry_date = ctk.CTkEntry(form_frame)
    entry_date.grid(row=5, column=1, padx=10, pady=10)

    # Function to register a student
    def register_student():
        student = {
            "name": entry_name.get(),
            "admission_number": entry_admission.get(),
            "phone_number": entry_phone.get(),
            "residence": entry_residence.get(),
            "course": course_var.get(),
            "date_of_admission": entry_date.get()
        }
        students = load_data(STUDENTS_FILE)
        if student["admission_number"] in students:
            messagebox.showerror("Error", "Admission number already exists!")
        else:
            students[student["admission_number"]] = student
            save_data(students, STUDENTS_FILE)
            messagebox.showinfo("Success", "Student registered successfully!")
            refresh_student_list()
            clear_form(entry_name, entry_admission, entry_phone, entry_residence, course_var, entry_date)  # Clear the form after registration

    # Function to refresh the student list
    def refresh_student_list():
        for row in tree.get_children():
            tree.delete(row)
        students = load_data(STUDENTS_FILE)
        for admission_number, student in students.items():
            tree.insert("", "end", values=(
                student["name"],
                admission_number,
                student["phone_number"],
                student["residence"],
                student["course"],
                student["date_of_admission"]
            ))

    # Function to search for a student
    def search_student():
        search_term = entry_search.get()
        students = load_data(STUDENTS_FILE)
        for row in tree.get_children():
            tree.delete(row)
        for admission_number, student in students.items():
            if (search_term.lower() in student["name"].lower() or
                search_term == admission_number or
                search_term.lower() == student["course"].lower()):
                tree.insert("", "end", values=(
                    student["name"],
                    admission_number,
                    student["phone_number"],
                    student["residence"],
                    student["course"],
                    student["date_of_admission"]
                ))

    # Function to update student details
    def update_student():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a student to update!")
            return
        admission_number = tree.item(selected_item, "values")[1]
        students = load_data(STUDENTS_FILE)
        if admission_number in students:
            students[admission_number] = {
                "name": entry_name.get(),
                "admission_number": entry_admission.get(),
                "phone_number": entry_phone.get(),
                "residence": entry_residence.get(),
                "course": course_var.get(),
                "date_of_admission": entry_date.get()
            }
            save_data(students, STUDENTS_FILE)
            messagebox.showinfo("Success", "Student details updated successfully!")
            refresh_student_list()
            clear_form(entry_name, entry_admission, entry_phone, entry_residence, course_var, entry_date)  # Clear the form after updating

    # Function to delete a student
    def delete_student():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a student to delete!")
            return
        admission_number = tree.item(selected_item, "values")[1]
        students = load_data(STUDENTS_FILE)
        if admission_number in students:
            del students[admission_number]
            save_data(students, STUDENTS_FILE)
            messagebox.showinfo("Success", "Student deleted successfully!")
            refresh_student_list()
            clear_form(entry_name, entry_admission, entry_phone, entry_residence, course_var, entry_date)  # Clear the form after deletion

    # Function to populate form fields when a student is selected
    def on_student_select(event):
        selected_item = tree.selection()
        if selected_item:
            student_data = tree.item(selected_item, "values")
            entry_name.delete(0, "end")
            entry_name.insert(0, student_data[0])
            entry_admission.delete(0, "end")
            entry_admission.insert(0, student_data[1])
            entry_phone.delete(0, "end")
            entry_phone.insert(0, student_data[2])
            entry_residence.delete(0, "end")
            entry_residence.insert(0, student_data[3])
            course_var.set(student_data[4])
            entry_date.delete(0, "end")
            entry_date.insert(0, student_data[5])

    # Buttons for student system
    ctk.CTkButton(form_frame, text="Register Student", command=register_student).grid(row=6, column=0, padx=10, pady=10)
    ctk.CTkButton(form_frame, text="Update Student", command=update_student).grid(row=6, column=1, padx=10, pady=10)
    ctk.CTkButton(form_frame, text="Delete Student", command=delete_student).grid(row=6, column=2, padx=10, pady=10)

    # Search bar
    search_frame = ctk.CTkFrame(student_window)
    search_frame.pack(pady=10, padx=10, fill="x")
    ctk.CTkLabel(search_frame, text="Search by Name/Admission/Course:").grid(row=0, column=0, padx=10, pady=10)
    entry_search = ctk.CTkEntry(search_frame)
    entry_search.grid(row=0, column=1, padx=10, pady=10)
    ctk.CTkButton(search_frame, text="Search", command=search_student).grid(row=0, column=2, padx=10, pady=10)

    # Treeview to display students
    tree_frame = ctk.CTkFrame(student_window)
    tree_frame.pack(pady=10, padx=10, fill="both", expand=True)
    columns = ("Name", "Admission Number", "Phone Number", "Residence", "Course", "Date of Admission")
    tree = ttk.Treeview(tree_frame, columns=columns, show="headings")

    # Set column headings and widths
    tree.heading("Name", text="Name")
    tree.heading("Admission Number", text="Admission Number")
    tree.heading("Phone Number", text="Phone Number")
    tree.heading("Residence", text="Residence")
    tree.heading("Course", text="Course")
    tree.heading("Date of Admission", text="Date of Admission")

    tree.column("Name", width=150, anchor="w")
    tree.column("Admission Number", width=120, anchor="w")
    tree.column("Phone Number", width=120, anchor="w")
    tree.column("Residence", width=150, anchor="w")
    tree.column("Course", width=100, anchor="w")
    tree.column("Date of Admission", width=120, anchor="w")

    # Enable column resizing
    for col in columns:
        tree.column(col, stretch=True)

    tree.pack(fill="both", expand=True)
    tree.bind("<<TreeviewSelect>>", on_student_select)

    # Refresh student list on startup
    refresh_student_list()

    student_window.mainloop()

# Login window
login_window = ctk.CTk()
login_window.title("Login / Register")
login_window.geometry("300x200")

ctk.CTkLabel(login_window, text="Username:").grid(row=0, column=0, padx=10, pady=10)
entry_username = ctk.CTkEntry(login_window)
entry_username.grid(row=0, column=1, padx=10, pady=10)

ctk.CTkLabel(login_window, text="Password:").grid(row=1, column=0, padx=10, pady=10)
entry_password = ctk.CTkEntry(login_window, show="*")
entry_password.grid(row=1, column=1, padx=10, pady=10)

ctk.CTkButton(login_window, text="Register", command=register_user).grid(row=2, column=0, padx=10, pady=10)
ctk.CTkButton(login_window, text="Login", command=login_user).grid(row=2, column=1, padx=10, pady=10)

login_window.mainloop()