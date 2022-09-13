from tkinter import *
import tkinter as tk


class Dialog(object):
    def __init__(self):
        self.toplevel = tk.Tk()
        self.toplevel.title("Overseer Client")
        self.toplevel.geometry("300x200")
        self.toplevel.configure(bg='black')
        self.toplevel.configure(background="black")
        self.text = Label(self.toplevel, text="Type additional data for registration", background="black", fg="white")
        self.textemail = Label(self.toplevel, text="name", background="black", fg="white")
        self.textpass = Label(self.toplevel, text="surname", background="black", fg="white")
        self.inputtxt = Entry(self.toplevel,
                              width=30,
                              bg="light yellow"
                              )
        self.inputtxtpass = Entry(self.toplevel,
                                  width=30,
                                  bg="light yellow"
                                  )
        self.buttonlogin = tk.Button(self.toplevel, text="REGISTER", command=self.close)

        self.text.pack(side="top")
        self.textemail.pack(pady=5)
        self.inputtxt.pack(pady=5)
        self.textpass.pack(pady=5)
        self.inputtxtpass.pack(pady=5)
        self.buttonlogin.pack(side="bottom", pady=5)
        self.values = None

    def close(self):
        self.values = (self.inputtxt.get(), self.inputtxtpass.get())
        self.toplevel.destroy()

    def show(self):
        self.toplevel.deiconify()
        self.toplevel.wait_window()
        return self.values
