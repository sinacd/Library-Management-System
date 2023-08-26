import tkinter
from tkinter import *
from tkinter import ttk
import tkinter.messagebox
from backend import *
from colors import *
from PIL import Image, ImageTk


class Main:
    def __init__(self):
        self.main = Tk()
        self.main.title("main")
        width = self.main.winfo_screenwidth()
        height = self.main.winfo_screenheight()
        self.main.geometry("%dx%d" % (width, height))
        self.main.state('zoomed')
        self.main.minsize(width, height-200)
        self.main.resizable(width=False, height=True)
        self.main.config(bg=lightWhite)
        # self.createElements()
        self.min_w = 60  # Minimum width of the frame
        self.max_w = 225  # Maximum width of the frame
        self.cur_width = self.min_w  # Increasing width of the frame
        self.expanded = False  # Check if it is completely self.expanded
        self.backend = Backend()
        self.sidebarFrame, self.mainFrame, self.label1 = self.createElements()
        # ================== prototype section ==============
        self.table = None
        self.titleText = StringVar()
        self.authorText = StringVar()
        self.yearText = StringVar()
        self.isbnText = StringVar()
        self.shelfText = StringVar()
        self.ent1 = None
        self.ent2 = None
        self.ent3 = None
        self.ent4 = None
        self.ent5 = None
        self.btn4 = None
        self.userIdText = None
        self.userNameText = None
        self.userFamilyText = None
        self.userExpireTimeText = None
        self.bookIdText = None
        self.currentUserId = None
        self.currentBookId = None
        self.IsIssuing = False
        # ================== prototypes ==============
        self.createElementsBooks()

    def run(self):
        self.main.mainloop()

    def expand(self):

        self.cur_width += 10  # Increase the width by 10
        rep = self.main.after(5, self.expand)  # Repeat this func every 5 ms
        self.sidebarFrame.config(width=self.cur_width)  # Change the width to new increase width
        if self.cur_width >= self.max_w:  # If width is greater than maximum width
            self.expanded = True  # Frame is expended
            self.main.after_cancel(rep)  # Stop repeating the func
            self.fill()

    def contract(self):

        self.cur_width -= 10  # Reduce the width by 10
        rep = self.main.after(5, self.contract)  # Call this func every 5 ms
        self.sidebarFrame.config(width=self.cur_width)  # Change the width to new reduced width
        if self.cur_width <= self.min_w:  # If it is back to normal width
            self.expanded = False  # Frame is not self.expanded
            self.main.after_cancel(rep)  # Stop repeating the func
            self.fill()

    def fill(self):
        if self.expanded:  # If the frame is exanded
            # Show a text, and remove the image
            # home_b.grid(row=3, column=0, pady=10)
            self.issueBook_b.config(text=' Issue Book ', image=self.issueBook, compound=LEFT, fg="white", font=(0, 15))
            self.books_b.config(text=' Book Management ', image=self.books, compound=LEFT, fg="white", font=(0, 15))
            self.user_b.config(text=' User Management', image=self.user, compound=LEFT, fg="white", font=(0, 15))
        else:
            # Bring the image back
            self.issueBook_b.config(image=self.issueBook, text='', compound=LEFT, font=(0, 15))
            self.books_b.config(image=self.books, text='', compound=LEFT, font=(0, 15))
            self.user_b.config(image=self.user, text='', compound=LEFT, font=(0, 15))

    def createElementsBooks(self, isissuing=False):
        self.label1.config(text="Book Management")
        self.IsIssuing = isissuing
        self.titleText = StringVar()
        self.authorText = StringVar()
        self.yearText = StringVar()
        self.isbnText = StringVar()
        self.shelfText = StringVar()

        self.mainFrame.pack_forget()
        self.mainFrame = Frame(self.main, bg=lightWhite, width=800, height=self.main.winfo_height())
        self.mainFrame.pack(side=RIGHT, expand=True, fill=BOTH)

        self.table = ttk.Treeview(self.mainFrame, columns=('title', 'author', 'year', 'isbn', 'shelf'), show='headings')
        self.table.heading('title', text='title')
        self.table.column('title', anchor=CENTER)
        self.table.heading('author', text='author')
        self.table.column('author', anchor=CENTER)
        self.table.heading('year', text='year')
        self.table.column('year', anchor=CENTER)
        self.table.heading('isbn', text='isbn')
        self.table.column('isbn', anchor=CENTER)
        self.table.heading('shelf', text='shelf')
        self.table.column('shelf', anchor=CENTER)
        self.table.grid(row=1, column=0, padx=(25, 0), columnspan=5, rowspan=4, sticky='nws', pady=0)
        # frame3 = Frame(self.mainFrame, bg=darkBlue2, width=self.min_w, height=self.main.winfo_height())
        # frame3.grid(row=4, column=0)
        sb1 = Scrollbar(self.mainFrame)
        sb1.grid(row=1, column=5, sticky='nws', rowspan=4)
        self.table.configure(yscrollcommand=sb1.set)
        sb1.configure(command=self.table.yview)
        self.ent1 = EntryWithPlaceholder(master=self.mainFrame, textvariable=self.titleText,
                                         highlightbackground=darkBlue2,
                                         highlightthickness=2,
                                         placeholder="title")
        self.ent1.grid(row=0, column=0, pady=(60, 25), padx=(30, 5))
        self.ent2 = EntryWithPlaceholder(master=self.mainFrame, textvariable=self.authorText,
                                         highlightbackground=darkBlue2,
                                         highlightthickness=2,
                                         placeholder="author")
        self.ent2.grid(row=0, column=1, pady=(60, 25), padx=5)
        self.ent3 = EntryWithPlaceholder(master=self.mainFrame, textvariable=self.yearText,
                                         highlightbackground=darkBlue2,
                                         highlightthickness=2,
                                         placeholder="year")
        self.ent3.grid(row=0, column=2, pady=(60, 25), padx=5)
        self.ent4 = EntryWithPlaceholder(master=self.mainFrame, textvariable=self.isbnText,
                                         highlightbackground=darkBlue2,
                                         highlightthickness=2,
                                         placeholder="isbn")
        self.ent4.grid(row=0, column=3, pady=(60, 25), padx=5)
        self.ent5 = EntryWithPlaceholder(master=self.mainFrame, textvariable=self.shelfText,
                                         highlightbackground=darkBlue2,
                                         highlightthickness=2,
                                         placeholder="shelf")
        self.ent5.grid(row=0, column=4, pady=(60, 25), padx=(5, 30))
        btn1 = Button1(self.mainFrame, command=lambda: self.SearchBooks(), text="Search Books", width=18, height=2,
                       relief='flat',
                       font=font1)
        btn1.grid(row=0, column=5, pady=(35, 0), padx=(25, 0))
        if self.IsIssuing == False:
            btn2 = Button1(self.mainFrame, command=lambda: self.AddBooks(), text="Add Books", width=18, height=2,
                           relief='flat',
                           font=font1)
            btn2.grid(row=1, column=5, pady=(30, 0), padx=(25, 0))
            btn3 = Button1(self.mainFrame, command=lambda: self.DeleteBooks(), text="Delete Books", width=18, height=2,
                           relief='flat',
                           font=font1)
            btn3.grid(row=2, column=5, pady=(30, 0), padx=(25, 0))
            self.btn4 = Button1(self.mainFrame, command=lambda: self.UpdateBooks(), text="Update Books", width=18,
                                height=2,
                                relief='flat',
                                font=font1)
            self.btn4.grid(row=3, column=5, pady=(30, 240), padx=(25, 0))
        else:
            self.btn5 = Button1(self.mainFrame, command=lambda: self.IssueBookChooseBook(), text="Finish Issue",
                                width=18, height=2,
                                relief='flat',
                                font=font1)
            self.btn5.grid(row=4, column=5, pady=(30, 240), padx=(25, 0))

        # btn2 = Button1(self.mainFrame, text="view exe1")
        # btn2.grid(row=1, column=1)

    def BookSelect(self, _):
        # self.table.delete()
        # for i in self.table.selection():

        if len(self.table.selection()) >= 1:
            entries = {0: self.ent1, 1: self.ent2, 2: self.ent3, 3: self.ent4, 4: self.ent5}
            for key, value in entries.items():
                value.delete(0, END)
                value.insert(END, self.table.item(self.table.selection()[0])['values'][key])
                value['fg'] = "black"

    # def BookDelete(self, _):
    #     if len(self.table.selection()) >= 1:
    #         self.table.delete(self.table.selection()[0])
    #     else:

    def SearchBooks(self):
        for row in self.table.get_children():
            self.table.delete(row)
        books = self.backend.searchBook(self.titleText.get(), self.authorText.get(), self.yearText.get(),
                                        self.isbnText.get(), self.shelfText.get())
        for book in books:
            data = (book[1], book[2], book[3], book[4], book[5], book[0])
            self.table.insert(parent="", index=0, values=data)
        self.table.bind('<<TreeviewSelect>>', self.BookSelect)
        self.table.bind('<Delete>', lambda event: self.DeleteBooks())

    def AddBooks(self):
        if self.titleText.get() != "title" and self.authorText.get() != "author":
            self.backend.createBook(self.titleText.get(), self.authorText.get(), self.yearText.get(),
                                    self.isbnText.get(), self.shelfText.get())
            self.SearchBooks()
        else:
            tkinter.messagebox.showerror("No title/author", "you should fill at least fields title and author ")

    def DeleteBooks(self):
        if len(self.table.selection()) >= 1:
            self.backend.deleteBook(self.table.item(self.table.selection()[0])['values'][5])
            self.SearchBooks()
        else:
            tkinter.messagebox.showerror("Not selected", "choose a book to delete ")

    def UpdateBooks(self):
        if len(self.table.selection()) >= 1:
            self.backend.updateBook(self.table.item(self.table.selection()[0])['values'][5], self.titleText.get(),
                                    self.authorText.get(), self.yearText.get(),
                                    self.isbnText.get(), self.shelfText.get())
            self.SearchBooks()
            entries = {0: self.ent1, 1: self.ent2, 2: self.ent3, 3: self.ent4, 4: self.ent5}
            for key, value in entries.items():
                value.delete(0, END)
                value['fg'] = darkBlue2
                value.focus_set()
            self.btn4.focus_set()
        else:
            tkinter.messagebox.showerror("Not selected", "choose a book to update ")

    def IssueBookChooseBook(self):
        if len(self.table.selection()) >= 1:
            self.currentBookId = self.table.item(self.table.selection()[0])['values'][5]
            self.backend.createIssue(self.currentUserId, self.currentBookId)
            tkinter.messagebox.showinfo("Success",
                                        f"book {self.titleText.get()} has been issued for user with id {self.currentUserId}")
            self.IsIssuing = False
            self.currentBookId = None
            self.currentUserId = None
            self.createElementsIssueBook()
            self.SearchIssues()
        else:
            tkinter.messagebox.showerror("Not selected", "choose a book to issue ")

    # =========================================users==============================================
    def SearchUsers(self):
        for row in self.table.get_children():
            self.table.delete(row)
        users = self.backend.searchUser(self.userIdText.get(), self.userNameText.get(), self.userFamilyText.get())
        for user in users:
            # datetime_obj = datetime.strptime(user[3], '%Y %m %d')
            data = (user[0], user[1], user[2], user[3])
            self.table.insert(parent="", index=0, values=data)
        self.table.bind('<<TreeviewSelect>>', self.UserSelect)
        # self.ent1.configure(state="normal")

    def UserSelect(self, _):

        # self.table.delete()
        # for i in self.table.selection():

        if len(self.table.selection()) >= 1:
            self.ent1.configure(state="normal")
            entries = {0: self.ent1, 1: self.ent2, 2: self.ent3, }
            for key, value in entries.items():
                value.delete(0, END)
                value.insert(END, self.table.item(self.table.selection()[0])['values'][key])
                value['fg'] = "black"
            self.ent1.configure(state="disabled")
        else:
            self.ent1.configure(state="normal")

    def AddUsers(self):
        if self.userNameText.get() != "name" and self.userFamilyText.get() != "family":
            self.backend.createUser(self.userNameText.get(), self.userFamilyText.get())
            self.SearchUsers()
        else:
            tkinter.messagebox.showerror("No name/family", "you should fill at least fields name and family ")

    def UpdateUsers(self):
        if len(self.table.selection()) >= 1:
            self.ent1.configure(state="normal")
            self.backend.updateUser(self.userIdText.get(), self.userNameText.get(), self.userFamilyText.get())
            self.SearchUsers()
            entries = {0: self.ent1, 1: self.ent2, 2: self.ent3}
            for key, value in entries.items():
                value.delete(0, END)
                value['fg'] = darkBlue2
                value.focus_set()
            self.btn4.focus_set()
        else:
            tkinter.messagebox.showerror("Not selected", "choose a user to update ")

    def ReSubscriptionUsers(self):
        if len(self.table.selection()) >= 1:
            msg_box = tkinter.messagebox.askyesno("confirm",
                                                  f"user with id {self.table.item(self.table.selection()[0])['values'][0]} has been resubed?")
            if msg_box:
                self.ent1.configure(state="normal")
                self.backend.reSubscriptionUser(self.userIdText.get())
                self.SearchUsers()
                entries = {0: self.ent1, 1: self.ent2, 2: self.ent3}
                for key, value in entries.items():
                    value.delete(0, END)
                    value['fg'] = darkBlue2
                    value.focus_set()
                self.btn4.focus_set()
            # self.userIdText = StringVar()

        else:
            tkinter.messagebox.showerror("Not selected", "choose a user to reSub ")

    def IssueBookChooseUser(self):
        if len(self.table.selection()) >= 1:
            self.currentUserId = self.userIdText.get()
            self.createElementsBooks(True)
        else:
            tkinter.messagebox.showerror("Not selected", "choose a user to issue book for ")

    def createElementsUser(self, isissuing=False):
        self.label1.config(text="User Management")
        self.IsIssuing = isissuing
        self.userIdText = StringVar()
        self.userNameText = StringVar()
        self.userFamilyText = StringVar()
        self.userExpireTimeText = StringVar()

        self.mainFrame.pack_forget()
        self.mainFrame = Frame(self.main, bg=lightWhite, width=800, height=self.main.winfo_height())
        self.mainFrame.pack(side=RIGHT, expand=True, fill=BOTH)

        self.table = ttk.Treeview(self.mainFrame, columns=('id', 'name', 'family', 'expireTime'), show='headings')
        self.table.heading('id', text='id')
        self.table.column('id', anchor=CENTER)
        self.table.heading('name', text='name')
        self.table.column('name', anchor=CENTER)
        self.table.heading('family', text='family')
        self.table.column('family', anchor=CENTER)
        self.table.heading('expireTime', text='expireTime')
        self.table.column('expireTime', anchor=CENTER)
        self.table.grid(row=1, column=0, padx=(25, 0), columnspan=4, rowspan=4, sticky='news', pady=0)
        # frame3 = Frame(self.mainFrame, bg=darkBlue2, width=self.min_w, height=self.main.winfo_height())
        # frame3.grid(row=4, column=0)
        label = Label(self.mainFrame,bg=lightWhite)
        label.grid(row=0, column=3, padx=(0, 300))
        sb1 = Scrollbar(self.mainFrame)
        sb1.grid(row=1, column=4, sticky='nws', rowspan=4)
        self.table.configure(yscrollcommand=sb1.set)
        sb1.configure(command=self.table.yview)
        self.ent1 = EntryWithPlaceholder(master=self.mainFrame, textvariable=self.userIdText,
                                         highlightbackground=darkBlue2,
                                         highlightthickness=2,
                                         placeholder="id")
        self.ent1.grid(row=0, column=0, pady=(60, 25), padx=(80, 0))
        self.ent2 = EntryWithPlaceholder(master=self.mainFrame, textvariable=self.userNameText,
                                         highlightbackground=darkBlue2,
                                         highlightthickness=2,
                                         placeholder="name")
        self.ent2.grid(row=0, column=1, pady=(60, 25), padx=(105, 5))
        self.ent3 = EntryWithPlaceholder(master=self.mainFrame, textvariable=self.userFamilyText,
                                         highlightbackground=darkBlue2,
                                         highlightthickness=2,
                                         placeholder="family")
        self.ent3.grid(row=0, column=2, pady=(60, 25), padx=(105, 0))

        btn1 = Button1(self.mainFrame, command=lambda: self.SearchUsers(), text="Search Users", width=18, height=2,
                       relief='flat',
                       font=font1)
        btn1.grid(row=0, column=5, pady=(35, 0), padx=(25, 0))
        if self.IsIssuing == False:
            btn2 = Button1(self.mainFrame, command=lambda: self.AddUsers(), text="Add User", width=18, height=2,
                           relief='flat',
                           font=font1)
            btn2.grid(row=1, column=5, pady=(30, 0), padx=(25, 0))
            btn3 = Button1(self.mainFrame, command=lambda: self.UpdateUsers(), text="Update User", width=18, height=2,
                           relief='flat',
                           font=font1)
            btn3.grid(row=2, column=5, pady=(30, 0), padx=(25, 0))
            self.btn4 = Button1(self.mainFrame, command=lambda: self.ReSubscriptionUsers(), text="ReSubscription",
                                width=18,
                                height=2,
                                relief='flat',
                                font=font1)
            self.btn4.grid(row=3, column=5, pady=(30, 0), padx=(25, 0))
        self.btn5 = Button1(self.mainFrame, command=lambda: self.IssueBookChooseUser(), text="Issue a Book", width=18,
                            height=2,
                            relief='flat',
                            font=font1)
        self.btn5.grid(row=4, column=5, pady=(30, 150), padx=(25, 0))

    # ===========================================issue book==============================================

    def SearchIssues(self):
        for row in self.table.get_children():
            self.table.delete(row)
        issues = self.backend.searchIssue(self.userIdText.get(), self.bookIdText.get())
        for issue in issues:
            # datetime_obj = datetime.strptime(user[3], '%Y %m %d')
            data = (issue[1], issue[2], issue[3], issue[4], issue[5], issue[0])
            self.table.insert(parent="", index=0, values=data)
        self.table.bind('<<TreeviewSelect>>', self.IssueSelect)

        # self.ent1.configure(state="normal")

    def IssueSelect(self, _):
        if len(self.table.selection()) >= 1:
            entries = {0: self.ent1, 2: self.ent2}
            for key, value in entries.items():
                value.delete(0, END)
                value.insert(END, self.table.item(self.table.selection()[0])['values'][key])
                value['fg'] = "black"

    def AddIssue(self):
        self.createElementsUser(True)
        # if len(self.table.selection()) >= 1:
        # self.backend.createUser(self.userNameText.get(), self.userFamilyText.get())

    def ReturnBook(self):
        if len(self.table.selection()) >= 1:
            msg_box = tkinter.messagebox.askyesno("confirm",
                                                  f"book {self.table.item(self.table.selection()[0])['values'][3]} has been returned?")
            if msg_box:
                self.backend.returnedIssue(self.table.item(self.table.selection()[0])['values'][5])
                self.SearchIssues()
        else:
            tkinter.messagebox.showerror("nothing has been chosen", "choose an issue to to return")

    def UpdateIssue(self):
        if len(self.table.selection()) >= 1:
            self.backend.updateIssue(self.table.item(self.table.selection()[0])['values'][5], self.userIdText.get(),
                                     self.bookIdText.get())
            self.SearchIssues()
        else:
            tkinter.messagebox.showerror("nothing has been chosen", "choose an issue to update")

    def createElementsIssueBook(self):
        self.label1.config(text="Issue Management")
        self.userIdText = StringVar()
        self.bookIdText = StringVar()

        self.mainFrame.pack_forget()
        self.mainFrame = Frame(self.main, bg=lightWhite, width=800, height=self.main.winfo_height())
        self.mainFrame.pack(side=RIGHT, expand=True, fill=BOTH)

        self.table = ttk.Treeview(self.mainFrame, columns=('userId', 'user', 'bookId', 'book', 'returned'),
                                  show='headings')
        self.table.heading('userId', text='userId')
        self.table.column('userId', anchor=CENTER)
        self.table.heading('user', text='user')
        self.table.column('user', anchor=CENTER)
        self.table.heading('bookId', text='bookId')
        self.table.column('bookId', anchor=CENTER)
        self.table.heading('book', text='book')
        self.table.column('book', anchor=CENTER)
        self.table.heading('returned', text='returned')
        self.table.column('returned', anchor=CENTER)
        self.table.grid(row=1, column=0, padx=(25, 0), columnspan=5, rowspan=3, sticky='nws', pady=0)
        # frame3 = Frame(self.mainFrame, bg=darkBlue2, width=self.min_w, height=self.main.winfo_height())
        # frame3.grid(row=4, column=0)
        sb1 = Scrollbar(self.mainFrame)
        sb1.grid(row=1, column=5, sticky='nws', rowspan=3)
        self.table.configure(yscrollcommand=sb1.set)
        sb1.configure(command=self.table.yview)
        self.ent1 = EntryWithPlaceholder(master=self.mainFrame, textvariable=self.userIdText,
                                         highlightbackground=darkBlue2,
                                         highlightthickness=2,
                                         placeholder="userId")
        self.ent1.grid(row=0, column=0, pady=(60, 25), padx=(0, 0))
        self.ent2 = EntryWithPlaceholder(master=self.mainFrame, textvariable=self.bookIdText,
                                         highlightbackground=darkBlue2,
                                         highlightthickness=2,
                                         placeholder="bookId")
        self.ent2.grid(row=0, column=2, pady=(60, 25), padx=(0, 100))

        btn1 = Button1(self.mainFrame, command=lambda: self.SearchIssues(), text="Search Issues", width=18, height=2,
                       relief='flat',
                       font=font1)
        btn1.grid(row=0, column=5, pady=(35, 0), padx=(25, 0))
        btn2 = Button1(self.mainFrame, command=lambda: self.AddIssue(), text="Add Issue", width=18, height=2,
                       relief='flat',
                       font=font1)
        btn2.grid(row=1, column=5, pady=(30, 0), padx=(25, 0))
        btn3 = Button1(self.mainFrame, command=lambda: self.ReturnBook(), text=" Book Returned", width=18, height=2,
                       relief='flat',
                       font=font1)
        btn3.grid(row=2, column=5, pady=(30, 0), padx=(25, 0))
        self.btn4 = Button1(self.mainFrame, command=lambda: self.UpdateIssue(), text="Update Issue", width=18,
                            height=2,
                            relief='flat',
                            font=font1)
        self.btn4.grid(row=3, column=5, pady=(30, 240), padx=(25, 0))

    def createElements(self):
        img = (Image.open("./pics/icons/dashboard.png"))
        resized_image = img.resize((20, 20), resample=Image.LANCZOS)
        self.issueBook = ImageTk.PhotoImage(resized_image)
        img = (Image.open("./pics/icons/book.png"))
        resized_image = img.resize((25, 25), resample=Image.LANCZOS)
        self.books = ImageTk.PhotoImage(resized_image)
        img = (Image.open("./pics/icons/user.png"))
        resized_image = img.resize((30, 30), resample=Image.LANCZOS)
        self.user = ImageTk.PhotoImage(resized_image)
        self.main.update()  # For the width to get updated
        header = Frame(self.main, bg=lightBlue2, height=60)
        header.pack(side=TOP, expand=True, fill=X)
        header.pack_propagate(False)
        label1 = Label(header, text="Book Management", bg=lightBlue2, fg="white", font=(0, 15))
        label1.pack(side=LEFT, padx=20)
        frame = Frame(self.main, bg=darkBlue2, width=self.min_w, height=self.main.winfo_height())
        frame.pack(side=LEFT)
        frame2 = Frame(self.main, bg=lightWhite, width=self.main.winfo_width(), height=self.main.winfo_height())
        frame2.pack(side=RIGHT, expand=True, fill=BOTH)
        self.issueBook_b = Button1(frame, command=lambda: self.createElementsIssueBook(), image=self.issueBook,
                                   bg=darkBlue2, relief='flat')
        self.books_b = Button1(frame, command=lambda: self.createElementsBooks(), image=self.books, bg=darkBlue2,
                               relief='flat')
        self.user_b = Button1(frame, command=lambda: self.createElementsUser(), image=self.user, bg=darkBlue2,
                              relief='flat')

        # Put them on the frame
        # self.dashboard_b.grid(row=0, column=0, pady=(20, 0), padx=10)
        # self.books_b.grid(row=1, column=0, pady=10)
        # self.user_b.grid(row=2, column=0)
        self.books_b.pack(fill=X, pady=(20, 0))
        self.user_b.pack(fill=X, pady=10)
        self.issueBook_b.pack(fill=X)

        # Bind to the frame, if entered or left
        frame.bind('<Enter>', lambda e: self.expand())
        frame.bind('<Leave>', lambda e: self.contract())
        # btn1 = Button1(frame2, text="view all books")
        # btn1.grid(row=0, column=0)
        # btn2 = Button1(frame2, text="view all books")
        # btn2.grid(row=1, column=1)
        # btn3 = Button1(frame2, text="view all books")
        # btn3.grid(row=2, column=2)

        # So that it does not depend on the widgets inside the frame
        frame.grid_propagate(False)
        frame.pack_propagate(False)
        return frame, frame2, label1


if __name__ == "__main__":
    main = Main()
    main.run()
