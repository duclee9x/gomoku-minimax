# author: DucLee9x
# Not implement minimax yet
from tkinter import Canvas, Menu, messagebox
import math
import tkinter as tk
import sys
import os
import random


class Board(tk.Frame):
    def __init__(self, master, board_size):
        tk.Frame.__init__(self, master)
        self.pack()
        self.player = Player("Player 1", "O", "blue")
        self.machine = Player("Machine", "X", "red")
        self.score = 0
        self.current_player = self.player
        self.winner = None
        self.footprint = None
        self.ruleLine = 3 if (board_size[0] > 2 and board_size[0] <= 9) else (
            4 if (board_size[0] > 9 and board_size[0] < 13) else 5)
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
        enemy_move = False
        x = math.ceil(event.x / self.distance_x)
        y = math.ceil(event.y / self.distance_y)
        if (self.state[y-1][x-1]) == "":
            self.state[y-1][x-1] = self.current_player.symbol
            self.canvas.create_text(self.distance_x*(x-1)+math.ceil(self.distance_x/2),
                                    self.distance_y*(y-1)+math.ceil(self.distance_y/2), text=self.current_player.symbol, font="sans-serif 25", fill=self.current_player.color)
            enemy_move = True
        else:
            print("Position is taken")
        self.score = self.checkScore()
        print(self.score)

        isWin, winner, self.footprint, isDraw = self.checkState(self.state)
        self.winner = self.traversePlayer(winner)
        self.ifWin(isWin, isDraw)

        if (isWin):
            return
        if (enemy_move):
            player_move = False
            self.changeEnemy()
            while True:
                machine_x = math.floor(random.random()*self.board_size[0])
                machine_y = math.floor(random.random()*self.board_size[1])
                if (self.state[machine_y][machine_x]) == "":
                    self.state[machine_y][machine_x] = self.current_player.symbol
                    self.canvas.create_text(self.distance_x*(machine_x)+math.ceil(self.distance_x/2),
                                            self.distance_y*(machine_y)+math.ceil(self.distance_y/2), text=self.current_player.symbol, font="sans-serif 25", fill=self.current_player.color)
                    #print(machine_y, machine_x)
                    break
                else:
                    print("Position is taken")
            isWin, winner, self.footprint, isDraw = self.checkState(self.state)
            self.winner = self.traversePlayer(winner)
            self.ifWin(isWin, isDraw)

            player_move = True

            # print(self.state)
            if player_move:
                self.changeEnemy()

    def ifWin(self, isWin, isDraw):
        if isWin != False:
            print(self.winner.name, self.winner.symbol)
            messagebox.showinfo(
                "Game Over!!!!", "Winner is {}, {}".format(self.winner.name, self.winner.symbol))
            self.canvas.create_line(self.distance_x*self.footprint[0][1]+math.ceil(self.distance_x/2), self.distance_y*self.footprint[0][0]+math.ceil(
                self.distance_y/2), self.distance_x*self.footprint[(self.ruleLine-1)][1]+math.ceil(self.distance_x/2), self.distance_y*self.footprint[(self.ruleLine-1)][0]+math.ceil(self.distance_y/2), fill=self.winner.color, width=2)
            self.canvas.config(state='disabled')
            self.canvas.unbind("<Button 1>")
        if isDraw:
            messagebox.showinfo("Game Over", "This game is Draw!!!")

    def checkState(self, state):
        isWin = False
        winner = None
        isDraw = True
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
        for row in range(self.board_size[0]):
            for col in range(self.board_size[1]):
                if state[row][col] == '':
                    isDraw = False
                    break
        return isWin, winner, footprint, isDraw

    def checkScore(self):
        score1 = self.calcScorePlayer(
            self.state, self.player)
        score2 = self.calcScorePlayer(self.state, self.machine)
        print("1: {}, 2: {}".format(score1, score2))
        return score1-score2

    def calcScorePlayer(self, state, player):
        enemy = self.getEnemy(player)
        sum = 0
        for row in range(self.board_size[0]):
            for col in range(self.board_size[1]-(self.ruleLine-1)):
                count = 0
                if state[row][col] != player.symbol:
                    continue
                for i in range(1, self.ruleLine):
                    if (state[row][col+i] == enemy.symbol):
                        break
                    elif(state[row][col] == state[row][col + i]):
                        count += 1
                    else:
                        continue
                sum += pow(3, count)

        for row in range(self.board_size[0]-(self.ruleLine-1)):
            for col in range(self.board_size[1]):
                count = 0
                if state[row][col] != player.symbol:
                    continue
                for i in range(1, self.ruleLine):
                    if (state[row+i][col] == enemy.symbol):
                        break
                    elif(state[row][col] == state[row+i][col]):
                        count += 1
                    else:
                        continue
                sum += pow(3, count)

        for row in range(self.board_size[0]-(self.ruleLine-1)):
            for col in range(self.board_size[1]-(self.ruleLine-1)):
                count = 0
                if state[row][col] != player.symbol:
                    continue
                for i in range(1, self.ruleLine):
                    if (state[row+i][col+i] == enemy.symbol):
                        break
                    elif(state[row][col] == state[row+i][col+i]):
                        count += 1
                    else:
                        continue
                sum += pow(3, count)

        for row in range(self.board_size[0]):
            for col in range(self.board_size[1]):
                count = 0

                if state[row][col] != player.symbol:
                    continue
                for i in range(1, self.ruleLine):
                    if (row + i <= (self.board_size[0]-1) and col-i >= 0):
                        if (state[row+i][col-i] == enemy.symbol):
                            break
                        elif(state[row][col] == state[row+i][col-i]):
                            count += 1
                        else:
                            continue
                    else:
                        break
                sum += pow(3, count)

        return sum

    def traversePlayer(self, symbol):
        if self.player.symbol == symbol:
            return self.player
        else:
            return self.machine

    def getEnemy(self, player):
        return self.machine if player == self.player else self.player

    def changeEnemy(self):
        self.current_player = self.machine if self.current_player == self.player else self.player


class Player:
    def __init__(self, name, symbol, color):
        self.symbol = symbol
        self.color = color
        self.name = name


class App(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.board = Board(self.master, [20, 20])
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


# Testing
# def analyzeHorizontalForAI(self, current_turn):
#     score = 0
#     countConsecutive = 0
#     openEnds = 0

#     for i in range(self.board_size[0]):
#         for a in range(self.board_size[1]):
#             if (self.board[i][a] == 'X'):
#                 countConsecutive += 1
#             elif (self.board[i][a] == ' ' and countConsecutive > 0):
#                 openEnds += 1
#                 score += gomokuShapeScore(countConsecutive,
#                                           openEnds, current_turn == self.machine)
#                 countConsecutive = 0
#                 openEnds = 1

#             elif (self.board[i][a] == ' '):
#                 openEnds = 1
#             elif (countConsecutive > 0):
#                 score += gomokuShapeScore(countConsecutive,
#                                           openEnds, current_turn == self.machine)
#                 countConsecutive = 0
#                 openEnds = 0
#             else:
#                 openEnds = 0
#         if (countConsecutive > 0):
#             score += gomokuShapeScore(countConsecutive,
#                                       openEnds, current_turn == self.machine)
#         countConsecutive = 0
#         openEnds = 0
#     return score


# def gomokuShapeScore(consecutive, openEnds, currentTurn):
# 	if (openEnds == 0 and consecutive < 5):
# 		return 0
# 	elif (consecutive == 4):
#         if openEnds == 1:
#             if (currentTurn):
#                 return 100000000
#             return 50
#         elif (openEnds == 2):
#             if (currentTurn)
#                 return 100000000
#             return 500000
#     elif (consecutive ==3):
# 		if (openEnds==1):
#             if (currentTurn)
# 				return 7
# 			return 5
# 		elif (openEnds==2):
# 			if (currentTurn)
# 				return 10000
# 			return 50

# 	elif (consecutive==2):
# 		if (openEnds==1):
# 			return 2
# 		elif (openEnds==2):
# 			return 5
# 	elif (consecutive ==1):
# 		if (openEnds ==1):
# 			return 0.5
# 		elif (openEnds ==2):
# 			return 1
# 	else:
# 		return 200000000

# def bestGomokuMove(AIturn, depth) {
# 	xBest = -1, yBest = -1
# 	bestScore = -1000000000 if AIturn else 1000000000
# 	analysis, response
# 	analTurn = AIturn if depth % 2 === 0 else not AIturn
# 	moves = get_moves()

# 	for (i = moves.length-1 i > moves.length - aiMoveCheck - 1
# 		and i >= 0 i--):
# 		board[moves[i][1]][moves[i][2]] = color
# 		if (depth == 1):
# 			analysis = analyzeGomoku(analTurn)
# 		else:
# 			response = bestGomokuMove(not bturn, depth - 1)
# 			analysis = response[2]

# 		board[moves[i][1]][moves[i][2]] = ' '
# 		if ((analysis > bestScore and bturn) or
# 			(analysis < bestScore and notbturn)):
# 			bestScore = analysis
# 			xBest = moves[i][1]
# 			yBest = moves[i][2]
# 	return [xBest, yBest, bestScore]
