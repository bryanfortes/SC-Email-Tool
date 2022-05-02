from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from db import Database
from ldap3 import Server, Connection, SUBTREE
from dotenv import load_dotenv
from emailer import User
import inflect
import os
from datetime import datetime

#load environment variables
load_dotenv()
domain = "@{}.org".format(os.environ.get("DOMAIN"))
server = Server(os.environ.get("SERVER"))
admin = os.environ.get("ADMIN")
admin_password = os.environ.get("ADMIN_PASSWORD")
searchbase = os.environ.get("SEARCH")
Justices =[]
for x in range(7): # load list of justices from env variables
    Justices.append(os.environ.get("J{}".format(x+1)))


NameDict, EmailDict = {}, {}




conn = Connection(server, admin, admin_password, auto_bind=True)
def ADSearch(connection,justice):
    connection.search(
        search_base=searchbase,
        search_scope=SUBTREE,
        search_filter=justice,
        attributes=['cn', 'mail'])
    return connection.entries

for x, justice in enumerate(Justices):
    print(x, justice)
    filterterm = f'(&(objectClass=Person)(department={justice}))'
    amt = ADSearch(conn, filterterm)
    NameDict.update({justice: []})
    for entry in amt:
        NameDict[justice].append(str(entry['cn']))
        EmailDict.update({str(entry['cn']): str(entry['mail'])})

def activateCombo():
    print(IsChecked.get())
    if IsChecked.get() == 1: #checked
        JusticeDropdown.config(state="readonly")
        JusticeDropdown.bind('<<ComboboxSelected>>', getUpdateData)
        ADDropDown.config(state="readonly")
    elif IsChecked.get() == 0:
        JusticeDropdown.config(state="disabled")
        ADDropDown.config(state="disabled")
def getUpdateData(event):
    ADDropDown.set('')
    nameDropDown.set('')
    nameDropDown ['values'] = NameDict[JusticeDropdown.get()]
   # alias = EmailDict[nameDropDown.get()]
    ADDropDown['values'] = NameDict[JusticeDropdown.get()]

UserList =[]


db = Database("Employee.db")
root = Tk()
root.title("Supreme Court Email Tool")
root.geometry("1920x1080+0+0")
root.config(bg="#2c3e50")

name = StringVar()
alias = StringVar()
start = StringVar()
job = StringVar()
email = StringVar()
mirror = StringVar()
suite = StringVar()

# Entries Frame
entries_frame = Frame(root, bg="#535c68")
entries_frame.pack(side=TOP, fill=X)
title = Label(entries_frame, text="Supreme Court Email Tool", font=("Calibri", 18, "bold"), bg="#535c68", fg="white")
title.grid(row=0, columnspan=2, padx=10, pady=20, sticky="w")

lblName = Label(entries_frame, text="Name:", font=("Calibri", 16), bg="#535c68", fg="white")
lblName.grid(row=1, column=0, padx=10, pady=10, sticky="w")
nameDropDown = ttk.Combobox(entries_frame,state="readonly",font=("Calibri", 16), width=30)
nameDropDown.grid(row=1, column=1, padx=10, pady=10, sticky="w")

#txtName = Entry(entries_frame, textvariable=name, font=("Calibri", 16), width=30)
#txtName.grid(row=1, column=1, padx=10, pady=10, sticky="w")
lblJusticeDropdown = Label(entries_frame, text="Suite:", font=("Calibri", 16), bg="#535c68", fg="white")
lblJusticeDropdown.grid(row=2, column=2, padx=10, pady=10,sticky="w")
JusticeDropdown = ttk.Combobox(entries_frame,state="readonly",font=("Calibri", 16), width=30)
JusticeDropdown.grid(row=2, column=3, padx=10, pady=10, sticky="w")
JusticeDropdown.bind('<<ComboboxSelected>>', getUpdateData)
JusticeDropdown['values'] = Justices


lblAlias = Label(entries_frame, text="Alias:", font=("Calibri", 16), bg="#535c68", fg="white")
lblAlias.grid(row=2, column=0, padx=10, pady=10, sticky="w")
txtAlias = Entry(entries_frame, textvariable=alias, state='readonly', font=("Calibri", 16), width=30)
txtAlias.grid(row=2, column=1, padx=10, pady=10, sticky="w")

lblstartDate = Label(entries_frame, text="Start Date (Month/Day)", font=("Calibri", 16), bg="#535c68", fg="white")
lblstartDate.grid(row=3, column=0, padx=10, pady=10, sticky="w")
txtstartDate = Entry(entries_frame, textvariable=start, font=("Calibri", 16), width=30)
txtstartDate.grid(row=3, column=1, padx=10, pady=10, sticky="w")


lblJob = Label(entries_frame, text="Job Title", font=("Calibri", 16), bg="#535c68", fg="white")
lblJob.grid(row=4, column=0, padx=10, pady=10, sticky="w")
txtJob = Entry(entries_frame, textvariable=job, font=("Calibri", 16), width=30)
txtJob.grid(row=4, column=1, padx=10, pady=10, sticky="w")

# lblMirror = Label(entries_frame, text="Mirror from Suite?", font=("Calibri", 16), bg="#535c68", fg="white")
# lblMirror.grid(row=1, column=2, padx=10, pady=10, sticky="w")
# IsChecked = IntVar()
# mirrorCheckbox = Checkbutton(entries_frame, variable=IsChecked, command=activateCombo, width=15, bg="#535c68")
# mirrorCheckbox.grid(row=1, column=3, padx=10, sticky="w")


# JusticeDropdown['values'] = Justices
lblADDropDown = Label(entries_frame, text="Person to Mirror:", font=("Calibri", 16), bg="#535c68", fg="white")
lblADDropDown.grid(row=3, column=2, padx=10, pady=10,sticky="w")
ADDropDown = ttk.Combobox(entries_frame, state="readonly", font=("Calibri", 16), width=30)
ADDropDown.grid(row=3, column=3, padx=10, sticky="w")



def getData(event):
    selected_row = tv.focus()
    data = tv.item(selected_row)
    global row
    row = data["values"]
    #print(row)
    name.set(row[1])
    alias.set(row[2])
    start.set(row[3])
    job.set(row[4])
    email.set(row[5])
    suite.set(row[6])
    mirror.set(row[7])

def displayAll():
    tv.delete(*tv.get_children())
    for row in db.fetch():
        tv.insert("", END, values=row)


def add_employee():
    #print(EmailDict[ADDropDown.get()])
    if txtName.get() == "" or txtAlias.get() == "" or txtstartDate.get() == "" or txtJob.get() == "" or ADDropDown.get() == "" or JusticeDropdown.get() == "":
        messagebox.showerror("Error in Input", "Please Fill All the Details")
    try: 
        datetime.strptime(txtstartDate.get(), "%m/%d")
    except ValueError:
        messagebox.showerror("Error in Input", "Incorrect Date Format")

        return
    db.insert(txtName.get().title(),txtAlias.get(), txtstartDate.get(),txtJob.get(), txtAlias.get()+domain, JusticeDropdown.get(), ADDropDown.get())
    messagebox.showinfo("Success", "Record Inserted")
    clearAll()
    displayAll()



def update_employee():
    if txtName.get() == "" or txtAge.get() == "" or txtstartDate.get() == "" or txtEmail.get() == "" or comboJob.get() == "" or txtContact.get() == "" or txtAddress.get(
            1.0, END) == "":
        messagebox.showerror("Error in Input", "Please Fill All the Details")
        return
    db.update(row[0],txtName.get(),txtAlias.get(), txtstartDate.get(),txtJob.get(), txtAlias.get()+domain, JusticeDropdown.get(), ADDropDown.get())
    messagebox.showinfo("Success", "Record Update")
    clearAll()
    displayAll()


def delete_employee():
    db.remove(row[0])
    clearAll()
    displayAll()


def clearAll():
    name.set("")
    alias.set("")
    start.set("")
    job.set("")
    ADDropDown.set("")
    JusticeDropdown.set("")

def sendSelected():
    #print(row[7])
    #print(EmailDict[row[7]])
    UserList.append(User(row[1], row[2], row[7], EmailDict[row[7]]))
    for i in range(len(UserList)):
        print(UserList[i])





btn_frame = Frame(entries_frame, bg="#535c68")
btn_frame.grid(row=6, column=0, columnspan=4, padx=10, pady=10, sticky="w")
btnAdd = Button(btn_frame, command=add_employee, text="Add Details", width=15, font=("Calibri", 16, "bold"), fg="white",
                bg="#16a085", bd=0).grid(row=0, column=0)
btnEdit = Button(btn_frame, command=update_employee, text="Update Details", width=15, font=("Calibri", 16, "bold"),
                 fg="white", bg="#2980b9",
                 bd=0).grid(row=0, column=1, padx=10)
btnDelete = Button(btn_frame, command=delete_employee, text="Delete Details", width=15, font=("Calibri", 16, "bold"),
                   fg="white", bg="#c0392b",
                   bd=0).grid(row=0, column=2, padx=10)
btnClear = Button(btn_frame, command=clearAll, text="Clear Details", width=15, font=("Calibri", 16, "bold"), fg="white",
                  bg="#f39c12",
                  bd=0).grid(row=0, column=3, padx=10)
btnSend = Button(btn_frame, command=sendSelected, text="Add to Email Queue", width=15, font=("Calibri", 16, "bold"), fg="white",
                  bg="#f39c12",
                  bd=0).grid(row=0, column=4, padx=10)


# Table Frame
tree_frame = Frame(root, bg="#ecf0f1")
tree_frame.place(x=0, y=480, width=1980, height=520)
style = ttk.Style()
style.configure("mystyle.Treeview", font=('Calibri', 18),
                rowheight=50)  # Modify the font of the body
style.configure("mystyle.Treeview.Heading", font=('Calibri', 18))  # Modify the font of the headings
tv = ttk.Treeview(tree_frame, columns=(1, 2, 3, 4, 5, 6, 7,8), style="mystyle.Treeview")
tv.heading("1", text="ID")
tv.column("1", width=5)
tv.heading("2", text="Name")
tv.heading("3", text="Alias")
tv.column("3", width=5)
tv.heading("4", text="Start Date")
tv.column("4", width=10)
tv.heading("5", text="Job Title")
tv.heading("6", text="Email")
tv.heading("7", text="Suite")
tv.column("7", width=10)
tv.heading("8", text="Mirror")
tv['show'] = 'headings'
tv.bind("<ButtonRelease-1>", getData)
tv.pack(fill=X)

displayAll()
root.mainloop()
