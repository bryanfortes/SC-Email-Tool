import tkinter as tk
from tkinter import ttk
from ldap3 import Server, Connection, SUBTREE
from dotenv import load_dotenv
import os

#load environment variables
load_dotenv()
server = Server(os.environ.get("SERVER"))
admin = os.environ.get("ADMIN")
admin_password = os.environ.get("ADMIN_PASSWORD")
searchbase = os.environ.get("SEARCH")
Justices =[]
for x in range(7): # load list of justices from env variables
    Justices.append(os.environ.get("J{}".format(x+1)))

#combobox logic
def activateCombo():
    if IsChecked.get() == 1: #checked
        JusticeDropdown.config(state="readonly")
        JusticeDropdown.bind('<<ComboboxSelected>>', getUpdateData)
        ADDropDown.config(state="readonly")
    elif IsChecked.get() == 0:
        JusticeDropdown.config(state="disabled")
        ADDropDown.config(state="disabled")
def getUpdateData(event):
    ADDropDown.set('')
    ADDropDown['values'] = NameDict[JusticeDropdown.get()]


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
    #print(x)
    filterterm = f'(&(objectClass=Person)(department={justice}))'
    amt = ADSearch(conn, filterterm)
    NameDict.update({justice: []})
    for entry in amt:
        NameDict[justice].append(str(entry['cn']))
        EmailDict.update({str(entry['cn']): str(entry['mail'])})


class User:
    def __init__(self, userName, userAlias, mirrorName, mirrorAlias, suite, startDate):
        self.userName = userName
        self.userAlias = userAlias
        self.mirrorName = mirrorName
        self.mirrorAlias = mirrorAlias
        self.suite = suite
        self.startDate = startDate

root = tk.Tk()
root.title("Email Tool")
root.geometry("500x280")
tab_parent = ttk.Notebook(root)
tab1 = ttk.Frame(tab_parent)
tab2 = ttk.Frame(tab_parent)
tab_parent.add(tab1, text='New User List')
tab_parent.add(tab2, text='Add New User')


#Widgets for New User list
firstLabelTabOne = tk.Label(tab1, text="First Name:")
familyLabelTabOne = tk.Label(tab1, text="Last Name:")
jobLabelTabOne = tk.Label(tab1, text="Job Title:")

firstEntryTabOne = tk.Entry(tab1)
familyEntryTabOne = tk.Entry(tab1)
jobEntryTabOne = tk.Entry(tab1)

imgLabelTabOne = tk.Label(tab1)

buttonForward = tk.Button(tab1, text="Forward")
buttonBack = tk.Button(tab1, text="Back")

# === ADD WIDGETS TO GRID ON TAB ONE
firstLabelTabOne.grid(row=0, column=0, padx=15, pady=15)
firstEntryTabOne.grid(row=0, column=1, padx=15, pady=15)

familyLabelTabOne.grid(row=1, column=0, padx=15, pady=15)
familyEntryTabOne.grid(row=1, column=1, padx=15, pady=15)

jobLabelTabOne.grid(row=2, column=0, padx=15, pady=15)
jobEntryTabOne.grid(row=2, column=1, padx=15, pady=15)

imgLabelTabOne.grid(row=0, column=2, rowspan=3, padx=15, pady=15)

# === WIDGETS FOR TAB TWO
firstLabelTabTwo = tk.Label(tab2, text="First Name:")
familyLabelTabTwo = tk.Label(tab2, text="Family Name:")
jobLabelTabTwo = tk.Label(tab2, text="Job Title:")
#mirrorLabelTabTwo = tk.Label(tab2, text="Mirror:")

firstEntryTabTwo = tk.Entry(tab2)
familyEntryTabTwo = tk.Entry(tab2)
jobEntryTabTwo = tk.Entry(tab2)
ADDropDown = ttk.Combobox(tab2, state="disabled")
IsChecked = tk.IntVar()
JusticeDropdown = ttk.Combobox(tab2,state="disabled")
mirrorCheckbox = tk.Checkbutton(tab2, text="Mirror? ", variable=IsChecked, command=activateCombo)

buttonCommit = tk.Button(tab2, text="Add User to User List")





JusticeDropdown['values'] = Justices


# === ADD WIDGETS TO GRID ON TAB TWO
firstLabelTabTwo.grid(row=0, column=0, padx=15, pady=15)
firstEntryTabTwo.grid(row=0, column=1, padx=15, pady=15)
#imgLabelTabTwo.grid(row=0, column=2, rowspan=3, padx=15, pady=15)

familyLabelTabTwo.grid(row=1, column=0, padx=15, pady=15)
familyEntryTabTwo.grid(row=1, column=1, padx=15, pady=15)

jobLabelTabTwo.grid(row=2, column=0, padx=15, pady=15)
jobEntryTabTwo.grid(row=2, column=1, padx=15, pady=15)
mirrorCheckbox.grid(row=3, column=0, padx=15, pady=15)
JusticeDropdown.grid(row=3, column=1, padx=15, pady=15)
ADDropDown.grid(row=3, column=2, padx=15, pady=15)
buttonCommit.grid(row=4, column=1, padx=15, pady=15)




tab_parent.pack(expand = 1, fill ="both")
root.mainloop()
