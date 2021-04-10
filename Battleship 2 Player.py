'''
Battleship 2 Player.py

This game will allow 2 players to play Battleship. The structure of the game will be as follows:

P1 selects coordinates of ships and orientation.
P1 confirms placement
P2 selects coordinates of ships and orientation.
P2 confirms placement

Empty board visible for P1, enter coordinates for missile
If enemy ship in location, HIT
else, MISS

P2's turn, performing same tasks

Repeat process until 1 player has sunk all of opponent's ships.


Things to consider:

Hide other player's moves when not their turn.
Coordinate selections must be int and within the range
Display coordinate grids. O for miss, X for hit, [ ] for no interaction
List for initial placements and list for opponent view? Or just mask when playing?

Produce text file upon game completion, displaying initial configurations of both players,
   final results of both players
OpenCV to allow player to click their selection (once game is functioning, next iteration of game)


\ 0 1 2 3 4
0
1
2

Player class:
__init__ - generates grid and places ship for player
hitormiss - determines if player's ship was hit at coord

.name - player's name
.grid - player's grid
.c4 - coords for 4 long ship
.c3 - coords for 3 long ship
.c2 - coords for 2 long ship

Functions:

cls() - "clears" screen, ready for next player
DisplayGrid() - used in GenerateGrid, shows grid in clean format.
GenerateGrid() - produce empty 2D list of correct dimensions
PossibleCoord() - checks to see if ship has possible orientations for coord
PlaceShips() - take user inputs inside of function, place ships in feasible configuration, return 2D list
Attack() - take coordinates and user's turn, attack the opponents grid
DisplayOppGrid() - displays the opponent's grid, only showing HIT/MISS
'''

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
        self.c4 = PlaceShips(4,self.grid)
        self.c3 = PlaceShips(3,self.grid)
        self.c2 = PlaceShips(2,self.grid)
        self.ships = 3
        input("Press enter to continue.")
        cls()

    def hitormiss(self, row, col):
        # Determine if player's ship was hit/sank. Return false if coord already
        # attacked by player, true if new coord

        if self.grid[row][col] == HIT or self.grid[row][col] == MISS:
            print("You have already attacked this coordinate.")
            return False
        self.grid[row][col] = HIT
        # If new coord
        if [row,col] in self.c4:
            self.c4.remove([row,col])
            print("Hit")
            if len(self.c4) == 0:
                print("You sank " + self.name + "'s 4 long ship!")
                self.ships-=1
                
        elif [row,col] in self.c4:
            self.c4.remove([row,col])
            print("Hit")
            if len(self.c4) == 0:
                print("You sank " + self.name + "'s 4 long ship!")
                self.ships-=1
        elif [row,col] in self.c4:
            self.c4.remove([row,col])
            print("Hit")
            if len(self.c4) == 0:
                print("You sank " + self.name + "'s 4 long ship!")
                self.ships-=1
        # Empty coord
        else:
            print("Miss")
            self.grid[row][col] = MISS
        return True
    
# //////////////////////////////

def cls():
    # Used to "clear" the screen, hiding placement of ships from the other user.
    print ("\n" * 40)

def DisplayGrid(grid, mask = False):
    # Displays the grid in clean format. If mask == True, display ' ' instead of W
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
            if (row >= 0 and row <= HEIGHT-1) and (col >= 0 and col <= WIDTH-1) and grid[row][col] != 'W':
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
            print(left)
            print(selection)
            
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
                    input("Press enter to continue.")
                    cls()
                    break
            else:
                print("Coordinate out of bounds")
        # Input type invalid
        except:
            print("Invalid input, must be an integer.\n")


#Testing



def main():

    # Create Players
    p1 = Player(1)
    p2 = Player(2)

    SimBattle(p1,p2)
    SimBattle(p1,p2)
    SimBattle(p2,p1)
    
main()


