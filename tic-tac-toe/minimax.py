#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 15 14:58:58 2021

@author: philip
"""
import random
from math import inf as infinity
from random import choice

HUMAN = -1
COMPUTER = +1
board = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
]


#create a function to show the initial instructions
def instructions():
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
    
#function for evaluation
# +1 if the computer is winning
# -1 if the computer lose
# 0 if draw
def evaluate(board):
    if isWinner(board, HUMAN):
        score = -1
    elif isWinner(board, COMPUTER):
        score =  +1
    else:
        score = 0
    return score

#Function to define all the winning possibilities:
#VERT left, middle. right
#HORIZONTAL up, middle, down
#DIAG left, right
def isWinner(board, mark):
    win_board = [
        [board[0][0], board[0][1], board[0][2]],
        [board[1][0], board[1][1], board[1][2]],
        [board[2][0], board[2][1], board[2][2]],
        [board[0][0], board[1][0], board[2][0]],
        [board[0][1], board[1][1], board[2][1]],
        [board[0][2], board[1][2], board[2][2]],
        [board[0][0], board[1][1], board[2][2]],
        [board[2][0], board[1][1], board[0][2]],
    ]
    if [mark, mark, mark] in win_board:
        return True
    else:
        return False

#Function to determine that the game is over
def end_game(board):
    return isWinner(board, HUMAN) or isWinner(board, COMPUTER)

#Function that returns which cells are empty
def isEmpty(board):
    cells = list()
    for x, row in enumerate(board):
        for y, cell in enumerate(row):
            if cell == 0:
                cells.append([x, y])
    return cells

#Function to determine the validity of the move
#You can place your character on an empty slot
def isValid(x,y):
    if [x,y] in isEmpty(board):
        return True
    else:
        return False

#Function for inserting the letter/move
def insertLetter(x,y,player):
    if isValid(x, y):
        board[x][y] = player
        return True
    else:
        return False
    
#Create the minimax function
def minimax(board, depth, player):
    if player == COMPUTER:
        bestMove = [-1, -1, -infinity]
    elif player == HUMAN:
        bestMove = [-1, -1, +infinity]

    if depth == 0 or end_game(board):
        score = evaluate(board)
        return [-1, -1, score]

    for i in isEmpty(board):
        x, y = i[0], i[1]
        board[x][y] = player
        score = minimax(board, depth - 1, -player)
        board[x][y] = 0
        score[0], score[1] = x, y

        if player == COMPUTER:
            if score[2] > bestMove[2]:
                bestMove = score
        else:
            if score[2] < bestMove[2]:
                bestMove = score
    #print("Best Possible Score: " + str(bestMove))
    return bestMove

def display_board(board, computer_choice, human_choice):
    moves = {
            -1: human_choice,
            +1: computer_choice,
            0: " "
            }
    print("\nBoard State")
    print("---------------")
    for i in board:
        for j in i:
            symbol = moves[j]
            print("| " + symbol + " |", end = '')
        print("\n---------------")

def comp_move(comp_choice, human_choice):
    depth = len(isEmpty(board))
    if depth == 0 or end_game(board):
        return
    
    if depth == 9:
        x = choice([0, 1, 2])
        y = choice([0, 1, 2])
    else:
        move = minimax(board, depth, COMPUTER)
        x, y = move[0], move[1]

    insertLetter(x, y, COMPUTER)
    
def human_move(comp_choice, human_choice):
    depth = len(isEmpty(board))
    if depth == 0 or end_game(board):
        return
    move = -1
    moves = {
        1: [0, 0], 2: [0, 1], 3: [0, 2],
        4: [1, 0], 5: [1, 1], 6: [1, 2],
        7: [2, 0], 8: [2, 1], 9: [2, 2],
    }
    
    while move < 1 or move > 9:
        move = int(input("Enter your move, human! (1-9): "))
        coord = moves[move]
        can_move = insertLetter(coord[0], coord[1], HUMAN)

        if not can_move:
            print("Place already marked, please choose another cell")
            move = -1

if __name__ == "__main__":
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
    human_choice = ""
    computer_choice = ""
    while not (human_choice == 'X' or human_choice == 'O'):
        human_choice = input("Choose your fighter (X/O): ").upper()
    
    if human_choice == "X":
        computer_choice = "O"
    else:
        computer_choice = "X"
    
    print("Randomly picking initial player...")
    randomizer = random.randint(1,2)
    if randomizer == 2:
        print("Human goes first")
    else:
        print("Computer goes first")
        
    while len(isEmpty(board)) > 0 and not end_game(board):
        if randomizer == 1:
            comp_move(computer_choice, human_choice)
            randomizer = ''

        display_board(board, computer_choice, human_choice)
        human_move(computer_choice, human_choice)
        comp_move(computer_choice, human_choice)
   
    # Game over message
    if isWinner(board, HUMAN):
        display_board(board, computer_choice, human_choice)
        print("Congratulations, human! You're smart!")
    elif isWinner(board, COMPUTER):
        display_board(board, computer_choice, human_choice)
        print("Better luck next time, human!")
    else:
        display_board(board, computer_choice, human_choice)
        print("Great minds think alike. It's a tie!")