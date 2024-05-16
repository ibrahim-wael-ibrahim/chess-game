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
animate = True
MOVE_LOG_PANEL_WIDTH = 250
MOVE_LOG_PANEL_HEIGHT = HEIGHT

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
def drawGameState(screen , gs , valid_moves , square_selected):
    drawBoard(screen)
    highlightSquares(screen, gs, valid_moves, square_selected)
    drawPieces(screen,gs.board)
# -----------------------------------------------------------------------
def drawMoveLog(screen, gs, font):
    move_log_rect = p.Rect(WIDTH, 0, MOVE_LOG_PANEL_WIDTH, MOVE_LOG_PANEL_HEIGHT)
    p.draw.rect(screen, p.Color('black'), move_log_rect)
    move_log = gs.move_log
    move_texts = []
    for i in range(0, len(move_log), 2):
        move_string = str(i // 2 + 1) + '. ' + str(move_log[i]) + " "
        if i + 1 < len(move_log):
            move_string += str(move_log[i + 1]) + "  "
        move_texts.append(move_string)

    moves_per_row = 3
    padding = 5
    line_spacing = 2
    text_y = padding
    for i in range(0, len(move_texts), moves_per_row):
        text = ""
        for j in range(moves_per_row):
            if i + j < len(move_texts):
                text += move_texts[i + j]

        text_object = font.render(text, True, p.Color('white'))
        text_location = move_log_rect.move(padding, text_y)
        screen.blit(text_object, text_location)
        text_y += text_object.get_height() + line_spacing


def drawEndGameText(screen, text):
    font = p.font.SysFont("Helvetica", 32, True, False)
    text_object = font.render(text, False, p.Color("gray"))
    text_location = p.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH / 2 - text_object.get_width() / 2,
                                                                 HEIGHT / 2 - text_object.get_height() / 2)
    screen.blit(text_object, text_location)
    text_object = font.render(text, False, p.Color('black'))
    screen.blit(text_object, text_location.move(2, 2))
# -----------------------------------------------------------------------
# this to draw border and color squre
def drawBoard(screen):
    global colors
    colors = [p.Color("white"), p.Color("gray")]
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            color = colors[((row + column) % 2)]
            p.draw.rect(screen, color, p.Rect(column * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))

# -----------------------------------------------------------------------
def highlightSquares(screen, gs, valid_moves, square_selected):

    if (len(gs.move_log)) > 0:
        last_move = gs.move_log[-1]
        s = p.Surface((SQ_SIZE, SQ_SIZE))
        s.set_alpha(100)
        s.fill(p.Color('green'))
        screen.blit(s, (last_move.end_col * SQ_SIZE, last_move.end_row * SQ_SIZE))
    if square_selected != ():
        row, col = square_selected
        if gs.board[row][col][0] == ('w' if gs.white_to_move else 'b'):  
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)  
            s.fill(p.Color('blue'))
            screen.blit(s, (col * SQ_SIZE, row * SQ_SIZE))
            s.fill(p.Color('yellow'))
            for move in valid_moves:
                if move.start_row == row and move.start_col == col:
                    screen.blit(s, (move.end_col * SQ_SIZE, move.end_row * SQ_SIZE))
# -----------------------------------------------------------------------
# this function to draw pices and set in place use borad in chessEngine
def drawPieces(screen , board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece],p.Rect(c*SQ_SIZE , r*SQ_SIZE , SQ_SIZE , SQ_SIZE))
# -----------------------------------------------------------------------
def animateMove(move, screen, board, clock):
    """
    Animating a move
    """
    global colors
    d_row = move.end_row - move.start_row
    d_col = move.end_col - move.start_col
    frames_per_square = 10  # frames to move one square
    frame_count = (abs(d_row) + abs(d_col)) * frames_per_square
    for frame in range(frame_count + 1):
        row, col = (move.start_row + d_row * frame / frame_count, move.start_col + d_col * frame / frame_count)
        drawBoard(screen)
        drawPieces(screen, board)
        # erase the piece moved from its ending square
        color = colors[(move.end_row + move.end_col) % 2]
        end_square = p.Rect(move.end_col * SQ_SIZE, move.end_row * SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, end_square)
        # draw captured piece onto rectangle
        if move.piece_captured != '--':
            if move.is_enpassant_move:
                enpassant_row = move.end_row + 1 if move.piece_captured[0] == 'b' else move.end_row - 1
                end_square = p.Rect(move.end_col * SQ_SIZE, enpassant_row * SQ_SIZE, SQ_SIZE, SQ_SIZE)
            screen.blit(IMAGES[move.piece_captured], end_square)
        # draw moving piece
        screen.blit(IMAGES[move.piece_moved], p.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(60)
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
    game_over = False
    running = True
    sqSelected = () # to save any cell user click
    playerClicks = [] # this list to save start click and end click
    validMoves = gs.getAllPossibleMoves()
    moveMade = False
    move_undone = False
    move_finder_process = None
    move_log_font = p.font.SysFont("Arial", 14, False, False)
    player_one = True  # if a human is playing white, then this will be True, else False
    player_two = False  # if a hyman is playing white, then this will be True, else False

    
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
                    if move.piece_moved != "--":
                        for i in range(len(validMoves)):
                            if move == validMoves[i] :
                                print(move.getChessNotation())
                                gs.makeMove(move)
                                sqSelected = ()
                                playerClicks =[]
                                moveMade = True
                            if not moveMade:
                                playerClicks =[sqSelected]

                    else:
                        sqSelected      = ()
                        playerClicks    = []
                        moveMade        = False
                        
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove()
                    moveMade = True
                if e.key == p.K_r:  # reset the game when 'r' is pressed
                    gs = chessEngine.GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    game_over = False
                    
        if moveMade:
            if animate:
                if len(gs.move_log) > 0:
                    animateMove(gs.move_log[-1], screen, gs.board, clock)
            validMoves = gs.getValidMoves()
            moveMade = False
                  
        drawGameState(screen, gs , validMoves , sqSelected)
        if not game_over:
            drawMoveLog(screen, gs, move_log_font)

        if gs.checkmate:
            game_over = True
            if gs.white_to_move:
                drawEndGameText(screen, "Black wins by checkmate")
            else:
                drawEndGameText(screen, "White wins by checkmate")

        elif gs.stalemate:
            game_over = True
            drawEndGameText(screen, "Stalemate")
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
