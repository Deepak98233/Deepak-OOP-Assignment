import tkinter as tk
from database import *
from tkinter import *
from tkinter import ttk, messagebox,filedialog
import pandas
import pymysql

conn, cursor = initialize_connection()


def center_window(width, height):
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')


class WelcomeWindow(tk.Frame):
    def __init__(self, master):
        super().__init__()
        self.master = master
        self.master.title("Welcome")
        center_window(240, 120)

        login_button = tk.Button(self, text="Login", width=10, command=self.open_login_window)
        login_button.pack(padx=20, pady=(20, 10))

        register_button = tk.Button(self, text="Register", width=10, command=self.open_register_window)
        register_button.pack(pady=10)
        self.pack()

    def open_login_window(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.destroy()
        LoginWindow(self.master)

    def open_register_window(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.destroy()
        RegisterWindow(self.master)


class LoginWindow(tk.Frame):
    def __init__(self, master):
        super().__init__()
        self.master = master
        self.master.title("Login")
        self.master.resizable(False, False)
        center_window(240, 150)

        tk.Label(self, text="Username:").grid(row=0, column=0)
        self.username_entry = tk.Entry(self)
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self, text="Password:").grid(row=1, column=0)
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)

        submit_button = tk.Button(self, text="Submit", width=8, command=self.submit)
        submit_button.grid(row=2, column=1, sticky="e", padx=10, pady=(10, 0))

        submit_button = tk.Button(self, text="Back", width=8, command=self.back)
        submit_button.grid(row=2, column=0, sticky="w", padx=10, pady=(10, 0))
        self.pack()

    def submit(self):
        data = {}
        data["email"] = self.username_entry.get()
        data["password"] = self.password_entry.get()

        if login(cursor, data) == True:
            print("successful login")
            for widget in self.winfo_children():
                widget.destroy()
            self.destroy()
            messagebox.showinfo("Success", "Welcome")
            MainWindow(self.master)
        else:
            print("unsuccessful login")

    def back(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.destroy()
        WelcomeWindow(self.master)


class RegisterWindow(tk.Frame):
    def __init__(self, master):
        super().__init__()
        self.master = master
        self.master.title("Register")
        self.master.resizable(False, False)
        center_window(320, 350)

        tk.Label(self, text="First Name:").grid(row=0, column=0, sticky="w")
        self.first_name_entry = tk.Entry(self, width=26)
        self.first_name_entry.grid(row=0, column=1, padx=10, pady=10, sticky="e")

        tk.Label(self, text="Last Name:").grid(row=1, column=0, sticky="w")
        self.last_name_entry = tk.Entry(self, width=26)
        self.last_name_entry.grid(row=1, column=1, padx=10, pady=10, sticky="e")

        tk.Label(self, text="Password:").grid(row=2, column=0, sticky="w")
        self.password_entry = tk.Entry(self, show="*", width=26)
        self.password_entry.grid(row=2, column=1, padx=10, pady=10, sticky="e")

        tk.Label(self, text="Email:").grid(row=3, column=0, sticky="w")
        self.email_entry = tk.Entry(self, width=26)
        self.email_entry.grid(row=3, column=1, padx=10, pady=10, sticky="e")

        tk.Label(self, text="Gender:").grid(row=4, column=0, sticky="w")
        self.gender_entry = tk.Entry(self, width=10)
        self.gender_entry.grid(row=4, column=1, padx=10, pady=10, sticky="e")

        tk.Label(self, text="Age:").grid(row=5, column=0, sticky="w")
        self.age_entry = tk.Entry(self, width=10)
        self.age_entry.grid(row=5, column=1, padx=10, pady=10, sticky="e")

        tk.Label(self, text="Address:").grid(row=6, column=0, sticky="w")
        self.address_entry = tk.Text(self, width=20, height=3)
        self.address_entry.grid(row=6, column=1, padx=10, pady=10, sticky="e")

        submit_button = tk.Button(self, text="Submit", width=8, command=self.submit)
        submit_button.grid(row=7, column=1, padx=10, pady=10, sticky="e")

        submit_button = tk.Button(self, text="Back", width=8, command=self.back)
        submit_button.grid(row=7, column=0, sticky="w", padx=10, pady=(10, 10))
        self.pack()

    def submit(self):
        data = {}
        data["firstName"] = self.first_name_entry.get()
        data["lastName"] = self.last_name_entry.get()
        data["password"] = self.password_entry.get()
        data["email"] = self.email_entry.get()
        data["gender"] = self.gender_entry.get()
        data["age"] = self.age_entry.get()
        data["address"] = self.address_entry.get(1.0, tk.END)

        register(cursor, conn, data)
        messagebox.showinfo("Success", "Record has been inserted")

    def back(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.destroy()
        WelcomeWindow(self.master)


class MainWindow(tk.Frame):
    def __init__(self, rootr):
        super().__init__()
        self.root = root
        self.root.title("To Do List")
        self.root.geometry("1370x700+0+0")

        title = Label(self.root, text="TO DO LIST", bd=9, relief=GROOVE, font=("times new roman", 50, "bold"),
                      bg="green", fg="yellow")
        title.pack(side=TOP, fill=X)
        # ============== All Variables db========================================
        self.number_var = StringVar()
        self.Task_var = StringVar()
        self.priority_var = StringVar()
        self.status_var = StringVar()
        self.due_date_var = StringVar()

        self.search_by = StringVar()
        self.search_txt = StringVar()

        # ==============Manageframe============================================
        Manage_Frame = Frame(self.root, bd=4, relief=RIDGE, bg="blue")
        Manage_Frame.place(x=20, y=100, width=450, height=585)

        m_title = Label(Manage_Frame, text="Information", bg="yellow", fg="black", font=("times new roman", 40, "bold"))
        m_title.grid(row=0, columnspan=2, pady=20)

        lbl_number = Label(Manage_Frame, text="Number:", bg="blue", fg="white", font=("times new roman", 20, "bold"))
        lbl_number.grid(row=1, column=0, pady=10, padx=20, sticky="w")
        txt_number = Entry(Manage_Frame, textvariable=self.number_var, font=("times new roman", 15, "bold"), bd=5, relief=GROOVE)
        txt_number.grid(row=1, column=1, pady=10, padx=20, sticky="w")

        lbl_task = Label(Manage_Frame, text="Task:", bg="blue", fg="white", font=("times new roman", 20, "bold"))
        lbl_task.grid(row=2, column=0, pady=10, padx=20, sticky="w")
        txt_task = Entry(Manage_Frame, textvariable=self.Task_var, font=("times new roman", 15, "bold"), bd=5,relief=GROOVE)
        txt_task.grid(row=2, column=1, pady=10, padx=20, sticky="w")

        lbl_priority = Label(Manage_Frame, text="Priority:", bg="blue", fg="white",font=("times new roman", 20, "bold"))
        lbl_priority.grid(row=3, column=0, pady=10, padx=20, sticky="w")

        combo_priority = ttk.Combobox(Manage_Frame, textvariable=self.priority_var,font=("times new roman", 13, "bold"), state='readonly')
        combo_priority['values'] = ("High", "Medium", "low")
        combo_priority.grid(row=3, column=1, padx=20, pady=10)

        lbl_status = Label(Manage_Frame, text="status:", bg="blue", fg="white", font=("times new roman", 20, "bold"))
        lbl_status.grid(row=4, column=0, pady=10, padx=20, sticky="w")

        combo_status = ttk.Combobox(Manage_Frame, textvariable=self.status_var, font=("times new roman", 13, "bold"),state='readonly')
        combo_status['values'] = ("Complete", "Incomplete")
        combo_status.grid(row=4, column=1, padx=20, pady=10)

        lbl_due_date = Label(Manage_Frame, text="due_date:", bg="blue", fg="white",font=("times new roman", 20, "bold"))
        lbl_due_date.grid(row=5, column=0, pady=10, padx=20, sticky="w")
        txt_due_date = Entry(Manage_Frame, textvariable=self.due_date_var, font=("times new roman", 15, "bold"), bd=5,relief=GROOVE)
        txt_due_date.grid(row=5, column=1, pady=10, padx=20, sticky="w")

        # =========Button Frame==================
        btn_Frame = Frame(Manage_Frame, bd=3, relief=RIDGE, bg="black")
        btn_Frame.place(x=15, y=525, width=420)

        Addbtn = Button(btn_Frame, text="Add", width=10, command=self.add_students).grid(row=0, column=0, padx=10,pady=10)
        deletebtn = Button(btn_Frame, text="Delete", width=10, command=self.delete_data).grid(row=0, column=1, padx=10,pady=10)
        Clearbtn = Button(btn_Frame, text="Clear", width=10, command=self.clear).grid(row=0, column=2, padx=10, pady=10)
        exitbtn = Button(btn_Frame, text="Logout", width=10, command=exit).grid(row=0, column=3, padx=10, pady=10)

        # =========2nd Detials  Frame==================
        Detials_Frame = Frame(self.root, bd=4, relief=RIDGE, bg="blue")
        Detials_Frame.place(x=500, y=100, width=800, height=585)

        lbl_search = Label(Detials_Frame, text="Search By", bg="blue", fg="white", font=("times new roman", 20, "bold"))
        lbl_search.grid(row=0, column=0, pady=10, padx=20, sticky="w")

        combo_search = ttk.Combobox(Detials_Frame, textvariable=self.search_by, width=10, font=("times new roman", 13, "bold"), state='readonly')
        combo_search['values'] = ("Number", "Task", "Priority")
        combo_search.grid(row=0, column=1, padx=20, pady=10)

        txt_search = Entry(Detials_Frame, textvariable=self.search_txt, width=20, font=("times new roman", 10, "bold"),bd=5, relief=GROOVE)
        txt_search.grid(row=0, column=2, pady=10, padx=20, sticky="w")

        searchbtn = Button(Detials_Frame, text="Search", width=8, pady=5, command=self.search_data).grid(row=0,column=3,padx=10,pady=10)
        showallbtn = Button(Detials_Frame, text="Show All", width=8, pady=5, command=self.fetch_data).grid(row=0,column=4, padx=10,pady=10)
        Exportbtn = Button(Detials_Frame, text="Export", width=8, pady=5, command=self.export_data).grid(row=0,column=5,padx=10,pady=10)


        # ========== table frame ===========
        Table_Frame = Frame(Detials_Frame, bd=4, relief=RIDGE, bg="crimson")
        Table_Frame.place(x=10, y=70, width=760, height=500)

        scroll_x = Scrollbar(Table_Frame, orient=HORIZONTAL)
        scroll_y = Scrollbar(Table_Frame, orient=VERTICAL)
        self.Student_table = ttk.Treeview(Table_Frame, column=("number", "Task", "priority", "status", "due_date"),
                                          xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.Student_table.xview)
        scroll_y.config(command=self.Student_table.yview)
        self.Student_table.heading("number", text="Number.")
        self.Student_table.heading("Task", text="Task")
        self.Student_table.heading("priority", text="Priority")
        self.Student_table.heading("status", text="Status")
        self.Student_table.heading("due_date", text="Due Date")

        self.Student_table['show'] = 'headings'
        self.Student_table.column("number", width=100,anchor=CENTER)
        self.Student_table.column("Task", width=100,anchor=CENTER)
        self.Student_table.column("priority", width=100,anchor=CENTER)
        self.Student_table.column("status", width=100,anchor=CENTER)
        self.Student_table.column("due_date", width=100,anchor=CENTER)

        self.Student_table.pack(fill=BOTH, expand=1)
        self.Student_table.bind("<ButtonRelease-1>", self.get_cursor)

        self.fetch_data()

    def add_students(self):
        if self.number_var.get() == "" or self.Task_var.get() == "":
            messagebox.showerror("Error", "All fields are required ")
        else:
            con = pymysql.connect(host="localhost", user="root", password="", database="tdl")
            cur = con.cursor()

            cur.execute("insert into students values(%s,%s,%s,%s,%s)", (self.number_var.get(),
                                                                        self.Task_var.get(),
                                                                        self.priority_var.get(),
                                                                        self.status_var.get(),
                                                                        self.due_date_var.get()
                                                                        ))

            con.commit()
            self.fetch_data()
            self.clear()
            con.close()
            messagebox.showinfo("Success", "Record has been inserted")

    def fetch_data(self):
        con = pymysql.connect(host="localhost", user="root", password="", database="tdl")
        cur = con.cursor()
        cur.execute("select * from students ")
        rows = cur.fetchall()
        if len(rows) != 0:

            self.Student_table.delete(*self.Student_table.get_children())
            for row in rows:
                self.Student_table.insert('', END, values=row)
            con.commit()
        con.close()


    def export_data(self):
        url = filedialog.asksaveasfile(defaultextension=' .csv')
        indexing = self.Student_table.get_children()
        newlist = []
        for index in indexing:
            content = self.Student_table.item(index)
            datalist = content['values']
            newlist.append(datalist)
            table = pandas.DataFrame(newlist, columns=['number', 'Task', 'priority', 'status', 'due_date'])
            table.to_csv(url, index=False)
            messagebox.showinfo('Success', 'Data is saved successfully')

    def clear(self):
        self.number_var.set("")
        self.Task_var.set("")
        self.priority_var.set("")
        self.status_var.set("")
        self.due_date_var.set("")

    def get_cursor(self, ev):
        curosor_row = self.Student_table.focus()
        contents = self.Student_table.item(curosor_row)
        row = contents['values']
        self.number_var.set(row[0])
        self.Task_var.set(row[1])
        self.priority_var.set(row[2])
        self.status_var.set(row[3])
        self.due_date_var.set(row[4])

    def exit(self):
        messagebox.askyesno('confirm','Do you want to logout?')
        for widget in self.winfo_children():
            widget.destroy()
        self.destroy()
        WelcomeWindow(self.master)

    def delete_data(self):
        con = pymysql.connect(host="localhost", user="root", password="", database="tdl")
        cur = con.cursor()
        cur.execute("delete from students where number=%s", self.number_var.get())
        con.commit()
        con.close()
        self.fetch_data()
        self.clear()

    def search_data(self):
        con = pymysql.connect(host="localhost", user="root", password="", database="tdl")
        cur = con.cursor()
        cur.execute("select * from students where " + str(self.search_by.get()) + " Like '%" + str(
            self.search_txt.get()) + "%'")
        rows = cur.fetchall()
        if len(rows) != 0:

            self.Student_table.delete(*self.Student_table.get_children())
            for row in rows:
                self.Student_table.insert('', END, values=row)
            con.commit()
        con.close()

        class MainWindow(tk.Frame):
            pass


root = tk.Tk()
root.eval('tk::PlaceWindow . center')
WelcomeWindow(root)
root.mainloop()