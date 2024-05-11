# Import libaray for Game 
import pygame as p
import chessEngine 
# -----------------------------------------------------------------------
# ----------------------------start code---------------------------------


# -----------------------------------------------------------------------
# importintat var for game like size and Images
WIDTH = HEIGHT = 512 
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}
# -----------------------------------------------------------------------

# -----------------------------------------------------------------------
# this function to load and render image of pieces and set in dictionre
def loadImages():
     pieces = ["wp","wR","wN","wB","wQ","wK","bp","bR","bN","bB","bQ","bK"]
     for piece in pieces :
         IMAGES[piece] = p.image.load("images/"+piece+".png")
# -----------------------------------------------------------------------

# -----------------------------------------------------------------------
#  this game for draw the border and pieces
def drawGameState(screen , gs):
    drawBoard(screen)
    drawPieces(screen,gs.board)
# -----------------------------------------------------------------------

# -----------------------------------------------------------------------
# this to draw border and color squre
def drawBoard(screen):
    colors = [p.Color("white"), p.Color("dark gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c) % 2)]
            p.draw.rect(screen , color , p.Rect(c*SQ_SIZE , r*SQ_SIZE , SQ_SIZE , SQ_SIZE))
# -----------------------------------------------------------------------

# -----------------------------------------------------------------------
# this function to draw pices and set in place use borad in chessEngine
def drawPieces(screen , board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece],p.Rect(c*SQ_SIZE , r*SQ_SIZE , SQ_SIZE , SQ_SIZE))
# -----------------------------------------------------------------------
# -----------------------------------------------------------------------
# this main function to aggragtion all function and fire
def main():
    p.init()
    screen = p.display.set_mode((WIDTH,HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = chessEngine.GameState()
    loadImages()
    # this var for game
    running = True
    sqSelected = () # to save any cell user click
    playerClicks = [] # this list to save start click and end click
    validMoves = gs.getAllPossibleMoves()
    moveMade = False
    
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() # this will return type tuble have (x,y)
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if sqSelected == (row , col):
                    sqSelected = ()
                    playerClicks = []
                else:
                    sqSelected = (row , col)
                    playerClicks.append(sqSelected)
                #this edit to fix in code do not return -Cell 
                if len(playerClicks) == 2 :
                    move = chessEngine.Move(playerClicks[0],playerClicks[1],gs.board)
                    if move.pieceMoved != "--":
                        if move in validMoves :
                            print(move.getChessNotation())
                            gs.makeMove(move)
                            sqSelected = ()
                            playerClicks =[]
                            moveMade = True
                        else:
                            sqSelected      = ()
                            playerClicks    = []
                            moveMade        = False
                    else:
                        sqSelected      = ()
                        playerClicks    = []
                        moveMade        = False
                        
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove()
                    moveMade = True
                    
        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False
                  
        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()
# -----------------------------------------------------------------------
# -----------------------------------------------------------------------
# -----------------------------------------------------------------------
#  this to cheack if main in function to call
if __name__ == "__main__":
    main()
# -----------------------------------------------------------------------
# -----------------------------------------------------------------------
