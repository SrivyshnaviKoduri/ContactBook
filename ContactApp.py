from tkinter import *
import sqlite3
import tkinter.ttk as ttk
import tkinter.messagebox as tkMessageBox

root = Tk()
root.title("Contact Book")
width = 700
height = 400
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width/2) - (width/2)
y = (screen_height/2) - (height/2)
root.geometry("%dx%d+%d+%d" % (width, height, x, y))
root.resizable(0, 0)
root.config(bg="white")

Name = StringVar()
Email = StringVar()
Contact = StringVar()

def Database():
    conn = sqlite3.connect("mydb.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS `member` (mem_id INTEGER NOT NULL  PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT UNIQUE, Contact TEXT)")
    cursor.execute("SELECT * FROM `member` ORDER BY `name` ASC")
    fetch = cursor.fetchall()
    for data in fetch:
        tree.insert('', 'end', values=(data))
    cursor.close()
    conn.close()

def SubmitData():
    if  Name.get() == "" or Email.get() == "" or Contact.get() == "":
        result = tkMessageBox.showwarning('', 'Invalid Info', icon="warning")
    else:
        tree.delete(*tree.get_children())
        conn = sqlite3.connect("mydb.db")
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO `member` (name, email, Contact) VALUES(?, ?, ?)", (str(Name.get()), str(Email.get()), str(Contact.get())))
            conn.commit()
            cursor.execute("SELECT * FROM `member` ORDER BY `name` ASC")
            fetch = cursor.fetchall()
            for data in fetch:
                tree.insert('', 'end', values=(data))
            cursor.close()
            conn.close()
            Name.set("")
            Email.set("")
            Contact.set("")
        except:
            result = tkMessageBox.askquestion('', 'Unique EmailAddress Constraint', icon="warning")
            if result == 'yes':
                Email.set("")

def UpdateData():
    tree.delete(*tree.get_children())
    conn = sqlite3.connect("mydb.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE `member` SET `name` = ?, `email` = ?, `Contact` = ? WHERE `mem_id` = ?", (str(Name.get()), str(Email.get()),  str(Contact.get()), int(mem_id)))
    conn.commit()
    cursor.execute("SELECT * FROM `member` ORDER BY `name` ASC")
    fetch = cursor.fetchall()
    for data in fetch:
        tree.insert('', 'end', values=(data))
    cursor.close()
    conn.close()
    Name.set("")
    Email.set("")
    Contact.set("")
def SearchData():
    if Contact.get()=='':
        result = tkMessageBox.showwarning('', 'Invalid Info', icon="warning")
    else:
        conn = sqlite3.connect("mydb.db")
        cursor = conn.cursor()
        s='%'+str(Contact.get())+'%'
        print(s)
        cursor.execute("SELECT * FROM `member` WHERE `name` like ?", (s,))
        tree.delete(*tree.get_children())
        fetch = cursor.fetchall()
        for data in fetch:
            tree.insert('', 'end', values=(data))
        cursor.close()
        conn.close()
        Contact.set("")
 
        
        
def OnSelected(event):
    global mem_id, UpdateWindow
    curItem = tree.focus()
    contents =(tree.item(curItem))
    selecteditem = contents['values']
    mem_id = selecteditem[0]
    Name.set("")
    Email.set("")
    Contact.set("")
    Name.set(selecteditem[1])
    Email.set(selecteditem[2])
    Contact.set(selecteditem[3])
    UpdateWindow = Toplevel()
    UpdateWindow.title("Contact Book")
    width = 400
    height = 300
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = ((screen_width/2) + 450) - (width/2)
    y = ((screen_height/2) + 20) - (height/2)
    UpdateWindow.resizable(0, 0)
    UpdateWindow.geometry("%dx%d+%d+%d" % (width, height, x, y))
    if 'NewWindow' in globals():
        NewWindow.destroy()

    FormTitle = Frame(UpdateWindow)
    FormTitle.pack(side=TOP)
    ContactForm = Frame(UpdateWindow)
    ContactForm.pack(side=TOP, pady=10)
    
    lbl_title = Label(FormTitle, text="Updating Contacts", font=('arial', 16), bg="orange",  width = 300)
    lbl_title.pack(fill=X)
    lbl_Name = Label(ContactForm, text="Name", font=('arial', 14), bd=5)
    lbl_Name.grid(row=0, sticky=W)
    lbl_Email = Label(ContactForm, text="Email", font=('arial', 14), bd=5)
    lbl_Email.grid(row=1, sticky=W)
    lbl_Contact = Label(ContactForm, text="Contact", font=('arial', 14), bd=5)
    lbl_Contact.grid(row=2, sticky=W)

    NameE = Entry(ContactForm, textvariable=Name, font=('arial', 14))
    NameE.grid(row=0, column=1)
    EmailE = Entry(ContactForm, textvariable=Email, font=('arial', 14))
    EmailE.grid(row=1, column=1)
    ContactE = Entry(ContactForm, textvariable=Contact,  font=('arial', 14))
    ContactE.grid(row=2, column=1)
    


    btn_updatecon = Button(ContactForm, text="Update", width=50, command=UpdateData)
    btn_updatecon.grid(row=6, columnspan=2, pady=10)



def SearchWindow():
    global NewWindow
    NewWindow = Toplevel()
    NewWindow.title("Contact Book")
    width = 400
    height = 300
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = ((screen_width/2) - 455) - (width/2)
    y = ((screen_height/2) + 20) - (height/2)
    NewWindow.resizable(0, 0)
    NewWindow.geometry("%dx%d+%d+%d" % (width, height, x, y))
    if 'UpdateWindow' in globals():
        UpdateWindow.destroy()

    FormTitle = Frame(NewWindow)
    FormTitle.pack(side=TOP)
    ContactForm = Frame(NewWindow)
    ContactForm.pack(side=TOP, pady=10)
    

    lbl_title = Label(FormTitle, text="Search Contact", font=('arial', 16), bg="#66ff66",  width = 300)
    lbl_title.pack(fill=X)
    lbl_Name = Label(ContactForm, text="Name", font=('arial', 14), bd=5)
    lbl_Name.grid(row=0, sticky=W)
    ContactE = Entry(ContactForm, textvariable=Contact,  font=('arial', 14))
    ContactE.grid(row=2, column=1)
    


    btn_updatecon = Button(ContactForm, text="Search", width=50, command=SearchData)
    btn_updatecon.grid(row=6, columnspan=2, pady=10)

   
def DeleteData():
    if not tree.selection():
       result = tkMessageBox.showwarning('', 'Select a Contact!', icon="warning")
    else:
        result = tkMessageBox.askquestion('', 'Confirm Delete', icon="warning")
        if result == 'yes':
            curItem = tree.focus()
            contents =(tree.item(curItem))
            selecteditem = contents['values']
            tree.delete(curItem)
            conn = sqlite3.connect("mydb.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM `member` WHERE `mem_id` = %d" % selecteditem[0])
            conn.commit()
            cursor.close()
            conn.close()
    
def AddNewWindow():
    global NewWindow
    NewWindow = Toplevel()
    NewWindow.title("Contact List")
    width = 400
    height = 300
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = ((screen_width/2) - 455) - (width/2)
    y = ((screen_height/2) + 20) - (height/2)
    NewWindow.resizable(0, 0)
    NewWindow.geometry("%dx%d+%d+%d" % (width, height, x, y))
    if 'UpdateWindow' in globals():
        UpdateWindow.destroy()

    FormTitle = Frame(NewWindow)
    FormTitle.pack(side=TOP)
    ContactForm = Frame(NewWindow)
    ContactForm.pack(side=TOP, pady=10)
    

    lbl_title = Label(FormTitle, text="New Contact", font=('arial', 16), bg="#66ff66",  width = 300)
    lbl_title.pack(fill=X)
    lbl_Name = Label(ContactForm, text="Name", font=('arial', 14), bd=5)
    lbl_Name.grid(row=0, sticky=W)
    lbl_Email = Label(ContactForm, text="Email", font=('arial', 14), bd=5)
    lbl_Email.grid(row=1, sticky=W)
    lbl_Contact = Label(ContactForm, text="Contact", font=('arial', 14), bd=5)
    lbl_Contact.grid(row=2, sticky=W)

    NameE = Entry(ContactForm, textvariable=Name, font=('arial', 14))
    NameE.grid(row=0, column=1)
    EmailE = Entry(ContactForm, textvariable=Email, font=('arial', 14))
    EmailE.grid(row=1, column=1)
    ContactE = Entry(ContactForm, textvariable=Contact,  font=('arial', 14))
    ContactE.grid(row=2, column=1)
    
    btn_addcon = Button(ContactForm, text="Save Contact", width=50, command=SubmitData)
    btn_addcon.grid(row=3, columnspan=2, pady=10)




Top = Frame(root, width=500, bd=1, relief=SOLID)
Top.pack(side=TOP)
Mid = Frame(root, width=500,  bg="white")
Mid.pack(side=TOP)
MidLeft = Frame(Mid, width=100)
MidLeft.pack(side=LEFT, pady=10)
MidLeftPadding = Frame(Mid, width=370, bg="white")
MidLeftPadding.pack(side=LEFT)
MidRight = Frame(Mid, width=100)
MidRight.pack(side=RIGHT, pady=10)
TableMargin = Frame(root, width=500, bg="white")
TableMargin.pack(side=TOP)

lbl_title = Label(Top, text="Contact Book", font=('arial', 16), width=500)
lbl_title.pack(fill=X)


btn_add = Button(MidLeft, text="Create Contact", bg="blue", command=AddNewWindow)
btn_add.pack()
l=Label(MidLeftPadding,text='Double click on Contact to Update!', font=('arial',8))
l.pack()
btn_delete = Button(MidRight, text="Delete Contact", bg="blue", command=DeleteData)
btn_delete.pack(side=RIGHT)
search_b=Button(TableMargin, text="Search Contact", bg="green", command=SearchWindow)
search_b.pack(side=BOTTOM)

scrollbarx = Scrollbar(TableMargin, orient=HORIZONTAL)
scrollbary = Scrollbar(TableMargin, orient=VERTICAL)
tree = ttk.Treeview(TableMargin, columns=("MemberID", "Name", "Email", "Contact"), height=400, selectmode="extended", yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
scrollbary.config(command=tree.yview)
scrollbary.pack(side=RIGHT, fill=Y)
scrollbarx.config(command=tree.xview)
scrollbarx.pack(side=BOTTOM, fill=X)
tree.heading('MemberID', text="MemberID", anchor=W)
tree.heading('Name', text="Name", anchor=W)
tree.heading('Email', text="Email", anchor=W)
tree.heading('Contact', text="Contact", anchor=W)
tree.column('#0', stretch=NO, minwidth=0, width=0)
tree.column('#1', stretch=NO, minwidth=0, width=0)
tree.column('#2', stretch=NO, minwidth=0, width=80)
tree.column('#3', stretch=NO, minwidth=0, width=120)
tree.column('#4', stretch=NO, minwidth=0, width=120)
tree.pack()
tree.bind('<Double-Button-1>', OnSelected)

if __name__ == '__main__':
    Database()
    root.mainloop()
    
