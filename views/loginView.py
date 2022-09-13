from tkinter import *
import tkinter as tk


class Dialog(object):
    def __init__(self):
        self.toplevel = tk.Tk()
        self.toplevel.title("Overseer Client")
        self.toplevel.geometry("300x300")
        self.toplevel.configure(bg='black')
        self.toplevel.configure(background="black")
        self.text = Label(self.toplevel, text="Please login", background="black", fg="white")
        self.textemail = Label(self.toplevel, text="email", background="black", fg="white")
        self.textpass = Label(self.toplevel, text="password", background="black", fg="white")
        self.inputtxt = Entry(self.toplevel,
                                       width=30,
                                       bg="light yellow"
                                       )
        self.inputtxtpass = Entry(self.toplevel,
                              width=30,
                              bg="light yellow"
                              )
        self.buttonlogin = tk.Button(self.toplevel, text="LOGIN", command=self.close)
        self.buttonregister = tk.Button(self.toplevel, text="REGISTER", command=self.register)

        self.text.pack(side="top")
        self.textemail.pack(pady=5)
        self.inputtxt.pack(pady=5)
        self.textpass.pack(pady=5)
        self.inputtxtpass.pack(pady=5)
        self.buttonlogin.pack(side="bottom", pady=5)
        self.buttonregister.pack(side="bottom", pady=5)
        self.values = [False, None, None]

    def register(self):
        self.values = list(self.values)
        self.values[0] = True
        self.values = tuple(self.values)
        self.close()

    def close(self):
        self.values = list(self.values)
        self.values[1] = self.inputtxt.get()
        self.values[2] = self.inputtxtpass.get()
        self.values = tuple(self.values)
        self.toplevel.destroy()

    def show(self):
        self.toplevel.deiconify()
        self.toplevel.wait_window()
        return self.values
