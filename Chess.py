import pygame, sys, math, random
from scripts.UltraColor import *

print("Beginning of program")

AI = ''
playerColor = ''
AIColor = ''

while(AI is not 'y' and AI is not 'n'):
    AI = input("Would you like to play against the computer?(y/n)")

if (AI is 'y'):
    while(playerColor is not 'B' and playerColor is not 'W'):
        playerColor = input("Would you like to be black or white?(B/W)")
    if (playerColor is 'B'):
        AIColor = 'W'
    else:
        AIColor = 'B'

pygame.init()
print("pygame was initialized")

#   Font used for SelectedPiece and player turn
wordFont = pygame.font.Font("Verdana.ttf",20)

#   Function used for creating the window
#   Makes 4 global variables
def createWindow():
    global window, windowHeight, windowWidth, windowTitle
    windowWidth, windowHeight = 800, 600
    windowTitle = "Pygame 'Silent' Chess"
    pygame.display.set_caption(windowTitle)
    window = pygame.display.set_mode((windowWidth,windowHeight),pygame.HWSURFACE | pygame.DOUBLEBUF)

#   Piece that depicts either Pawn, Queen, King, Bishop, Rook
#   Contains the coordinates, type, color, and surface (or image)
class Piece:
    def __init__(self, surface, moveType, sideColor, xCoordPix = None, yCoordPix = None):
        self.xCoordPix = xCoordPix
        self.yCoordPix = yCoordPix
        self.surface = surface
        self.moveType = moveType
        self.sideColor = sideColor
        self.rect = None


#   Square class that makes up the chessboard. Allows for easier implementation of
#   chess rules (since it uses a 2d array).
class Square:
    def __init__(self, size, color, index, xCoord, yCoord):
        self.sideSize = size
        self.color = color
        self.index = index
        self.shape = None
        self.piece = None
        self.occupied = False
        self.xCoord = xCoord
        self.yCoord = yCoord

    def setShape(self, newShape):
        self.shape = newShape

    def setPiece(self, newPiece):
        self.piece = newPiece

#   This text is shown on the top-right. Shows who's turn it is
def showTurn(turn):
    if turn == 'W':
        turnOverlay = wordFont.render(("It is White's turn."),True, Color.Goldenrod)
    else:
        turnOverlay = wordFont.render(("It is Black's turn."),True, Color.Goldenrod)
    window.blit(turnOverlay, (600,0))

#   This text is shown on the top-left. Shows selected piece
def showCurrentPiece(piece):
    pieceOverlay = None
    if(piece == None):
        pieceOverlay = wordFont.render(("       "),True, Color.Goldenrod)
        window.blit(pieceOverlay, (0,0))
        return
    if(piece.moveType == 'k'):
        pieceOverlay = wordFont.render(("King"),True, Color.Goldenrod)
    if(piece.moveType == 'q'):
        pieceOverlay = wordFont.render(("Queen"),True, Color.Goldenrod)
    if(piece.moveType == 'p'):
        pieceOverlay = wordFont.render(("Pawn"),True, Color.Goldenrod)
    if(piece.moveType == 'b'):
        pieceOverlay = wordFont.render(("Bishop"),True, Color.Goldenrod)
    if(piece.moveType == 'r'):
        pieceOverlay = wordFont.render(("Rook"),True, Color.Goldenrod)
    window.blit(pieceOverlay, (0,0))


boardWidth = 6
boardHeight = 6


chessBoard = []     #Chessboard constructed as a 2D array
indexing = 0        #Indexing for debugging purposes
sizePix = 64        #The size in pixels of each square in the chessboard
coloring = Color.MidnightBlue       #Color of the starting square

#   Making of the board outside the window
for i in range(boardHeight):
    chessBoard.append([])
    for j in range(boardWidth):
        chessBoard[i].append(Square(sizePix, coloring, indexing, j, i))
        indexing += 1
        if (coloring == Color.MidnightBlue):
            coloring = Color.IndianRed
        else:
            coloring = Color.MidnightBlue
            
    if (coloring == Color.MidnightBlue):
        coloring = Color.IndianRed
    else:
        coloring = Color.MidnightBlue
        
#   Checking the board in python window
for i in chessBoard:
    for j in i:
        print(j.sideSize, j.color, j.index)
        print(j.xCoord, " ", j.yCoord)

#   Used to end main game loop when finished playing
isRunning = True

#   Creates main window
createWindow()
print("Window has been created")

#   Variables that position the board
width = (windowWidth / sizePix) / 4 
height = (windowHeight / sizePix) / 5

#   Set the shape of each sqare as a pygame surface Rect
for i in chessBoard:
    for j in i:
        j.setShape(pygame.Rect(j.sideSize * width, j.sideSize * height, j.sideSize, j.sideSize))
        width += 1
    height += 1
    width = (windowWidth / sizePix) / 4

print("Shapes have been set in Squares")


#   Render Background
window.fill(Color.Green)

#   First time board rendering
def drawBoard(widthTemp,heightTemp):
    width = widthTemp
    height = heightTemp
    for i in chessBoard:
        for j in i:
            pygame.draw.rect(window, j.color, j.shape)
            if (j.piece is not None):
                #print("here is a piece: ", j.piece.moveType)
                j.piece.rect = window.blit(j.piece.surface, (width * j.sideSize, height * j.sideSize))
            width += 1
        height += 1
        width = widthTemp

#   Create(and returns) all possible move sets with the given piece
def moveSets(pieces):
    possibleMov = []
    if(pieces.moveType == 'p'):
        #   Pawn Movement
        if(pieces.sideColor == 'B'):
            print("you selected a black pawn")
            if(pieces.yCoordPix + 1 < 6 and chessBoard[pieces.yCoordPix + 1][pieces.xCoordPix].occupied is False):
                possibleMov.append(chessBoard[pieces.yCoordPix + 1][pieces.xCoordPix])
                
            if(pieces.yCoordPix + 1 < 6 and pieces.xCoordPix +1 < 6 and chessBoard[pieces.yCoordPix + 1][pieces.xCoordPix + 1].occupied is True and
               chessBoard[pieces.yCoordPix + 1][pieces.xCoordPix + 1].piece.sideColor == 'W'):
                possibleMov.append(chessBoard[pieces.yCoordPix + 1][pieces.xCoordPix + 1])
                
            if(pieces.yCoordPix + 1 < 6 and pieces.xCoordPix - 1 >= 0 and chessBoard[pieces.yCoordPix + 1][pieces.xCoordPix - 1].occupied is True and
               chessBoard[pieces.yCoordPix + 1][pieces.xCoordPix - 1].piece.sideColor == 'W'):
                possibleMov.append(chessBoard[pieces.yCoordPix + 1][pieces.xCoordPix - 1])
                
        if(pieces.sideColor == 'W'):
            print("you selected a white pawn")
            if(pieces.yCoordPix -1 >= 0 and chessBoard[pieces.yCoordPix - 1][pieces.xCoordPix].occupied is False):
                possibleMov.append(chessBoard[pieces.yCoordPix - 1][pieces.xCoordPix])
                
            if(pieces.yCoordPix - 1 >= 0 and pieces.xCoordPix - 1 >= 0 and chessBoard[pieces.yCoordPix - 1][pieces.xCoordPix - 1].occupied is True and
               chessBoard[pieces.yCoordPix - 1][pieces.xCoordPix - 1].piece.sideColor == 'B'):
                possibleMov.append(chessBoard[pieces.yCoordPix - 1][pieces.xCoordPix - 1])
                
            if(pieces.yCoordPix - 1 >= 0 and pieces.xCoordPix +1 < 6 and chessBoard[pieces.yCoordPix - 1][pieces.xCoordPix + 1].occupied is True and
               chessBoard[pieces.yCoordPix - 1][pieces.xCoordPix + 1].piece.sideColor == 'B'):
                possibleMov.append(chessBoard[pieces.yCoordPix - 1][pieces.xCoordPix + 1])
                
    if(pieces.moveType == 'b'):
        #   Bishop Movement
        for i in range(1,7):#   Down-right check
            if(pieces.yCoordPix + i >= 6 or pieces.xCoordPix + i >= 6):
                break
            elif(chessBoard[pieces.yCoordPix + i][pieces.xCoordPix + i].occupied is False or (chessBoard[pieces.yCoordPix + i][pieces.xCoordPix + i].occupied is True and
                                chessBoard[pieces.yCoordPix + i][pieces.xCoordPix + i].piece.sideColor is not pieces.sideColor)):#      If empty or enemy square
                 possibleMov.append(chessBoard[pieces.yCoordPix + i][pieces.xCoordPix + i])
                 if(chessBoard[pieces.yCoordPix + i][pieces.xCoordPix + i].occupied is True):#      Stop if enemy square after adding
                     break
            else:#      If ally square
                break

        for i in range(1,7):#   Down-left check
            if(pieces.yCoordPix + i >= 6 or pieces.xCoordPix - i < 0):
                break
            elif(chessBoard[pieces.yCoordPix + i][pieces.xCoordPix - i].occupied is False or (chessBoard[pieces.yCoordPix + i][pieces.xCoordPix - i].occupied is True and
                                chessBoard[pieces.yCoordPix + i][pieces.xCoordPix - i].piece.sideColor is not pieces.sideColor)):#      If empty or enemy square
                 possibleMov.append(chessBoard[pieces.yCoordPix + i][pieces.xCoordPix - i])
                 if(chessBoard[pieces.yCoordPix + i][pieces.xCoordPix - i].occupied is True):#      Stop if enemy square after adding
                     break
            else:#      If ally square
                break

        for i in range(1,7):#   Upper-left check
            if(pieces.yCoordPix - i < 0 or pieces.xCoordPix - i < 0):
                break
            elif(chessBoard[pieces.yCoordPix - i][pieces.xCoordPix - i].occupied is False or (chessBoard[pieces.yCoordPix - i][pieces.xCoordPix - i].occupied is True and
                                chessBoard[pieces.yCoordPix - i][pieces.xCoordPix - i].piece.sideColor is not pieces.sideColor)):#      If empty or enemy square
                 possibleMov.append(chessBoard[pieces.yCoordPix - i][pieces.xCoordPix - i])
                 if(chessBoard[pieces.yCoordPix - i][pieces.xCoordPix - i].occupied is True):#      Stop if enemy square after adding
                     break
            else:#      If ally square
                break

        for i in range(1,7):#   Upper-right check
            if(pieces.yCoordPix - i < 0 or pieces.xCoordPix + i >= 6):
                break
            elif(chessBoard[pieces.yCoordPix - i][pieces.xCoordPix + i].occupied is False or (chessBoard[pieces.yCoordPix - i][pieces.xCoordPix + i].occupied is True and
                                chessBoard[pieces.yCoordPix - i][pieces.xCoordPix + i].piece.sideColor is not pieces.sideColor)):#      If empty or enemy square
                 possibleMov.append(chessBoard[pieces.yCoordPix - i][pieces.xCoordPix + i])
                 if(chessBoard[pieces.yCoordPix - i][pieces.xCoordPix + i].occupied is True):#      Stop if enemy square after adding
                     break
            else:#      If ally square
                break
            
    if(pieces.moveType == 'r'):
        #   Rook Movement
        for i in range(1,7):#   Downward check
            if(pieces.yCoordPix + i >= 6):#     Out of bounds
                break
            elif(chessBoard[pieces.yCoordPix + i][pieces.xCoordPix].occupied is False or (chessBoard[pieces.yCoordPix + i][pieces.xCoordPix].occupied is True and
                                chessBoard[pieces.yCoordPix + i][pieces.xCoordPix].piece.sideColor is not pieces.sideColor)):#      If empty or enemy square
                 possibleMov.append(chessBoard[pieces.yCoordPix + i][pieces.xCoordPix])
                 if(chessBoard[pieces.yCoordPix + i][pieces.xCoordPix].occupied is True):#      Stop if enemy square after adding
                     break
            else:#      If ally square
                break

        for i in range(1,7):#   Upward check
            if(pieces.yCoordPix - i < 0):#     Out of bounds
                break
            elif(chessBoard[pieces.yCoordPix - i][pieces.xCoordPix].occupied is False or (chessBoard[pieces.yCoordPix - i][pieces.xCoordPix].occupied is True and
                                chessBoard[pieces.yCoordPix - i][pieces.xCoordPix].piece.sideColor is not pieces.sideColor)):#      If empty or enemy square
                 possibleMov.append(chessBoard[pieces.yCoordPix - i][pieces.xCoordPix])
                 if(chessBoard[pieces.yCoordPix - i][pieces.xCoordPix].occupied is True):#      Stop if enemy square after adding
                     break
            else:#      If ally square
                break

        for i in range(1,7):#   Right check
            if(pieces.xCoordPix + i >= 6):#     Out of bounds
                break
            elif(chessBoard[pieces.yCoordPix][pieces.xCoordPix + i].occupied is False or (chessBoard[pieces.yCoordPix][pieces.xCoordPix + i].occupied is True and
                                chessBoard[pieces.yCoordPix][pieces.xCoordPix + i].piece.sideColor is not pieces.sideColor)):#      If empty or enemy square
                 possibleMov.append(chessBoard[pieces.yCoordPix][pieces.xCoordPix + i])
                 if(chessBoard[pieces.yCoordPix][pieces.xCoordPix + i].occupied is True):#      Stop if enemy square after adding
                     break
            else:#      If ally square
                break

        for i in range(1,7):#   Left check
            if(pieces.xCoordPix - i < 0):#     Out of bounds
                break
            elif(chessBoard[pieces.yCoordPix][pieces.xCoordPix - i].occupied is False or (chessBoard[pieces.yCoordPix][pieces.xCoordPix - i].occupied is True and
                                chessBoard[pieces.yCoordPix][pieces.xCoordPix - i].piece.sideColor is not pieces.sideColor)):#      If empty or enemy square
                 possibleMov.append(chessBoard[pieces.yCoordPix][pieces.xCoordPix - i])
                 if(chessBoard[pieces.yCoordPix][pieces.xCoordPix - i].occupied is True):#      Stop if enemy square after adding
                     break
            else:#      If ally square
                break

    if(pieces.moveType == 'q'):
        #   Queen Movement
        #   Copy of rook and bishop combined
        for i in range(1,7):#   Down-right check
            if(pieces.yCoordPix + i >= 6 or pieces.xCoordPix + i >= 6):
                break
            elif(chessBoard[pieces.yCoordPix + i][pieces.xCoordPix + i].occupied is False or (chessBoard[pieces.yCoordPix + i][pieces.xCoordPix + i].occupied is True and
                                chessBoard[pieces.yCoordPix + i][pieces.xCoordPix + i].piece.sideColor is not pieces.sideColor)):#      If empty or enemy square
                 possibleMov.append(chessBoard[pieces.yCoordPix + i][pieces.xCoordPix + i])
                 if(chessBoard[pieces.yCoordPix + i][pieces.xCoordPix + i].occupied is True):#      Stop if enemy square after adding
                     break
            else:#      If ally square
                break

        for i in range(1,7):#   Down-left check
            if(pieces.yCoordPix + i >= 6 or pieces.xCoordPix - i < 0):
                break
            elif(chessBoard[pieces.yCoordPix + i][pieces.xCoordPix - i].occupied is False or (chessBoard[pieces.yCoordPix + i][pieces.xCoordPix - i].occupied is True and
                                chessBoard[pieces.yCoordPix + i][pieces.xCoordPix - i].piece.sideColor is not pieces.sideColor)):#      If empty or enemy square
                 possibleMov.append(chessBoard[pieces.yCoordPix + i][pieces.xCoordPix - i])
                 if(chessBoard[pieces.yCoordPix + i][pieces.xCoordPix - i].occupied is True):#      Stop if enemy square after adding
                     break
            else:#      If ally square
                break

        for i in range(1,7):#   Upper-left check
            if(pieces.yCoordPix - i < 0 or pieces.xCoordPix - i < 0):
                break
            elif(chessBoard[pieces.yCoordPix - i][pieces.xCoordPix - i].occupied is False or (chessBoard[pieces.yCoordPix - i][pieces.xCoordPix - i].occupied is True and
                                chessBoard[pieces.yCoordPix - i][pieces.xCoordPix - i].piece.sideColor is not pieces.sideColor)):#      If empty or enemy square
                 possibleMov.append(chessBoard[pieces.yCoordPix - i][pieces.xCoordPix - i])
                 if(chessBoard[pieces.yCoordPix - i][pieces.xCoordPix - i].occupied is True):#      Stop if enemy square after adding
                     break
            else:#      If ally square
                break

        for i in range(1,7):#   Upper-right check
            if(pieces.yCoordPix - i < 0 or pieces.xCoordPix + i >= 6):
                break
            elif(chessBoard[pieces.yCoordPix - i][pieces.xCoordPix + i].occupied is False or (chessBoard[pieces.yCoordPix - i][pieces.xCoordPix + i].occupied is True and
                                chessBoard[pieces.yCoordPix - i][pieces.xCoordPix + i].piece.sideColor is not pieces.sideColor)):#      If empty or enemy square
                 possibleMov.append(chessBoard[pieces.yCoordPix - i][pieces.xCoordPix + i])
                 if(chessBoard[pieces.yCoordPix - i][pieces.xCoordPix + i].occupied is True):#      Stop if enemy square after adding
                     break
            else:#      If ally square
                break

        for i in range(1,7):#   Downward check
            if(pieces.yCoordPix + i >= 6):#     Out of bounds
                break
            elif(chessBoard[pieces.yCoordPix + i][pieces.xCoordPix].occupied is False or (chessBoard[pieces.yCoordPix + i][pieces.xCoordPix].occupied is True and
                                chessBoard[pieces.yCoordPix + i][pieces.xCoordPix].piece.sideColor is not pieces.sideColor)):#      If empty or enemy square
                 possibleMov.append(chessBoard[pieces.yCoordPix + i][pieces.xCoordPix])
                 if(chessBoard[pieces.yCoordPix + i][pieces.xCoordPix].occupied is True):#      Stop if enemy square after adding
                     break
            else:#      If ally square
                break

        for i in range(1,7):#   Upward check
            if(pieces.yCoordPix - i < 0):#     Out of bounds
                break
            elif(chessBoard[pieces.yCoordPix - i][pieces.xCoordPix].occupied is False or (chessBoard[pieces.yCoordPix - i][pieces.xCoordPix].occupied is True and
                                chessBoard[pieces.yCoordPix - i][pieces.xCoordPix].piece.sideColor is not pieces.sideColor)):#      If empty or enemy square
                 possibleMov.append(chessBoard[pieces.yCoordPix - i][pieces.xCoordPix])
                 if(chessBoard[pieces.yCoordPix - i][pieces.xCoordPix].occupied is True):#      Stop if enemy square after adding
                     break
            else:#      If ally square
                break

        for i in range(1,7):#   Right check
            if(pieces.xCoordPix + i >= 6):#     Out of bounds
                break
            elif(chessBoard[pieces.yCoordPix][pieces.xCoordPix + i].occupied is False or (chessBoard[pieces.yCoordPix][pieces.xCoordPix + i].occupied is True and
                                chessBoard[pieces.yCoordPix][pieces.xCoordPix + i].piece.sideColor is not pieces.sideColor)):#      If empty or enemy square
                 possibleMov.append(chessBoard[pieces.yCoordPix][pieces.xCoordPix + i])
                 if(chessBoard[pieces.yCoordPix][pieces.xCoordPix + i].occupied is True):#      Stop if enemy square after adding
                     break
            else:#      If ally square
                break

        for i in range(1,7):#   Left check
            if(pieces.xCoordPix - i < 0):#     Out of bounds
                break
            elif(chessBoard[pieces.yCoordPix][pieces.xCoordPix - i].occupied is False or (chessBoard[pieces.yCoordPix][pieces.xCoordPix - i].occupied is True and
                                chessBoard[pieces.yCoordPix][pieces.xCoordPix - i].piece.sideColor is not pieces.sideColor)):#      If empty or enemy square
                 possibleMov.append(chessBoard[pieces.yCoordPix][pieces.xCoordPix - i])
                 if(chessBoard[pieces.yCoordPix][pieces.xCoordPix - i].occupied is True):#      Stop if enemy square after adding
                     break
            else:#      If ally square
                break
            
    if(pieces.moveType == 'k'):
        #   King movement
        if(pieces.yCoordPix + 1 < 6 and (chessBoard[pieces.yCoordPix + 1][pieces.xCoordPix].occupied is False or (chessBoard[pieces.yCoordPix + 1][pieces.xCoordPix].occupied is True and
                                chessBoard[pieces.yCoordPix + 1][pieces.xCoordPix].piece.sideColor is not pieces.sideColor))):#     Down move
            possibleMov.append(chessBoard[pieces.yCoordPix + 1][pieces.xCoordPix])

        if(pieces.yCoordPix - 1 >= 0 and (chessBoard[pieces.yCoordPix - 1][pieces.xCoordPix].occupied is False or (chessBoard[pieces.yCoordPix - 1][pieces.xCoordPix].occupied is True and
                                chessBoard[pieces.yCoordPix - 1][pieces.xCoordPix].piece.sideColor is not pieces.sideColor))):#     Up move
            possibleMov.append(chessBoard[pieces.yCoordPix - 1][pieces.xCoordPix])

        if(pieces.xCoordPix + 1 < 6 and (chessBoard[pieces.yCoordPix][pieces.xCoordPix + 1].occupied is False or (chessBoard[pieces.yCoordPix][pieces.xCoordPix + 1].occupied is True and
                                chessBoard[pieces.yCoordPix][pieces.xCoordPix + 1].piece.sideColor is not pieces.sideColor))):#     Right move
            possibleMov.append(chessBoard[pieces.yCoordPix][pieces.xCoordPix + 1])

        if(pieces.xCoordPix - 1 >= 0 and (chessBoard[pieces.yCoordPix][pieces.xCoordPix - 1].occupied is False or (chessBoard[pieces.yCoordPix][pieces.xCoordPix - 1].occupied is True and
                                chessBoard[pieces.yCoordPix][pieces.xCoordPix - 1].piece.sideColor is not pieces.sideColor))):#     Left move
            possibleMov.append(chessBoard[pieces.yCoordPix][pieces.xCoordPix - 1])

        if((pieces.yCoordPix + 1 < 6 and pieces.xCoordPix + 1 < 6) and (chessBoard[pieces.yCoordPix + 1][pieces.xCoordPix + 1].occupied is False or (chessBoard[pieces.yCoordPix + 1][pieces.xCoordPix + 1].occupied is True and
                                chessBoard[pieces.yCoordPix + 1][pieces.xCoordPix + 1].piece.sideColor is not pieces.sideColor))):#     Down-right move
            possibleMov.append(chessBoard[pieces.yCoordPix + 1][pieces.xCoordPix + 1])

        if((pieces.yCoordPix - 1 >= 0 and pieces.xCoordPix - 1 >= 0) and (chessBoard[pieces.yCoordPix - 1][pieces.xCoordPix - 1].occupied is False or (chessBoard[pieces.yCoordPix - 1][pieces.xCoordPix - 1].occupied is True and
                                chessBoard[pieces.yCoordPix - 1][pieces.xCoordPix - 1].piece.sideColor is not pieces.sideColor))):#     Upper-left move
            possibleMov.append(chessBoard[pieces.yCoordPix - 1][pieces.xCoordPix - 1])

        if((pieces.yCoordPix + 1 < 6 and pieces.xCoordPix - 1 >= 0) and (chessBoard[pieces.yCoordPix + 1][pieces.xCoordPix - 1].occupied is False or (chessBoard[pieces.yCoordPix + 1][pieces.xCoordPix - 1].occupied is True and
                                chessBoard[pieces.yCoordPix + 1][pieces.xCoordPix - 1].piece.sideColor is not pieces.sideColor))):#     Down-left move
            possibleMov.append(chessBoard[pieces.yCoordPix + 1][pieces.xCoordPix - 1])

        if((pieces.yCoordPix - 1 >= 0 and pieces.xCoordPix + 1 < 6) and (chessBoard[pieces.yCoordPix - 1][pieces.xCoordPix + 1].occupied is False or (chessBoard[pieces.yCoordPix - 1][pieces.xCoordPix + 1].occupied is True and
                                chessBoard[pieces.yCoordPix - 1][pieces.xCoordPix + 1].piece.sideColor is not pieces.sideColor))):#     Upper-right move
            possibleMov.append(chessBoard[pieces.yCoordPix - 1][pieces.xCoordPix + 1])
            
    return possibleMov
            

print("Begin loading of Images")
#   Load all image neccessary
allImages = [pygame.image.load("images\\KingB.png"),
             pygame.image.load("images\\QueenB.png"),
             pygame.image.load("images\\PawnB.png"),
             pygame.image.load("images\\BishopB.png"),
             pygame.image.load("images\\RookB.png"),
             
             pygame.image.load("images\\KingW.png"),
             pygame.image.load("images\\QueenW.png"),
             pygame.image.load("images\\PawnW.png"),
             pygame.image.load("images\\BishopW.png"),
             pygame.image.load("images\\RookW.png"),]

#   All surface formulated by the size of the images are here
allSurfaces = [pygame.Surface(allImages[0].get_size(), pygame.HWSURFACE | pygame.SRCALPHA),
               pygame.Surface(allImages[1].get_size(), pygame.HWSURFACE | pygame.SRCALPHA),
               pygame.Surface(allImages[2].get_size(), pygame.HWSURFACE | pygame.SRCALPHA),
               pygame.Surface(allImages[3].get_size(), pygame.HWSURFACE | pygame.SRCALPHA),
               pygame.Surface(allImages[4].get_size(), pygame.HWSURFACE | pygame.SRCALPHA),
               pygame.Surface(allImages[5].get_size(), pygame.HWSURFACE | pygame.SRCALPHA),
               pygame.Surface(allImages[6].get_size(), pygame.HWSURFACE | pygame.SRCALPHA),
               pygame.Surface(allImages[7].get_size(), pygame.HWSURFACE | pygame.SRCALPHA),
               pygame.Surface(allImages[8].get_size(), pygame.HWSURFACE | pygame.SRCALPHA),
               pygame.Surface(allImages[9].get_size(), pygame.HWSURFACE | pygame.SRCALPHA)]

#   Blit all images to those surfaces
allSurfaces[0].blit(allImages[0],(0,0))
allSurfaces[1].blit(allImages[1],(0,0))
allSurfaces[2].blit(allImages[2],(0,0))
allSurfaces[3].blit(allImages[3],(0,0))
allSurfaces[4].blit(allImages[4],(0,0))
allSurfaces[5].blit(allImages[5],(0,0))
allSurfaces[6].blit(allImages[6],(0,0))
allSurfaces[7].blit(allImages[7],(0,0))
allSurfaces[8].blit(allImages[8],(0,0))
allSurfaces[9].blit(allImages[9],(0,0))


#   This is where all actual pieces will be stored
allPieces = [ Piece(allSurfaces[0],'k','B',2,0),
              Piece(allSurfaces[1],'q','B',3,0),
              Piece(allSurfaces[2],'p','B',0,1),
              Piece(allSurfaces[2],'p','B',1,1),
              Piece(allSurfaces[2],'p','B',2,1),
              Piece(allSurfaces[2],'p','B',3,1),
              Piece(allSurfaces[2],'p','B',4,1),
              Piece(allSurfaces[2],'p','B',5,1),
              Piece(allSurfaces[3],'b','B',1,0),
              Piece(allSurfaces[3],'b','B',4,0),
              Piece(allSurfaces[4],'r','B',0,0),
              Piece(allSurfaces[4],'r','B',5,0),

              Piece(allSurfaces[5],'k','W',3,5),
              Piece(allSurfaces[6],'q','W',2,5),
              Piece(allSurfaces[7],'p','W',0,4),
              Piece(allSurfaces[7],'p','W',1,4),
              Piece(allSurfaces[7],'p','W',2,4),
              Piece(allSurfaces[7],'p','W',3,4),
              Piece(allSurfaces[7],'p','W',4,4),
              Piece(allSurfaces[7],'p','W',5,4),
              Piece(allSurfaces[8],'b','W',1,5),
              Piece(allSurfaces[8],'b','W',4,5),
              Piece(allSurfaces[9],'r','W',0,5),
              Piece(allSurfaces[9],'r','W',5,5)]

#   Movement function, returns a piece if one is captured
#   Uses the piece and destination as input. The piece returned is
#   added to the captured list and removed from the allPieces list
def moveTo(pieceA, dest):
    if(pieceA.moveType is 'p'):
        if(pieceA.sideColor is 'W'):
            #   Promotion of white pawns
            if(dest.yCoord == 0):
                pieceA.moveType = 'q'
                pieceA.surface = allSurfaces[6]
        if(pieceA.sideColor is 'B'):
            #   Promotion of black pawns
            if(dest.yCoord == 5):
                pieceA.moveType = 'q'
                pieceA.surface = allSurfaces[1]

    
    if(dest.piece == None):
        dest.piece = pieceA
        chessBoard[pieceA.yCoordPix][pieceA.xCoordPix].piece = None
        chessBoard[pieceA.yCoordPix][pieceA.xCoordPix].occupied = False
        pieceA.xCoordPix = dest.xCoord
        pieceA.yCoordPix = dest.yCoord
        dest.occupied = True
        return None
    else:
        temp = dest.piece
        dest.piece = pieceA
        chessBoard[pieceA.yCoordPix][pieceA.xCoordPix].piece = None
        chessBoard[pieceA.yCoordPix][pieceA.xCoordPix].occupied = False
        pieceA.xCoordPix = dest.xCoord
        pieceA.yCoordPix = dest.yCoord
        dest.occupied = True
        return temp


for i in range(len(chessBoard)):
    for j in range(len(chessBoard[i])):
        for piece in allPieces:
            if (piece.xCoordPix == j and piece.yCoordPix == i):
                chessBoard[i][j].setPiece(piece)
                chessBoard[i][j].occupied = True
                

mousePos = 0
mouseX, mouseY = 0,0
highlighter = pygame.Surface((sizePix,sizePix), pygame.HWSURFACE | pygame.SRCALPHA)
highlighter.fill(Color.WithAlpha(100, Color.Silver))
movementLighter = pygame.Surface((sizePix,sizePix), pygame.HWSURFACE | pygame.SRCALPHA)
movementLighter.fill(Color.WithAlpha(100, Color.Green))

moveSpaces = []
captured = []

selector = None     #   Selecting pieces

currentTurn = 'W'

def winConditions():
    #   Check for win conditions!
    for piece in captured:
        if(piece.moveType is 'k'):
            print("The game has ended")
            if(piece.sideColor is 'W'):
                print("The winner is Black!")
            else:
                print("The winner is White!")
            return False
    return True

#   Here is the main game loop                                      
while isRunning:
    #print(isRunning)#debug purposes
    width = (windowWidth / sizePix) / 4 
    height = (windowHeight / sizePix) / 5
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        if event.type == pygame.MOUSEMOTION:
            #   Creates a higlighter which follows the panels the mouse is on
            mousePos = pygame.mouse.get_pos()
            mouseX = math.floor(mousePos[0] / sizePix) * sizePix + 8
            mouseY = math.floor(mousePos[1] / sizePix) * sizePix - 8
        if event.type == pygame.MOUSEBUTTONDOWN:
            #   If selecting a piece the move sets will be shown and highlighted
            #   If clicking on a move set the move will take place
            mousePos = pygame.mouse.get_pos()
            capturing = False
            for moves in moveSpaces:
                if(moves.shape.collidepoint(mousePos)):
                    capture = moveTo(selector,moves)
                    if(capture is not None):
                        captured.append(capture)
                        allPieces.remove(capture)
                    selector = None
                    moveSpaces = []
                    capturing = True
                    if(currentTurn == 'W'):
                        currentTurn = 'B'
                    else:
                        currentTurn = 'W'
                    break
            if(capturing is False):
                for piece in allPieces:
                    if(piece.rect.collidepoint(mousePos)):
                        #print("Collision!!!")
                        if(piece.sideColor is not currentTurn):
                            print("It is not your turn!")
                            break
                        selector = piece
                        moveSpaces = moveSets(selector)[:]
                        break
                    else:
                        selector = None
                        moveSpaces = []                   
                
    #   Here is the game loop (each frame)

    #   AI procedures. All randomized
    if (AI is 'y' and AIColor is currentTurn and winConditions()):
        selector = random.choice(allPieces)
        while(len(moveSpaces) is 0 or selector.sideColor is not AIColor):
            selector = random.choice(allPieces)
            moveSpaces = moveSets(selector)[:]
        capture = moveTo(selector, random.choice(moveSpaces))
        if(capture is not None):
            captured.append(capture)
            allPieces.remove(capture)
        selector = None
        moveSpaces = []
        if(currentTurn == 'W'):
            currentTurn = 'B'
        else:
            currentTurn = 'W'
        

    #   DrawBackGround
    window.fill(Color.Green)

    #   DrawBoard
    drawBoard(width,height)


    #   Draw the highlighter if inside board
    if mouseX >= width * sizePix and mouseX <= (width + 5) * sizePix and mouseY >= height * sizePix and mouseY <= (height + 5) * sizePix:
        window.blit(highlighter, (mouseX, mouseY))

    #   Draw highlighted move sets
    for moves in moveSpaces:
        window.blit(movementLighter, ((width + moves.xCoord) * moves.sideSize, (height + moves.yCoord) * moves.sideSize))

    #   Draw current turn and selected piece
    showTurn(currentTurn)
    showCurrentPiece(selector)

    #   Check for win conditions!
    isRunning = winConditions()
        
    
    #   Update the display
    pygame.display.update()


    
pygame.quit()
print("End of program")

sys.exit()


#End
