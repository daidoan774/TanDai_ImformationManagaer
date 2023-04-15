import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from tkinter import*

class LoginWindow:
    def __init__(self, parent):
        self.parent = parent
        self.parent.title("Login System")
        self.parent.geometry('390x450')
        self.parent.configure( bg='#856ff8')
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        
        self.login_frame = ttk.Frame(self.parent, padding=10)
        self.login_frame.place(x = 70,y =130,width=250,height=150,bordermode='outside')
        self.special = ttk.Separator(self.login_frame,orient='horizontal')
        self.special.place(x=0, y=125, relwidth=3)
        style = ttk.Style()
        style.configure("TSeparator", bordercolor="#ececec", relief="raised")
        
        self.label = Label(self.login_frame,text="My Account",font=('arial',14,'bold'))
        self.label.place(x = 70,y=5)
        
        ttk.Label(self.login_frame, text="Username: ").place(x=10,y=40)
        self.username_entry = ttk.Entry(self.login_frame,width=22, textvariable=self.username_var)
        self.username_entry.place(x=75,y=40)

        ttk.Label(self.login_frame, text="Password: ").place(x=10,y=70)
        self.password_entry = ttk.Entry(self.login_frame, show="*",width=22 ,textvariable=self.password_var)
        self.password_entry.place(x=75,y=70)

        self.login_button = ttk.Button(self.login_frame, text="Login",width=15, command=self.login)
        self.login_button.place(x=80,y=100)

    def login(self):
        username = self.username_var.get()
        password = self.password_var.get()

        if username == "admin" and password == "admin":
            self.parent.destroy()
            StudentManager()
        else:
            messagebox.showerror("Error","Invalid username or password")


class StudentManager:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Student Manager")
        self.root.geometry("760x400")
        self.root.config(bg="#6699CC")
        self.db_conn = sqlite3.connect("students.db")
        self.create_tables()

        self.top = tk.Frame(self.root, pady=10,bg="#FFFFCC")
        self.top.pack(side=tk.TOP)

        self.bottom = tk.Frame(self.root, pady=10)
        self.bottom.place(x=5, y=100)
        
        self.tree = ttk.Treeview(self.bottom, columns=("id", "name", "email", "phone","fname","mname"))
        self.tree.heading("#0", text="")
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Name")
        self.tree.heading("email", text="Email")
        self.tree.heading("phone", text="Phone")
        self.tree.heading("fname", text="FatherName")
        self.tree.heading("mname", text="MotherName")
        self.tree.column("#0", width=0)
        self.tree.column("id", width=50, anchor=tk.CENTER)
        self.tree.column("name", width=150)
        self.tree.column("email", width=150)
        self.tree.column("phone", width=100)
        self.tree.column("fname", width=150)
        self.tree.column("mname", width=150)
        self.tree.pack()

        ttk.Button(self.top, text="Add Student", command=self.add_student).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.top, text="Edit Student", command=self.edit_student).pack(side=tk.LEFT, padx=5)
        # ttk.Button(self.top, text="Delete Student", command=self.delete_student).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.top, text="Refresh", command=self.refresh).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.top, text="Batch Delete", command=self.batch_delete_students).pack(side=tk.LEFT, padx=5)
        search_button = ttk.Button(self.top, text="Search Students", command=self.search_students)
        search_button.pack(side=tk.LEFT, padx=5)

        self.load_students()
    def search_students(self):
        search_window = tk.Toplevel(self.root)
        search_window.title("Search Students")
        search_window.geometry("280x150")
        search_window.config(bg="#F8F8FF")
        search_label = ttk.Label(search_window, text="Enter the student name to search:")
        search_label.pack(pady=10)

        search_var = tk.StringVar()
        search_entry = ttk.Entry(search_window, width=30, textvariable=search_var)
        search_entry.pack()

        def search():
            name = search_var.get().lower()
            cursor = self.db_conn.cursor()
            cursor.execute("SELECT * FROM students WHERE LOWER(name) LIKE ?", ('%' + name + '%',))
            students = cursor.fetchall()

        # Clear the treeview
            for child in self.tree.get_children():
                self.tree.delete(child)

        # Add the searched students to the treeview
            for student in students:
                self.tree.insert("", tk.END, values=student)

        search_button = ttk.Button(search_window, text="Search", command=search)
        search_button.pack(pady=10)
        search()

    def refresh(self):
        # Clear the treeview
        for child in self.tree.get_children():
            self.tree.delete(child)
        # Reload the data from the database
        self.load_students()
        
    def create_tables(self):
        cursor = self.db_conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS students (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT, phone TEXT,fname TEXT, mname TEXT )")
        self.db_conn.commit()

    def load_students(self):
        cursor = self.db_conn.cursor()
        cursor.execute("SELECT * FROM students")
        students = cursor.fetchall()

        for student in students:
            self.tree.insert("", tk.END, values=student)
    def add_student(self):
        add_window = AddStudentWindow(self)
        add_window.top.transient(self.root)
        add_window.top.grab_set()
        self.root.wait_window(add_window.top)
        
        self.root.attributes("-disabled", True)

        self.root.attributes("-disabled", False)
    def edit_student(self):
        # Get the selected item from the treeview
        selected_item = self.tree.selection()
        if len(selected_item) == 0:
            messagebox.showwarning("Warning", "Please select a student to edit.")
            return
        # Get the student information from the selected item
        student_id = self.tree.item(selected_item, "values")[0]
        name = self.tree.item(selected_item, "values")[1]
        email = self.tree.item(selected_item, "values")[2]
        phone = self.tree.item(selected_item, "values")[3]
        fname = self.tree.item(selected_item,"values")[4]
        mname = self.tree.item(selected_item,"values")[5]
        # Open the edit student window
        edit_window = EditStudentWindow(self, student_id, name, email, phone,fname,mname)
        edit_window.top.transient(self.root)
        edit_window.top.grab_set()
        self.root.wait_window(edit_window.top)
        self.root.attributes("-disabled", True)
        self.root.attributes("-disabled", False)

    # def delete_student(self):
    #     # Get the selected item from the treeview
    #     selected_item = self.tree.selection()
    #     if len(selected_item) == 0:
    #         messagebox.showwarning("Warning", "Please select a student to delete.")
    #         return

    #     # Confirm the deletion with the user
    #     confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this student?")

    #     if confirm:
    #         # Get the student ID from the selected item
    #         student_id = self.tree.item(selected_item, "values")[0]

    #         # Delete the student from the database
    #         cursor = self.db_conn.cursor()
    #         cursor.execute("DELETE FROM students WHERE id=?", (student_id))
    #         self.db_conn.commit()

    #         # Remove the student from the treeview
    #         self.tree.delete(selected_item)
            
    def batch_delete_students(self):
        # Get the selected items from the treeview
        selected_items = self.tree.selection()
        if len(selected_items) == 0:
            messagebox.showwarning("Warning", "Please select at least one student to delete.")
            return

        # Ask the user to confirm the deletion
        confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete the selected students? This action cannot be undone!!!!.")
        if not confirm:
            return

        # Loop through the selected items and delete them
        for item in selected_items:
            student_id = self.tree.item(item, "values")[0]
            cursor = self.db_conn.cursor()
            cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
            self.db_conn.commit()
            self.tree.delete(item)

class EditStudentWindow:
    def __init__(self, parent, student_id, name, email, phone,fname,mname):
        self.db_conn = sqlite3.connect("students.db")
        self.parent = parent
        self.student_id = student_id

        self.name_var = tk.StringVar(value=name)
        self.email_var = tk.StringVar(value=email)
        self.phone_var = tk.StringVar(value=phone)
        self.fname_var =  tk.StringVar(value=fname)
        self.mname_var =  tk.StringVar(value=mname)
        self.top = tk.Toplevel(self.parent.root)

        ttk.Label(self.top, text="Name: ").grid(row=0, column=0, sticky=tk.W)
        self.name_entry = ttk.Entry(self.top, textvariable=self.name_var)
        self.name_entry.grid(row=0, column=1)

        ttk.Label(self.top, text="Email: ").grid(row=1, column=0, sticky=tk.W)
        self.email_entry = ttk.Entry(self.top, textvariable=self.email_var)
        self.email_entry.grid(row=1, column=1)

        ttk.Label(self.top, text="Phone: ").grid(row=2, column=0, sticky=tk.W)
        self.phone_entry = ttk.Entry(self.top, textvariable=self.phone_var)
        self.phone_entry.grid(row=2, column=1)
        
        ttk.Label(self.top, text="FatherName: ").grid(row=3, column=0, sticky=tk.W)
        self.phone_entry = ttk.Entry(self.top, textvariable=self.fname_var)
        self.phone_entry.grid(row=3, column=1)
        
        ttk.Label(self.top, text="MotherName: ").grid(row=4, column=0, sticky=tk.W)
        self.phone_entry = ttk.Entry(self.top, textvariable=self.mname_var)
        self.phone_entry.grid(row=4, column=1)
        ttk.Button(self.top, text="Save", command=self.save_student).grid(row=5, column=1, pady=10)

    def save_student(self):
        name = self.name_var.get()
        email = self.email_var.get()
        phone = self.phone_var.get()
        fname = self.fname_var.get()
        mname = self.mname_var.get()
        if name and email and phone and fname and mname:
            try:
                cursor = self.parent.db_conn.cursor()
                cursor.execute("UPDATE students SET name=?, email=?, phone=?, fname=?, mname=? WHERE id=?", (name, email, phone,fname,mname ,self.student_id))
                self.parent.db_conn.commit()
                messagebox.showinfo("UPDATE","UPDATE SUCCESFULLY!!")
                # self.parent.destroy()
                self.top.destroy()
            except Exception as e:
                print(f"Error occurred: {e}")


   

    def delete_student(students, id):
        for i, student in enumerate(students):
            if student["id"] == id:
                del students[i]
                print(f"Student with ID {id} deleted successfully!")
                return
        print(f"No student with ID {id} found.")

class AddStudentWindow:
    def __init__(self, parent):
        self.parent = parent
        
        self.name_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.fnam_var = tk.StringVar()
        self.mnam_var = tk.StringVar()
       
        self.top = tk.Toplevel(self.parent.root,background="#FFFFFF")
        self.top.geometry("240x200")
        
        ttk.Label(self.top, text="Name: ").grid(row=0, column=0, sticky=tk.W,pady=5)
        self.name_entry = ttk.Entry(self.top, textvariable=self.name_var)
        self.name_entry.grid(row=0, column=1,pady=5)

        ttk.Label(self.top, text="Email: ").grid(row=1, column=0, sticky=tk.W,pady=5)
        self.email_entry = ttk.Entry(self.top, textvariable=self.email_var)
        self.email_entry.grid(row=1, column=1,pady=5)

        ttk.Label(self.top, text="Phone: ").grid(row=2, column=0, sticky=tk.W)
        self.phone_entry = ttk.Entry(self.top, textvariable=self.phone_var)
        self.phone_entry.grid(row=2, column=1)

        ttk.Label(self.top, text="Fathername: ").grid(row=3, column=0, sticky=tk.W,pady=5)
        self.phone_entry = ttk.Entry(self.top, textvariable=self.fnam_var)
        self.phone_entry.grid(row=3, column=1,pady=5)
        
        ttk.Label(self.top, text="Mothername: ").grid(row=4, column=0, sticky=tk.W,pady=5)
        self.phone_entry = ttk.Entry(self.top, textvariable=self.mnam_var)
        self.phone_entry.grid(row=4, column=1,pady=5)
        
        ttk.Button(self.top, text="Add", command=self.add_student).grid(row=5, column=1, pady=10)

    def add_student(self):
        name = self.name_var.get()
        email = self.email_var.get()
        phone = self.phone_var.get()
        fname = self.fnam_var.get()
        mname = self.mnam_var.get()
        if name and email and phone and fname and mname:
            cursor = self.parent.db_conn.cursor()
            cursor.execute("INSERT INTO students (name, email, phone,fname,mname) VALUES (?, ?, ?,?,?)", (name, email, phone,fname,mname))
            self.parent.db_conn.commit()

            student_id = cursor.lastrowid
            self.parent.tree.insert("", tk.END, values=(student_id, name, email, phone,fname,mname))

            self.top.destroy()
        else:
            messagebox.showerror("Error", "All fields are required")
root = Tk()
oj = LoginWindow(root)
root.mainloop()