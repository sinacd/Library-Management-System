import tkinter.messagebox
from tkinter import *
from main import *
from backend import *
from colors import *
from PIL import Image, ImageTk
import time


class Login:
    def __init__(self):
        self.login = Tk()
        self.login.title("login")
        self.login.geometry('360x470')
        self.login.config(bg=darkBlue)
        self.frame1 = Frame(self.login, background=darkBlue)
        self.frame1.pack(side=TOP)
        self.createElements()
        self.loginStatus = False
        self.backend = Backend()

    def run(self):
        self.login.mainloop()

    def createElements(self):
        userNameEString = StringVar()
        passwordEString = StringVar()
        img = (Image.open("./pics/icons/userlogo.png"))
        resized_image = img.resize((200, 100), resample=Image.LANCZOS)
        userLogo = ImageTk.PhotoImage(resized_image)
        img = (Image.open("./pics/icons/userId.png"))
        resized_image = img.resize((35, 35), resample=Image.LANCZOS)
        usernameLogo = ImageTk.PhotoImage(resized_image)
        img = (Image.open("./pics/icons/passlogo.png"))
        resized_image = img.resize((35, 35), resample=Image.LANCZOS)
        passLogo = ImageTk.PhotoImage(resized_image)
        userLogoL = Label(self.frame1, text='avatar', image=userLogo, bg=darkBlue)
        userLogoL.image = userLogo
        userLogoL.grid(row=0, column=0, columnspan=2, pady=40)
        userNameL = Label(self.frame1, text='userName', image=usernameLogo, bg=darkBlue)
        userNameL.image = usernameLogo
        userNameL.grid(row=1, column=0)
        userNameE = EntryWithPlaceholder(master=self.frame1, textvariable=userNameEString, width=32,
                                         placeholder="username")
        userNameE.grid(row=1, column=1, pady=30, sticky="w", padx=(0, 20))

        passwordL = Label(self.frame1, text='password', image=passLogo, bg=darkBlue)
        passwordL.image = passLogo
        passwordL.grid(row=2, column=0)
        passwordE = EntryWithPlaceholder(master=self.frame1, textvariable=passwordEString, width=32,
                                         placeholder="password")
        passwordE.grid(row=2, column=1, sticky="w", padx=(0, 20))

        loginB = Button(self.frame1, text='login', bg=lightBlue, width=31, height=1,
                        command=lambda: self.loginF(userNameEString, passwordEString))
        loginB.grid(row=3, column=0, columnspan=2, pady=20)
        signUpB = Button(self.frame1, text='sign Up', fg=lightWhite, bg=darkBlue2, width=31, height=1,
                         command=lambda: self.signUpF(userNameEString, passwordEString))
        signUpB.grid(row=4, column=0, columnspan=2)

    def loginF(self, Username, Password):
        username = str(Username.get())
        Password = str(Password.get())
        res = self.backend.employeeLogin(username, Password)

        if len(res) != 0 and type(res) == list:
            self.loginStatus = True
        if self.loginStatus:
            self.login.destroy()
            self.openMain()
        elif res == "password is wrong":
            tkinter.messagebox.showerror("Error", "your password is wrong")
        elif res == "user does not exist":
            tkinter.messagebox.showerror("Error", "your username is wrong")

    def signUpF(self, Username, Password):
        signUp = Toplevel()
        signUp.title("signup")
        signUp.geometry('460x270')
        signUp.resizable(False, False)
        userNameEString = StringVar()
        passwordEString = StringVar()
        userNameL = Label(signUp, text='confirm with the default username and password or an admin confirmation ')
        userNameL.grid(row=0, column=0, columnspan=2, pady=10, padx=(20, 0))
        userNameL = Label(signUp, text='userName:', )
        userNameL.grid(row=1, column=0)
        userNameE = EntryWithPlaceholder(master=signUp, textvariable=userNameEString, width=32,
                                         placeholder="username")
        userNameE.grid(row=1, column=1, pady=30, sticky="w", padx=(0, 20))

        passwordL = Label(signUp, text='password:')
        passwordL.grid(row=2, column=0)
        passwordE = EntryWithPlaceholder(master=signUp, textvariable=passwordEString, width=32,
                                         placeholder="password")
        passwordE.grid(row=2, column=1, sticky="w", padx=(0, 20))
        signUpB = Button(signUp, text='sign Up', fg=lightWhite, bg=darkBlue2, width=40, height=1,
                         command=lambda: checkAdmin(userNameEString, passwordEString))
        signUpB.grid(row=4, column=0, columnspan=2, pady=30)
        resL = Label(signUp, text='')
        resL.grid(row=5, column=0, columnspan=2, pady=10, padx=(20, 0))
        def checkAdmin(Username2, Password2):
            username2 = str(Username2.get())
            Password2 = str(Password2.get())
            res = self.backend.employeeLogin(username2, Password2)
            if len(res) != 0 and type(res) == list:
                username = str(Username.get())
                password = str(Password.get())
                res = self.backend.employeeCreate(username, password)
                resL.config(text="the information is correct . new account created")
                signUp.after(3000, lambda: signUp.destroy())
                return True
            else:
                resL.config(text="wrong information")
                return False


    def openMain(self):
        main = Main()
        main.run()


if __name__ == "__main__":
    login = Login()
    login.run()
