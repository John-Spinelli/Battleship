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

Functions:

DisplayGrid() - used in GenerateGrid, shows grid in clean format.
GenerateGrid() - produce empty 2D list of correct dimensions
PlaceShips() - take user inputs inside of function, place ships in feasible configuration, return 2D list
Attack() - take coordinates and user's turn, attack the opponents grid
DisplayOppGrid() - displays the opponent's grid, only showing HIT/MISS
'''

WIDTH = 8
HEIGHT = 8

def cls():
    # Used to "clear" the screen, hiding placement of ships from the other user.
    print ("\n" * 30)

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
                if element == 'W':
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
    
    L = col > (shipsize-2)
    if L:
        for i in range(1,shipsize):
            if grid[row][col-i] == 'W':
                L = False
                break    
    R = col < WIDTH-(shipsize-1)
    if R:
        for i in range(1,shipsize):
            if grid[row][col+i] == 'W':
                R = False
                break
    U = row > (shipsize-2)
    if U:
        for i in range(1,shipsize):
            if grid[row-i][col] == 'W':
                U = False
                break
    D = row < HEIGHT-(shipsize-1)
    if D:
        for i in range(1,shipsize):
            if grid[row+i][col] == 'W':
                D = False
                break
    return L, R, U, D
    

def PlaceShips(shipsize, grid):
    # Allows player to place ship of length shipsize onto board. Prompts player to input coordinate and
    # direction of their ship. If valid, places ship.
    row = -1
    col = -1
    ####DisplayGrid(grid)
    
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

    
    print("Select the orientation of the ship.")
    if left:
        print("1. [",row,',',col-(shipsize-1),"] - [",row,',',col,"], left")
    if right:
        print("2. [",row,',',col,"] - [",row,',',col+(shipsize-1),"], right")
    if up:
        print("3. [",row-(shipsize-1),',',col,"] - [",row,',',col,"], up")
    if down:
        print("4. [",row,',',col,"] - [",row+(shipsize-1),',',col,"], down")

    shipcoords = [[row,col]]
    # Prompt user for direction of ship
    while True:
        try:
            selection = int(input("Enter value matching orientation: "))
            if selection == 1 and left:
                for i in range(shipsize):
                    grid[row][col-i] = 'W'
                    shipcoords.append([row][col-i])
                break
            elif selection == 2 and right:
                for i in range(shipsize):
                    grid[row][col+i] = 'W'
                    shipcoords.append([row][col+i])
                break                    
            elif selection == 3 and up:
                for i in range(shipsize):
                    grid[row-i][col] = 'W'
                    shipcoords.append([row-i][col])
                break
            elif selection == 4 and down:
                for i in range(shipsize):
                    grid[row+i][col] = 'W'
                    shipcoords.append([row+i][col])
                break
            else:
                print("Invalid selection")
           
        # Input type invalid
        except:
            print("Invalid input, must be an integer.\n")
            
    print("Ship placed successfully.")
    DisplayGrid(grid)
    return shipcoords


#PlaceShips(4)
'''
print("Hello, Player", pnumber, "it is your turn to place your ships.")
print("You have a 4 long, 3 long and 2 long ship to place.")
'''
#Testing

#A = GenerateGrid()

#DisplayGrid(A)

def main():
    # Generate Grids for each player
    P1 = GenerateGrid()
    P2 = GenerateGrid()

    # Place Ships for P1
    print("Hello, Player 1. It is your turn to place your ships.")
    print("You have a 4 long, 3 long and 2 long ship to place.")
    DisplayGrid(P1)
    P1_4 = PlaceShips(4,P1)
    P1_3 = PlaceShips(3,P1)
    P1_2 = PlaceShips(2,P1)
    cls()

    # Place Ships for P2
    print("Hello, Player 2. It is your turn to place your ships.")
    print("You have a 4 long, 3 long and 2 long ship to place.")
    DisplayGrid(P2)
    P2_4 = PlaceShips(4,P2)
    P2_3 = PlaceShips(3,P2)
    P2_2 = PlaceShips(2,P2)
    cls()
                
    
main()


