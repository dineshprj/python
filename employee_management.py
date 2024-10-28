import sqlite3
from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from PIL import Image, ImageTk

class Database:
    def __init__(self, db):
        self.con = sqlite3.connect(db)
        self.cur = self.con.cursor()
        sql = """
        CREATE TABLE IF NOT EXISTS employees(
            id INTEGER PRIMARY KEY,
            name TEXT,
            age TEXT,
            doj TEXT,
            email TEXT,
            gender TEXT,
            contact TEXT,
            address TEXT
        )
        """
        self.cur.execute(sql)
        self.con.commit()

    def insert(self, name, age, doj, email, gender, contact, address):
        self.cur.execute("INSERT INTO employees VALUES (NULL, ?, ?, ?, ?, ?, ?, ?)",
                         (name, age, doj, email, gender, contact, address))
        self.con.commit()

    def fetch(self):
        self.cur.execute("SELECT * FROM employees")
        rows = self.cur.fetchall()
        return rows

    def remove(self, id):
        self.cur.execute("DELETE FROM employees WHERE id=?", (id,))
        self.con.commit()

    def update(self, id, name, age, doj, email, gender, contact, address):
        self.cur.execute(
            "UPDATE employees SET name=?, age=?, doj=?, email=?, gender=?, contact=?, address=? WHERE id=?",
            (name, age, doj, email, gender, contact, address, id))
        self.con.commit()

    def search(self, name):
        self.cur.execute("SELECT * FROM employees WHERE name LIKE ?", ('%' + name + '%',))
        return self.cur.fetchall()

class EmployeeManagementApp:
    def __init__(self, root):
        self.db = Database("Employee.db")
        self.root = root
        self.root.title("Employee Management System")
        self.root.geometry("1920x1080+0+0")
        self.root.config(bg="#2c3e50")
        self.root.state("zoomed")

        # Variables
        self.name = StringVar()
        self.age = StringVar()
        self.doj = StringVar()
        self.email = StringVar()
        self.gender = StringVar()
        self.contact = StringVar()

        # Entries Frame
        self.entries_frame = Frame(self.root, bg="#535c68")
        self.entries_frame.pack(side=TOP, fill=X)
        title = Label(self.entries_frame, text="Employee Management System", font=("Calibri", 18, "bold"), bg="#535c68", fg="white")
        title.grid(row=0, columnspan=5, padx=10, pady=20, sticky="w")

        # Entry Labels and Fields
        self.create_entry_fields()

        # Button Frame
        self.create_button_frame()

        # Search Frame
        self.create_search_frame()

        # Table Frame
        self.create_table_frame()

        # Load Logout Icon
        self.load_logout_icon()

        # Populate the table
        self.display_all()

    def create_entry_fields(self):
        lblName = Label(self.entries_frame, text="Name", font=("Calibri", 16), bg="#535c68", fg="white")
        lblName.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        txtName = Entry(self.entries_frame, textvariable=self.name, font=("Calibri", 16), width=30)
        txtName.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        lblAge = Label(self.entries_frame, text="Age", font=("Calibri", 16), bg="#535c68", fg="white")
        lblAge.grid(row=1, column=2, padx=10, pady=5, sticky="w")
        txtAge = Entry(self.entries_frame, textvariable=self.age, font=("Calibri", 16), width=30)
        txtAge.grid(row=1, column=3, padx=10, pady=5, sticky="w")

        lbldoj = Label(self.entries_frame, text="D.O.J", font=("Calibri", 16), bg="#535c68", fg="white")
        lbldoj.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.doj_entry = DateEntry(self.entries_frame, textvariable=self.doj, font=("Calibri", 16), width=28, date_pattern="yyyy-mm-dd")
        self.doj_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        lblEmail = Label(self.entries_frame, text="Email", font=("Calibri", 16), bg="#535c68", fg="white")
        lblEmail.grid(row=2, column=2, padx=10, pady=5, sticky="w")
        txtEmail = Entry(self.entries_frame, textvariable=self.email, font=("Calibri", 16), width=30)
        txtEmail.grid(row=2, column=3, padx=10, pady=5, sticky="w")

        lblGender = Label(self.entries_frame, text="Gender", font=("Calibri", 16), bg="#535c68", fg="white")
        lblGender.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        comboGender = ttk.Combobox(self.entries_frame, font=("Calibri", 16), width=28, textvariable=self.gender, state="readonly")
        comboGender['values'] = ("Male", "Female")
        comboGender.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        lblContact = Label(self.entries_frame, text="Contact No", font=("Calibri", 16), bg="#535c68", fg="white")
        lblContact.grid(row=3, column=2, padx=10, pady=5, sticky="w")
        txtContact = Entry(self.entries_frame, textvariable=self.contact, font=("Calibri", 16), width=30)
        txtContact.grid(row=3, column=3, padx=10, pady=5, sticky="w")

        lblAddress = Label(self.entries_frame, text="Address", font=("Calibri", 16), bg="#535c68", fg="white")
        lblAddress.grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.txtAddress = Text(self.entries_frame, width=85, height=5, font=("Calibri", 16))
        self.txtAddress.grid(row=5, column=0, columnspan=4, padx=10, pady=5, sticky="w")

    def create_button_frame(self):
        btn_frame = Frame(self.entries_frame, bg="#535c68")
        btn_frame.grid(row=6, column=0, columnspan=4, padx=10, pady=10, sticky="w")
        btnAdd = Button(btn_frame, command=self.add_employee, text="Add Details", width=15, font=("Calibri", 16, "bold"), fg="white", bg="#16a085", bd=0)
        btnAdd.grid(row=0, column=0)
        btnEdit = Button(btn_frame, command=self.update_employee, text="Update Details", width=15, font=("Calibri", 16, "bold"), fg="white", bg="#2980b9", bd=0)
        btnEdit.grid(row=0, column=1, padx=10)
        btnDelete = Button(btn_frame, command=self.delete_employee, text="Delete Details", width=15, font=("Calibri", 16, "bold"), fg="white", bg="#c0392b", bd=0)
        btnDelete.grid(row=0, column=2, padx=10)
        btnClear = Button(btn_frame, command=self.clear_all, text="Clear Details", width=15, font=("Calibri", 16, "bold"), fg="white", bg="#f39c12", bd=0)
        btnClear.grid(row=0, column=3, padx=10)

    def create_search_frame(self):
        search_frame = Frame(self.entries_frame, bg="#535c68")
        search_frame.grid(row=7, column=0, columnspan=4, padx=10, pady=10, sticky="w")
        lblSearch = Label(search_frame, text="Search by Name:", font=("Calibri", 16), bg="#535c68", fg="white")
        lblSearch.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.txtSearch = Entry(search_frame, font=("Calibri", 16), width=30)
        self.txtSearch.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        btnSearch = Button(search_frame, command=self.search_employee, text="Search", width=15, font=("Calibri", 16, "bold"), fg="white", bg="#2980b9", bd=0)
        btnSearch.grid(row=0, column=2, padx=10)

    def create_table_frame(self):
        tree_frame = Frame(self.root)
        tree_frame.pack(pady=20)
        style = ttk.Style()
        style.configure("mystyle.Treeview", font=("Calibri", 14), rowheight=25)
        style.configure("mystyle.Treeview.Heading", font=("Calibri", 15, "bold"))
        self.tv = ttk.Treeview(tree_frame, columns=("ID", "Name", "Age", "D.O.J", "Email", "Gender", "Contact", "Address"), style="mystyle.Treeview")
        self.tv.heading("ID", text="ID")
        self.tv.heading("Name", text="Name")
        self.tv.heading("Age", text="Age")
        self.tv.heading("D.O.J", text="D.O.J")
        self.tv.heading("Email", text="Email")
        self.tv.heading("Gender", text="Gender")
        self.tv.heading("Contact", text="Contact")
        self.tv.heading("Address", text="Address")
        self.tv['show'] = 'headings'
        self.tv.pack(fill=BOTH, expand=True)
        self.tv.bind("<ButtonRelease-1>", self.select_employee)

    def load_logout_icon(self):
        try:
            self.logout_img = Image.open("logout_icon.png")  # Make sure you have an appropriate icon
            self.logout_img = self.logout_img.resize((50, 50), Image.ANTIALIAS)
            self.logout_icon = ImageTk.PhotoImage(self.logout_img)
            logout_btn = Button(self.root, image=self.logout_icon, command=self.logout, bd=0, bg="#2c3e50")
            logout_btn.place(x=1800, y=20)
        except FileNotFoundError:
            print("Logout icon not found. Please ensure the 'logout_icon.png' file is in the project directory.")
            # If the icon isn't found, create a text button instead
            logout_btn = Button(self.root, text="Logout", command=self.logout, bd=0, bg="#2c3e50", font=("Calibri", 14), fg="white")
            logout_btn.place(x=1800, y=20)

    def display_all(self):
        for i in self.tv.get_children():
            self.tv.delete(i)
        for row in self.db.fetch():
            self.tv.insert("", "end", values=row)

    def add_employee(self):
        if self.name.get() == "" or self.age.get() == "" or self.doj.get() == "" or self.email.get() == "" or self.gender.get() == "" or self.contact.get() == "":
            messagebox.showerror("Error", "Please fill all fields.")
            return
        self.db.insert(self.name.get(), self.age.get(), self.doj.get(), self.email.get(), self.gender.get(), self.contact.get(), self.txtAddress.get("1.0", END))
        messagebox.showinfo("Success", "Employee added successfully!")
        self.display_all()
        self.clear_all()

    def update_employee(self):
        selected_item = self.tv.focus()
        if not selected_item:
            messagebox.showwarning("Select an Employee", "Please select an employee to update.")
            return
        id = self.tv.item(selected_item)['values'][0]
        self.db.update(id, self.name.get(), self.age.get(), self.doj.get(), self.email.get(), self.gender.get(), self.contact.get(), self.txtAddress.get("1.0", END))
        messagebox.showinfo("Success", "Employee updated successfully!")
        self.display_all()
        self.clear_all()

    def delete_employee(self):
        selected_item = self.tv.focus()
        if not selected_item:
            messagebox.showwarning("Select an Employee", "Please select an employee to delete.")
            return
        id = self.tv.item(selected_item)['values'][0]
        self.db.remove(id)
        messagebox.showinfo("Success", "Employee deleted successfully!")
        self.display_all()
        self.clear_all()

    def search_employee(self):
        if self.txtSearch.get() == "":
            messagebox.showwarning("Search Field Empty", "Please enter a name to search.")
            return
        for i in self.tv.get_children():
            self.tv.delete(i)
        for row in self.db.search(self.txtSearch.get()):
            self.tv.insert("", "end", values=row)

    def select_employee(self, event):
        selected_item = self.tv.focus()
        values = self.tv.item(selected_item)['values']
        self.name.set(values[1])
        self.age.set(values[2])
        self.doj.set(values[3])
        self.email.set(values[4])
        self.gender.set(values[5])
        self.contact.set(values[6])
        self.txtAddress.delete("1.0", END)
        self.txtAddress.insert(END, values[7])

    def clear_all(self):
        self.name.set("")
        self.age.set("")
        self.doj.set("")
        self.email.set("")
        self.gender.set("")
        self.contact.set("")
        self.txtAddress.delete("1.0", END)
        self.txtSearch.delete(0, END)

    def logout(self):
        # Logout functionality (currently does nothing)
        messagebox.showinfo("Logout", "Logout button clicked, but functionality is disabled.")

if __name__ == "__main__":
    root = Tk()
    app = EmployeeManagementApp(root)
    root.mainloop()
