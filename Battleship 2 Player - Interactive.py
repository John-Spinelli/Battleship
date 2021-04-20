'''
Battleship 2 Player.py

This game will allow 2 players to play Battleship.
This version will be interactive, allowing users to click and select
their locations rather than typing in coordinates.
See Battleship Interactive Documentation for list of functions
and logistics
'''

# CV Constants & Init
import cv2 as cv
import numpy as np

S_WIDTH = 800
S_HEIGHT = 800
cv.namedWindow("Battleship")
background = (251, 221, 66)
screen = np.zeros([S_WIDTH,S_HEIGHT,3], np.uint8)
screen = cv.rectangle(screen, (0,0), (S_HEIGHT, S_WIDTH), background, -1)

# Create Grid
screen = cv.rectangle(screen, (100,100), (S_WIDTH-50, S_HEIGHT-100), (10,10,10), 10)
screen = cv.imshow("Battleship",screen)


# Battleship Constants
WIDTH = 8
HEIGHT = 8
SHIP = chr(9632)
HIT = 'X'
MISS = 'O'

# ///////////////////////////
class Player:

    def __init__(self, pnum):
        # Generate and fill board for the player
        self.name = "Player " + str(pnum)
        self.grid = GenerateGrid()
        DisplayGrid(self.grid)
        print("Hello,", self.name + ". It is your turn to place your ships.")
        # Place each ship
        self.c4 = PlaceShips(4,self.grid)
        self.c3 = PlaceShips(3,self.grid)
        self.c2 = PlaceShips(2,self.grid)
        self.ships = 3
        input("Press enter to continue.")
        cls()

    def hitormiss(self, row, col):
        # Determine if player's ship was hit/sank. Return false if coord already
        # attacked by player, true if new coord
        try:
            if self.grid[row][col] == HIT or self.grid[row][col] == MISS:
                print("You have already attacked this coordinate.")
                return False
            self.grid[row][col] = HIT
            # If new coord:
            # coord belongs to 4 long ship
            if [row,col] in self.c4:
                self.c4.remove([row,col])
                print("Hit")
                if len(self.c4) == 0:
                    print("You sank " + self.name + "'s 4 long ship!")
                    self.ships-=1
            # 3 long ship        
            elif [row,col] in self.c3:
                self.c3.remove([row,col])
                print("Hit")
                if len(self.c3) == 0:
                    print("You sank " + self.name + "'s 3 long ship!")
                    self.ships-=1
            # 4 long ship
            elif [row,col] in self.c2:
                self.c2.remove([row,col])
                print("Hit")
                if len(self.c2) == 0:
                    print("You sank " + self.name + "'s 2 long ship!")
                    self.ships-=1
            # Empty coord
            else:
                print("Miss")
                self.grid[row][col] = MISS
            return True
        except:
            print("Something went wrong")
            
# //////////////////////////////

def cls():
    # Used to "clear" the screen, hiding placement of ships from the other user.
    print ("\n" * 40)

def DisplayGrid(grid, mask = False):
    # Displays the grid in clean format. If mask == True, display ' ' instead of ship character
    print('\n\\', end='  ')
    for i in range(WIDTH):
        print(i, end='  ')
    print()
    if mask:
        # Hide ships from other player
        for i in range(HEIGHT):
            print(i, end=' ')
            for element in grid[i]:
                if element == SHIP:
                    print('[ ]', end='')
                else:
                    print('['+element+']', end='')
            print()
    else:
        # Placing ships, reveal the board
        for i in range(HEIGHT):
            print(i, end=' ')
            for element in grid[i]:
                print('['+element+']', end='')
            print()
    print()

def GenerateGrid():
    # Produce empty grid, returns grid
    grid = []
    for i in range(WIDTH):
        row = []
        for j in range(HEIGHT):
            row.append(' ')
        grid.append(row)
    return grid

def PossibleCoord(row, col, grid, shipsize):
    # Assuming valid row/col position, checks if there are possible orientations
    L = col > (shipsize-2)
    if L:
        for i in range(1,shipsize):
            if grid[row][col-i] == SHIP:
                L = False
                break    
    R = col < WIDTH-(shipsize-1)
    if R:
        for i in range(1,shipsize):
            if grid[row][col+i] == SHIP:
                R = False
                break
    U = row > (shipsize-2)
    if U:
        for i in range(1,shipsize):
            if grid[row-i][col] == SHIP:
                U = False
                break
    D = row < HEIGHT-(shipsize-1)
    if D:
        for i in range(1,shipsize):
            if grid[row+i][col] == SHIP:
                D = False
                break
    return L, R, U, D
    

def PlaceShips(shipsize, grid):
    # Allows player to place ship of length shipsize onto board. Prompts player to input coordinate and
    # direction of their ship. If valid, places ship.
    row = -1
    col = -1
    left,right,up,down = 0,0,0,0
    
    # Prompt user for coordinate until valid coordinate given
    while True:
        try:
            print("Select the coordinate that you would like the end of your", shipsize, "long ship to be in.")
            row = int(input("Enter the row #: "))
            col = int(input("Enter the col #: "))
            # Coordinate within board
            if (row >= 0 and row <= HEIGHT-1) and (col >= 0 and col <= WIDTH-1) and grid[row][col] != SHIP:
                # Ship has at least one possible configuration 
                left, right, up, down = PossibleCoord(row,col,grid,shipsize)
                # No possible configuration
                if not(left or right or up or down):
                    print("Ship of this size cannot exist in this coordinate.\n")
                # Possible configuration
                else:
                    print("Valid coordinate selected")
                    break
            else:
                print("Invalid coordinate\n")
        # Input type invalid
        except:
            print("Invalid input, must be an integer.\n")

    # print orientation options to user
    print("Select the orientation of the ship.")
    if left:
        print("1. [",row,',',col-(shipsize-1),"] - [",row,',',col,"], left")
    if right:
        print("2. [",row,',',col,"] - [",row,',',col+(shipsize-1),"], right")
    if up:
        print("3. [",row-(shipsize-1),',',col,"] - [",row,',',col,"], up")
    if down:
        print("4. [",row,',',col,"] - [",row+(shipsize-1),',',col,"], down")

    shipcoords = []
    selection = " "
    # Prompt user for direction of ship
    while True:
        try:
            selection = int(input("Enter value matching orientation: "))
            if selection == 1 and left:
                for i in range(shipsize):
                    grid[row][col-i] = SHIP
                    shipcoords.append([row,col-i])
                break
            elif selection == 2 and right:
                for i in range(shipsize):
                    grid[row][col+i] = SHIP
                    shipcoords.append([row,col+i])
                break                    
            elif selection == 3 and up:
                for i in range(shipsize):
                    grid[row-i][col] = SHIP
                    shipcoords.append([row-i,col])
                break
            elif selection == 4 and down:
                for i in range(shipsize):
                    grid[row+i][col] = SHIP
                    shipcoords.append([row+i,col])
                break
            else:
                print("Invalid selection")
           
        # Input type invalid
        except:
            print("Invalid input, must be an integer.\n")
            
    print("Ship placed successfully.")
    DisplayGrid(grid)
    return shipcoords

def SimBattle(attacker, defender):
    # Asks attacker for coordinates to attack, attacks the coordinate.
    DisplayGrid(defender.grid, True)
    while True:
        try:
            print(attacker.name + ', select coordinate to attack.')
            row = int(input("Enter the row #: "))
            col = int(input("Enter the col #: "))
            # Coordinate within board
            if (row >= 0 and row <= HEIGHT-1) and (col >= 0 and col <= WIDTH-1):
                # New coord?
                if defender.hitormiss(row,col):
                    DisplayGrid(defender.grid, True)
                    if defender.ships == 0:
                        print(attacker.name, "wins!\nGame Over")
                        return True
                    input("Press enter to continue.")
                    cls()
                    break
                    
            else:
                print("Coordinate out of bounds")
        # Input type invalid
        except:
            print("Invalid input, must be an integer.\n")
    
    else:
        return False


def main():

    # Create Players
    p1 = Player(1)
    p2 = Player(2)

    # Alternate turns until one player has no more ships
    turn = 0
    while True:
        if turn == 0:
            cont = SimBattle(p1,p2)
        else:
            cont = SimBattle(p2,p1)
        if cont:
            break
        turn = (turn+1)%2
        
#main()


