#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 7 21:09:21 2021

@author: philip
"""

import random

#Have the initial setup of the board according to the initial instructions
def display(cell):
    print("**************************")
    print("| " + cell[1] + " | " + cell[2] + " | " + cell[3])
    print("------------")
    print("| " + cell[4] + " | " + cell[5] + " | " + cell[6])
    print("------------")
    print("| " + cell[7] + " | " + cell[8] + " | " + cell[9])
    print("------------")

"""
Setup on how to win the game:
Winning the game means having 3 consecutive marks on
Top Horizontal, Middle Horizontal, Bottom Horizontal,
Left Vertical, Middle Vertical, Right Vertical
Left Diagonal, and Right diagonal
"""
def isWinner(board, marks):
    return((board[1] == marks and board[2] == marks and board[3] == marks) or #Top horizontal
		(board[4] == marks and board[5] == marks and board[6] == marks) or #Middle horizontal
		(board[7] == marks and board[8] == marks and board[9] == marks) or #Bottom Horizontal
		(board[1] == marks and board[4] == marks and board[7] == marks) or #Left Vertical
		(board[2] == marks and board[5] == marks and board[8] == marks) or #middle Vertical
		(board[3] == marks and board[6] == marks and board[9] == marks) or #Right Vertical
		(board[1] == marks and board[5] == marks and board[9] == marks) or #Left Diagonal
		(board[3] == marks and board[5] == marks and board[7] == marks)) #Right Diagonal

#Create a function that will return who is X and who is O
def marker():
    marker = ""
    while not (marker == 'X' or marker == 'O'):
        marker = input("Choose your fighter (X/O): ").upper()
    if marker == "X":
        return ["X","O"]
    else:
        return ["O","X"]

def initialMove(turn):
    if turn == 1:
        return 1
    elif turn == 2:
        return 2

def isFree(board, move):
    return board[move] == ' '

def isFull(board):
    for i in range(1, 10):
        if isFree(board, i):
            return False
    return True

#Get the possible moves of human
def humanMove(cell):
    move = ' '
    while move not in [1,2,3,4,5,6,7,8,9] or not isFree(cell, move):
        move = int(input("Please enter the location of your move: "))
    return move

#Create a function for possible random moves of the computer
def randMoves(board, moves):
    freeMoves = list()
    for i in moves:
        if isFree(board, i):
            freeMoves.append(i)
    
    if len(freeMoves) !=0:
        return random.choice(freeMoves)
    else:
        return None

#Create a peek function for intelligence = 1
def peek(board):
    boardList = list()
    
    #Copy the board contents
    for i in board:
        boardList.append(i)
        
    return boardList

def computerMove(board, marker, intelligence):
    if marker == "X":
        human = "O"
    else: human = "X"
        
    if intelligence == 0:
        compMove = randMoves(board, [1,2,3,4,5,6,7,8,9])
        if compMove != None:
            return compMove
        
    elif intelligence == 1:
        for i in range(1,10):
            copyBoard = peek(board)
            if isFree(copyBoard, i):
                allMovements(copyBoard, marker, i)
                if isWinner(copyBoard, marker):
                    return i

        for i in range(1,10):
            peekBoard = peek(board)
            if isFree(peekBoard, i): #check whether if the slot 1-9 is filled
                allMovements(peekBoard, human, i) #try to put the human letter on the slot
                if isWinner(peekBoard, human): #check if winner, return it if winner
                    return i

        #If the center is free, take it.
        if isFree(board, 5):
            return 5

        #Get a corner so that there will be a corner block
        cornerMove = randMoves(board, [1,3,7,9])
        if cornerMove != None:
            return cornerMove

        compMove = randMoves(board, [1,2,3,4,5,6,7,8,9])
        if compMove != None:
            return compMove
    
    elif intelligence == 2:
        pass
                
    
def minimax(board, depth, isMaximizing):
    if isWinner(board, computer):
        return 1
    elif isWinner(board, human):
        return -1
        
#Record all the moves:
def allMovements(board, marker, move):
    board[move] = marker #mark the move on the marker
    
if __name__ == '__main__':
    print("=======Tic-Tac-Toe=======")
    print("Board instructions:")
    print("Enter your move according to the corresponding board location number")
    print("**************************")
    print("| " + str(1) + " | " + str(2) + " | " + str(3))
    print("------------")
    print("| " + str(4) + " | " + str(5) + " | " + str(6))
    print("------------")
    print("| " + str(7) + " | " + str(8) + " | " + str(9))
    print("------------")
    #score_max = int(input())
    intelligence_level = int(input("Enter how smart would you like the computer to be (0-1): "))
    while (True):
        #initialize the board
        board = [' '] * 10 #10 Blank spaces
        human, computer = marker()
        print("Randomly picking initial player...")
        randomizer = random.randint(1,2)
        if randomizer == 1:
            print("Human goes first")
        else:
            print("Computer goes first")
        turn = initialMove(randomizer)
        commencing = True
        while(commencing):
            if turn == 1: #Human Turn
                display(board)
                move = humanMove(board)
                allMovements(board, human, move)
                
                if isWinner(board, human):
                    display(board)
                    print("Congratulations, human! You're smart!")
                    commencing = False
                else:
                    if isFull(board):
                        display(board)
                        print("Great minds think alike")
                        break
                    else:
                        turn = 2
            else:
                move = computerMove(board, computer, intelligence_level)
                allMovements(board, computer, move)

                if isWinner(board, computer) and (intelligence_level == 0):
                    display(board)
                    print("The computer luckily won!")
                    commencing = False
                elif isWinner(board, computer) and ((intelligence_level == 1) or (intelligence_level == 2)):
                    display(board)
                    print("Better luck next time, human!")
                    commencing = False
                else:
                    if isFull(board):
                        display(board)
                        print("Great minds think alike")
                        break
                    else:
                        turn = 1
        break