from tkinter import Canvas, Menu, messagebox
import math
import tkinter as tk
import sys
import os


class Board(tk.Frame):
    def __init__(self, master, board_size):
        tk.Frame.__init__(self, master)
        self.pack()
        self.player1 = Player("Player 1", "O", "blue")
        self.player2 = Player("Player 2", "X", "red")

        self.current_player = self.player1
        self.winner = None
        self.footprint = None
        self.ruleLine = board_size[0] if board_size[0] < 5 else 5
        self.board_size = board_size
        self.state = [["" for x in range(board_size[0])]
                      for y in range(board_size[1])]

        self.canvas = Canvas(self, width=600,
                             height=600, background="#fff", confine=False, state='normal')
        canvas_size = 600
        self.distance_x = canvas_size / self.board_size[0]
        self.distance_y = canvas_size / self.board_size[1]
        for i in range(1, self.board_size[0]+1):
            self.canvas.create_line(i*self.distance_x, 0, i*self.distance_x,
                                    canvas_size, fill='black')
        for i in range(1, self.board_size[1]+1):
            self.canvas.create_line(0, i*self.distance_y, canvas_size,
                                    i*self.distance_y, fill='black')
        self.canvas.bind("<Button 1>", self.makeMove)
        self.canvas.pack()

    def makeMove(self, event):
        x = math.ceil(event.x / self.distance_x)
        y = math.ceil(event.y / self.distance_y)
        if (self.state[y-1][x-1]) == "":
            self.state[y-1][x-1] = self.current_player.symbol
            self.canvas.create_text(self.distance_x*(x-1)+math.ceil(self.distance_x/2),
                                    self.distance_y*(y-1)+math.ceil(self.distance_y/2), text=self.current_player.symbol, font="sans-serif 130", fill=self.current_player.color)
            self.changeEnemy()
        else:
            print("Position is taken")
        isWin, winner, self.footprint = self.checkState(self.state)
        self.winner = self.traversePlayer(winner)
        if isWin != False:
            print(self.winner.name, self.winner.symbol)
            messagebox.showinfo(
                "Game Over!!!!", "Winner is {}, {}".format(self.winner.name, self.winner.symbol))
            self.canvas.create_line(self.distance_x*self.footprint[0][1]+math.ceil(self.distance_x/2), self.distance_y*self.footprint[0][0]+math.ceil(
                self.distance_y/2), self.distance_x*self.footprint[(self.ruleLine-1)][1]+math.ceil(self.distance_x/2), self.distance_y*self.footprint[(self.ruleLine-1)][0]+math.ceil(self.distance_y/2), fill=self.winner.color, width=2)
            self.canvas.config(state='disabled')
            self.canvas.unbind("<Button 1>")

    def checkState(self, state):
        isWin = False
        winner = None
        footprint = [None for x in range(self.ruleLine)]
        for row in range(self.board_size[0]):
            for col in range(self.board_size[1]-(self.ruleLine-1)):
                win = 0
                if state[row][col] == '':
                    continue
                for i in range(1, self.ruleLine):
                    if(state[row][col] == state[row][col + i]):
                        win += 1
                        if(win == self.ruleLine-1):
                            isWin = True
                            winner = state[row][col]
                            footprint = [[row, col+x]
                                         for x in range(self.ruleLine)]
                            break
                    else:
                        break

        for row in range(self.board_size[0]-(self.ruleLine-1)):
            for col in range(self.board_size[1]):
                win = 0
                if state[row][col] == '':
                    continue
                for i in range(1, self.ruleLine):
                    if(state[row][col] == state[row+i][col]):

                        win += 1
                        if(win == self.ruleLine-1):  # <-indicates 5 items matched in a row
                            isWin = True
                            winner = state[row][col]
                            footprint = [[row+x, col]
                                         for x in range(self.ruleLine)]
                            break
                    else:
                        break
        for row in range(self.board_size[0]-(self.ruleLine-1)):
            for col in range(self.board_size[1]-(self.ruleLine-1)):
                win = 0
                if state[row][col] == '':
                    continue
                for i in range(1, self.ruleLine):
                    if(state[row][col] == state[row+i][col+i]):
                        win += 1
                        if(win == (self.ruleLine-1)):  # <-indicates 5 items matched in a row
                            isWin = True
                            winner = state[row][col]
                            footprint = [[row+x, col+x]
                                         for x in range(self.ruleLine)]
                            break
                    else:
                        break

        for row in range(self.board_size[0]):
            for col in range(self.board_size[1]):
                win = 0

                if state[row][col] == '':
                    continue
                for i in range(1, self.ruleLine):
                    if (row + i <= (self.board_size[0]-1) and col-i >= 0):
                        if(state[row][col] == state[row+i][col-i]):
                            win += 1
                            if(win == (self.ruleLine-1)):  # <-indicates 5 items matched in a row
                                isWin = True
                                winner = state[row][col]
                                footprint = [[row+x, col-x]
                                             for x in range(self.ruleLine)]
                                break
                        else:
                            break
                    else:
                        break

        return isWin, winner, footprint

    def traversePlayer(self, symbol):
        if self.player1.symbol == symbol:
            return self.player1
        else:
            return self.player2

    def changeEnemy(self):
        self.current_player = self.player2 if self.current_player == self.player1 else self.player1


class Player:
    def __init__(self, name, symbol, color):
        self.symbol = symbol
        self.color = color
        self.name = name


class App(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.board = Board(self.master, [3, 3])
        self.initMenubar()
        self.master.bind('<Escape>', self.exitWindow)

    def initMenubar(self):
        menubar = Menu(self.master)
        self.master.config(menu=menubar)

        fileMenu = Menu(menubar)
        fileMenu.add_command(label="Restart", command=self.restart)
        fileMenu.add_command(label="Exit", command=self.master.destroy)
        menubar.add_cascade(label="File", menu=fileMenu)

    def restart(self):
        python = sys.executable
        os.execl(python, python, * sys.argv)

    def exitWindow(self, event=None):
        self.master.destroy()


root = tk.Tk()
# menu = Menu(root)
# root.config(menu=menu)
# filemenu = Menu(menu)
# filemenu.add_command(label="Restart", command=restart)
app = App(root)
app.mainloop()
