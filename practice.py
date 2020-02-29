# author: DucLee9x
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import subprocess
from tkinter import Canvas
import math
from test import Board


class App(tk.Frame):
    def __init__(self, master):

        tk.Frame.__init__(self, master)
        self.pack()

        # self.master.resizable(False, False)
        self.master.tk_setPalette(background="#cecece")
        self.master.title("Welcome")

        x = (self.master.winfo_screenwidth() -
             self.master.winfo_reqwidth())
        y = self.master.winfo_screenheight() * 0.9

        self.master.geometry("{}x{}".format(round(x), round(y)))

        header = tk.Frame(self)
        header.pack()
        tk.Label(header, text="Welcome to my first App with Tkinter").pack()
        self.text = tk.Entry(header)
        self.text.pack()

        body = tk.Frame(self)
        body.pack(pady=10, anchor='e')
        tk.Button(body, text="Show Text", default='active',
                  command=self.showText).pack(side='right')
        tk.Button(body, text="Exit", command=self.exitWindow).pack(
            side='right')
        self.master.config(menu=tk.Menu(self.master))

        self.master.protocol('WM_DELETE_WINDOW', self.exitWindow)
        self.master.bind('<Escape>', self.exitWindow)
        self.board_size = [20, 20]
        board = Board(self.master, self.board_size)
        board.destroy()
        self.pack()

    def showText(self, event=None):
        messagebox.showinfo("Info", self.text.get())
        self.master.destroy()

    def exitWindow(self, event=None):
        print("Exit Window...")
        self.master.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
