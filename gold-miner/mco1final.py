#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 1 17:37:28 2021

@author: philip
"""

#Initialize all the markers
face_north = "^"
face_south = "v"
face_east = ">"
face_west = "<"
gold = "G"
pit = "P"
beacon = "B"

import random

#Create the Agent class, this will be the player of the game
class Agent():
    #Initialize an empty list to store the pits for intelligence 2
    pits = list()
    total_rotations = list()
    total_movements = list()
    def __init__(self, row, col, movements, rotations, scans):
        self.row = row
        self.col = col
        self.marker = face_east #this is the initial face of the agent > at point 0,0
        self.rotations = rotations
        self.movements = movements
        self.scans = scans
   
    def rotate(self, nodes):
        pointer = random.randint(1,4)
        if pointer == 1 and 0 < self.row: #if you are not in the highest row, you can face north
            self.marker = face_north
        elif pointer == 2 and self.row < (nodes-1): #if you are not in the lowest row, you can face south
            self.marker = face_south
        elif pointer == 3 and self.col < (nodes-1): #if you are not in the rightmost, you can face east
            self.marker = face_east
        elif pointer == 4 and self.col > 0: #if you are not in the leftmost, face west
            self.marker = face_west
        self.rotations += 1
    
    def scan(self, maze, nodes):
        if self.marker == face_north and self.row > 0 and  maze[self.row - 1][self.col] != pit:
            return 1
        elif self.marker == face_south and 0 <= self.row < (nodes - 1) and maze[self.row + 1][self.col] != pit:
            return 2
        elif self.marker == face_east and 0 <= self.col < (nodes - 1) and maze[self.row][self.col + 1] != pit:
            return 3
        elif self.marker == face_west and self.col > 0 and maze[self.row][self.col - 1] != pit:
            return 4
        self.scans += 1
        
    def is_stuck(self, maze, nodes):
        #If agent on the left most column
        if (0 <= self.row < (nodes-1) and self.col == 0) and (maze[self.row-1][self.col] == "-" and maze[self.row + 1][self.col] == "-" and maze[self.row][self.col + 1] == "-"):
            return True
        elif (0 <= self.row < (nodes-1) and self.col == 0) and (maze[self.row-1][self.col] == "P" and maze[self.row + 1][self.col] == "P" and maze[self.row][self.col + 1] == "P"):
            return True
        
        #If agent is not 
        elif (0 <= self.row < (nodes - 1) and self.col == (nodes - 1)) and (maze[self.row - 1][self.col] == "-" and maze[self.row + 1][self.col] == "-" and maze[self.row][self.col - 1] == "-"):
            return True
        elif (0 <= self.row < (nodes - 1) and self.col == (nodes - 1)) and (maze[self.row - 1][self.col] == "P" and maze[self.row + 1][self.col] == "P" and maze[self.row][self.col - 1] == "P"):
            return True
        
        #
        elif (self.row == (nodes - 1) and self.col == (nodes - 1)) and (maze[self.row - 1][self.col] == "-" and maze[self.row][self.col - 1] == "-"):
            return True
        elif (self.row == (nodes - 1) and self.col == (nodes - 1)) and (maze[self.row - 1][self.col] == "P" and maze[self.row][self.col - 1] == "P"):
            return True
        
        elif (0 < self.row < (nodes - 1) and 0 < self.col < (nodes - 1) and (maze[self.row + 1][self.col] == "-" and maze[self.row - 1][self.col] == "-" and maze[self.row][self.col + 1] == "-" and maze[self.row][self.col - 1] == "-")
        ):
            return True
        elif (0 < self.row < (nodes - 1) and 0 < self.col < (nodes - 1) and (maze[self.row + 1][self.col] == "P" and maze[self.row - 1][self.col] == "P" and maze[self.row][self.col + 1] == "P" and maze[self.row][self.col - 1] == "P")
        ):
            return True
        
        elif (self.row == 0 and 0 <= self.col < (nodes - 1)) and ((maze[self.row][self.col + 1] == "-" and maze[self.row + 1][self.col] == "-")
            or (maze[self.row + 1][self.col] == "-" and maze[self.row][self.col + 1] == "-" and maze[self.row][self.col - 1] == "-")):
            return True
        elif (self.row == 0 and 0 <= self.col < (nodes - 1)) and ((maze[self.row][self.col + 1] == "P" and maze[self.row + 1][self.col] == "P")
            or (maze[self.row + 1][self.col] == "P" and maze[self.row][self.col + 1] == "P" and maze[self.row][self.col - 1] == "P")):
            return True
        
        elif (self.row == 0 and self.col == (nodes - 1)) and (maze[self.row + 1][self.col] == "-" and maze[self.row][self.col - 1] == "-"):
            return True
        elif (self.row == 0 and self.col == (nodes - 1)) and (maze[self.row + 1][self.col] == "P" and maze[self.row][self.col - 1] == "P"):
            return True
        
        elif (self.row == (nodes - 1) and 0 <= self.col < (nodes - 1)) and (
            (maze[self.row - 1][self.col] == "-" and maze[self.row][self.col + 1] == "-")
            or (maze[self.row - 1][self.col] == "-" and maze[self.row][self.col - 1] == "-" and maze[self.row][self.col + 1] == "-")
        ):
            return True
        elif (self.row == (nodes - 1) and 0 <= self.col < (nodes - 1)) and (
            (maze[self.row - 1][self.col] == "P" and maze[self.row][self.col + 1] == "P")
            or (maze[self.row - 1][self.col] == "P" and maze[self.row][self.col - 1] == "P" and maze[self.row][self.col + 1] == "P")
        ):
            return True
    
    def forward(self, maze, nodes, intelligence):
        if intelligence == 0: #Intelligence zero moves the agent randomly until a gold or pit is discovered
            self.rotate(nodes)
            if self.marker == face_north and 0 < self.row:
                self.row -= 1
            elif self.marker == face_south and 0 <= self.row < (nodes-1):
                self.row += 1
            elif self.marker == face_east and 0 <= self.col < (nodes-1):
                self.col += 1
            elif self.marker == face_west and self.col > 0:
                self.col -= 1
        elif intelligence == 5: #Intelligence 1's rationallity is no backtracking
            while True:
                self.rotate(nodes)
                if (
                    self.marker == face_south
                    and 0 <= self.row < (nodes - 1)
                    and maze[self.row + 1][self.col] != "-"
                ):
                    self.row += 1
                    break
                elif (
                    self.marker == face_east
                    and 0 <= self.col < (nodes - 1)
                    and maze[self.row][self.col + 1] != "-"
                ):
                    self.col += 1
                    break
                elif (
                    self.marker == face_west
                    and self.col > 0
                    and maze[self.row][self.col - 1] != "-"
                ):
                    self.col -= 1
                    break
                elif (
                    self.marker == face_north
                    and self.row > 0
                    and maze[self.row - 1][self.col] != "-"
                ):
                    self.row -= 1
                    break
        elif intelligence == 1: #This level remembers all the pits it passed through and skips it
            while True:
                self.rotate(nodes)
                if (
                    self.marker == face_south
                    and 0 <= self.row < (nodes - 1)
                    and [self.row+1, self.col] not in self.pits
                ):
                    self.row += 1
                    break
                elif (
                    self.marker == face_east
                    and 0 <= self.col < (nodes - 1)
                    and [self.row,self.col + 1] not in self.pits
                ):
                    self.col += 1
                    break
                elif (
                    self.marker == face_west
                    and self.col > 0
                    and [self.row, self.col - 1] not in self.pits
                ):
                    self.col -= 1
                    break
                elif (
                    self.marker == face_north
                    and self.row > 0
                    and [self.row - 1, self.col] not in self.pits
                ):
                    self.row -= 1
                    break
        elif intelligence == 2: #has a power called scan but cant backtrack
            while True:
                self.rotate(nodes)
                scanner = self.scan(maze, nodes)
                self.scans += 1
                if (self.marker == face_south and 0 <= self.row < (nodes - 1) and scanner == 2) and maze[self.row + 1][self.col] != "-":
                    self.row += 1
                    break
                elif (self.marker == face_east and 0 <= self.col < (nodes - 1) and scanner == 3) and maze[self.row][self.col + 1] != "-":
                    self.col += 1
                    break
                elif (self.marker == face_west and self.col > 0 and scanner == 4) and maze[self.row][self.col - 1] != "-":
                    self.col -= 1
                    break
                elif (self.marker == face_north and self.row > 0 and scanner == 1) and maze[self.row - 1][self.col] != "-":
                    self.row -= 1
                    break
                if self.is_stuck(maze, nodes):
                    return True
        self.movements += 1
    
    
    
#Create the function that would initialize the maze
def init_maze(n):
    maze = [["*" for i in range(n)] for j in range(n)]
    return maze 
    #we return the maze here so that we can unpack it later on
    #This function will return an n by n list


"""
Now that we have the nxn list, we can now create a function to "paste" the
agent, the pits, beacons, and gold here.
"""
#This function takes 6 parameters, it will also unpack/return 6 parameters
#Final Maze, Agent location, goldx, goldy, pit coordinates and beacon coordinates
def setup_maze(maze, agent, goldx, goldy, pit_coordinates, beacon_coordinates):
    maze[goldx][goldy] = gold
    maze[agent.row][agent.col] = agent.marker #This will be > initially
       
    for coordinates in pit_coordinates:
        maze[coordinates[0]][coordinates[1]] = pit   

    for coordinates in beacon_coordinates:
        maze[coordinates[0]][coordinates[1]] = beacon
        
    return maze, goldx, goldy, pit_coordinates, beacon_coordinates

#Create the function that will display the final maze
def display_maze(maze, agent, failures):
    maze[agent.row][agent.col] = agent.marker
    n_movements = agent.movements
    rotations = agent.rotations
    n_scans = agent.scans
    for i in maze:
        print(*i, sep = "\t")
    print("Number of movements: " + str(n_movements))
    print("Number of failures/pits encountered: " + str(failures))
    print("Number of rotations done: " +str(rotations))
    print("Number of scans done: " +str(n_scans))
    
if __name__ == "__main__":
    agent = Agent(row = 0, col = 0, movements = 0, rotations = 0, scans = 0)
    cells = int(input("Please enter the size of your matrix: ")) #Edit the raiseValueError here to limit the size to only 8-50
    if 8 > cells or cells > 50:
        raise ValueError("Please input a number from 8 to 50")
    maze = init_maze(cells) #initialize the maze
    #Enter the inputs for setting up the maze
    #GOLD LOCATION
    goldx = int(input("Enter the X coordinate of gold: "))
    goldy = int(input("Enter the Y coordinate of gold: "))
    
    #PITS
    pit_coordinates = list() #initialize empty list to store the pit coordinates
    n_pits = int(input("Enter the number of pits: "))
    for i in range(n_pits):
        pitx = int(input("X location of pit "+str(i)+ " :"))
        pity = int(input("Y location of pit "+str(i)+ " :"))
        pitxy = [pitx, pity]
        pit_coordinates.append(pitxy)
    
    #BEACONS
    beacon_coordinates = list()
    n_beacon = int(input("Enter the number of beacons: "))
    for i in range(n_beacon):
        beaconx = int(input("X location of Beacon "+str(i) +" :"))
        beacony = int(input("Y location of Beacon "+str(i) +" :"))
        beaconxy = [beaconx, beacony]
        beacon_coordinates.append(beaconxy)
    
    #Now that we initialized the Agent, maze, goldx, gold, pit coordiantes, and beacon coordinates,
    #We can now paste/setup these values to the initial maze returned by the init_maze function
    #We also unpack these values because these are the values where our Agent will rely on
    fmaze, goldx, goldy, pits, beacons = setup_maze(maze, agent, goldx, goldy, pit_coordinates, beacon_coordinates)
    intelligence = int(input("Enter the intelligence of your agent (0-2): "))
    if intelligence < 0 or intelligence > 2:
        raise ValueError("Please input a number between [0-2]")
    failures = 0
    #Display the initial maze
    print("----------INITIAL MAZE----------")
    display_maze(fmaze, agent, failures = 0)
    print("--------------------------------")
    while True:
        fmaze[agent.row][agent.col] = "-"
        is_stuck = agent.forward(fmaze, cells, intelligence) #this will return if the agent is stuck
        display_maze(fmaze, agent, failures)
        
        agent.total_movements.append(agent.movements)
        agent.total_rotations.append(agent.rotations)
        
        if(agent.row == goldx) and (agent.col == goldy):
            print("Gold found!")
            print("Total Movements: " + str(len(agent.total_movements)))
            break
        elif [agent.row, agent.col] in pit_coordinates or is_stuck:
            failures += 1
            agent.pits.append([agent.row, agent.col])
            print("Search failed")
            print("**********************************************************")
            agent = Agent(row = 0, col = 0, movements = 0, rotations = 0, scans = 0)
            maze = init_maze(cells)
            fmaze, goldx, goldy, pit_coordinates, beacon_coordinates = setup_maze(maze, agent, goldx, goldy, pit_coordinates, beacon_coordinates)
            display_maze(maze, agent, failures) 
