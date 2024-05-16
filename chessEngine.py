# -----------------------------------------------------------------------
# this some rules for game like place of pieces on border and history moves
class GameState():
    def __init__(self):
        self.board = [
            ["bR","bN","bB","bQ","bK","bB","bN","bR"],
            ["bp","bp","bp","bp","bp","bp","bp","bp"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["wp","wp","wp","wp","wp","wp","wp","wp"],
            ["wR","wN","wB","wQ","wK","wB","wN","wR"]
        ]
        self.moveFunctions = {"p": self.getPawnMoves, "R": self.getRookMoves, "N": self.getKnightMoves,
                              "B": self.getBishopMoves, "Q": self.getQueenMoves, "K": self.getKingMoves}
        self.white_to_move = True
        self.move_log = []
        self.white_king_location = (7, 4)
        self.black_king_location = (0, 4)
        self.checkmate = False
        self.stalemate = False
        self.in_check = False
        self.pins = []
        self.checks = []
        
        self.enpassant_possible = () 
        self.enpassant_possible_log = [self.enpassant_possible]
        
    def makeMove(self,move):
        self.board[move.start_row][move.start_col] = "--"
        self.board[move.end_row][move.end_col]     = move.piece_moved
        self.move_log.append(move)
        self.white_to_move = not self.white_to_move
        if move.piece_moved == "wK":
            self.white_king_location = (move.end_row,move.end_col)
        elif move.piece_moved == "bK":
            self.black_king_location = (move.end_row , move.end_col)
            
        if move.is_pawn_promotion:
            self.board[move.end_row][move.end_col] = move.piece_moved[0] + "Q"
        
        if move.is_enpassant_move:
            self.board[move.start_row][move.end_col] = "--" 

        if move.piece_moved[1] == "p" and abs(move.start_row - move.end_row) == 2: 
            self.enpassant_possible = ((move.start_row + move.end_row) // 2, move.start_col)
        else:
            self.enpassant_possible = ()
            
        self.enpassant_possible_log.append(self.enpassant_possible)

                    
    def undoMove(self):
        if len(self.move_log) != 0 :
            move = self.move_log.pop()
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col]     = move.piece_captured
            self.white_to_move = not self.white_to_move
            if move.piece_moved == "wK":
                self.white_king_location = (move.start_row,move.start_col)
            elif move.piece_moved == "bK":
                self.black_king_location = (move.start_row , move.start_col)    
            
            if move.is_enpassant_move:
                self.board[move.end_row][move.end_col] = "--" 
                self.board[move.start_row][move.end_col] = move.piece_captured
                

            self.enpassant_possible_log.pop()
            self.enpassant_possible = self.enpassant_possible_log[-1]
                   
    
    def getValidMoves(self):
        moves = []
        self.in_check, self.pins, self.checks = self.checkForPinsAndChecks()

        if self.white_to_move:
            king_row = self.white_king_location[0]
            king_col = self.white_king_location[1]
        else:
            king_row = self.black_king_location[0]
            king_col = self.black_king_location[1]
        if self.in_check:
            if len(self.checks) == 1:  # only 1 check, block the check or move the king
                moves = self.getAllPossibleMoves()
                # to block the check you must put a piece into one of the squares between the enemy piece and your king
                check = self.checks[0]  # check information
                check_row = check[0]
                check_col = check[1]
                piece_checking = self.board[check_row][check_col]
                valid_squares = []  # squares that pieces can move to
                # if knight, must capture the knight or move your king, other pieces can be blocked
                if piece_checking[1] == "N":
                    valid_squares = [(check_row, check_col)]
                else:
                    for i in range(1, 8):
                        valid_square = (king_row + check[2] * i,
                                        king_col + check[3] * i)  # check[2] and check[3] are the check directions
                        valid_squares.append(valid_square)
                        if valid_square[0] == check_row and valid_square[
                            1] == check_col:  # once you get to piece and check
                            break
                # get rid of any moves that don't block check or move king
                for i in range(len(moves) - 1, -1, -1):  # iterate through the list backwards when removing elements
                    if moves[i].piece_moved[1] != "K":  # move doesn't move king so it must block or capture
                        if not (moves[i].end_row,
                                moves[i].end_col) in valid_squares:  # move doesn't block or capture piece
                            moves.remove(moves[i])
            else:  # double check, king has to move
                self.getKingMoves(king_row, king_col, moves)
        else:  # not in check - all moves are fine
            moves = self.getAllPossibleMoves()
        if len(moves) == 0:
            if self.inCheck():
                self.checkmate = True
            else:
                # TODO stalemate on repeated moves
                self.stalemate = True
        else:
            self.checkmate = False
            self.stalemate = False
        return moves

    def inCheck(self):

        if self.white_to_move:
            return self.squareUnderAttack(self.white_king_location[0], self.white_king_location[1])
        else:
            return self.squareUnderAttack(self.black_king_location[0], self.black_king_location[1])

    def squareUnderAttack(self, row, col):

        self.white_to_move = not self.white_to_move 
        opponents_moves = self.getAllPossibleMoves()
        self.white_to_move = not self.white_to_move
        for move in opponents_moves:
            if move.end_row == row and move.end_col == col:  
                return True
        return False

    def getAllPossibleMoves(self):
        moves = []
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                turn = self.board[row][col][0]
                if (turn == "w" and self.white_to_move) or (turn == "b" and not self.white_to_move):
                    piece = self.board[row][col][1]
                    self.moveFunctions[piece](row, col, moves)  
        return moves

    def checkForPinsAndChecks(self):
        pins = []  
        checks = []  
        in_check = False
        if self.white_to_move:
            enemy_color = "b"
            ally_color = "w"
            start_row = self.white_king_location[0]
            start_col = self.white_king_location[1]
        else:
            enemy_color = "w"
            ally_color = "b"
            start_row = self.black_king_location[0]
            start_col = self.black_king_location[1]
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        for j in range(len(directions)):
            direction = directions[j]
            possible_pin = () 
            for i in range(1, 8):
                end_row = start_row + direction[0] * i
                end_col = start_col + direction[1] * i
                if 0 <= end_row <= 7 and 0 <= end_col <= 7:
                    end_piece = self.board[end_row][end_col]
                    if end_piece[0] == ally_color and end_piece[1] != "K":
                        if possible_pin == (): 
                            possible_pin = (end_row, end_col, direction[0], direction[1])
                        else:  
                            break
                    elif end_piece[0] == enemy_color:
                        enemy_type = end_piece[1]
                        if (0 <= j <= 3 and enemy_type == "R") or (4 <= j <= 7 and enemy_type == "B") or (
                                i == 1 and enemy_type == "p" and (
                                (enemy_color == "w" and 6 <= j <= 7) or (enemy_color == "b" and 4 <= j <= 5))) or (
                                enemy_type == "Q") or (i == 1 and enemy_type == "K"):
                            if possible_pin == (): 
                                in_check = True
                                checks.append((end_row, end_col, direction[0], direction[1]))
                                break
                            else:  
                                pins.append(possible_pin)
                                break
                        else:  
                            break
                else:
                    break 

        knight_moves = ((-2, -1), (-2, 1), (-1, 2), (1, 2), (2, -1), (2, 1), (-1, -2), (1, -2))
        for move in knight_moves:
            end_row = start_row + move[0]
            end_col = start_col + move[1]
            if 0 <= end_row <= 7 and 0 <= end_col <= 7:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] == enemy_color and end_piece[1] == "N": 
                    in_check = True
                    checks.append((end_row, end_col, move[0], move[1]))
        return in_check, pins, checks
    
    # --------------------------------------------
     #   this function to get all moves for pieces
    def getPawnMoves(self,r,c,moves):
        piecePinned = False
        pinDirectoin = ()
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0] == r and self.pins[i][1] == c :
                piecePinned = True
                pinDirectoin = (self.pins[i][2],self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        
        if self.white_to_move:
            if self.board[r-1][c]=="--":
                if not piecePinned or pinDirectoin == (-1,0):
                    moves.append(Move((r,c),(r-1,c),self.board))
                    if r == 6 and self.board[r-2][c] == "--":
                        moves.append(Move((r,c),(r-2,c),self.board))
            if c-1 >= 0 :
                if self.board[r-1][c-1][0] == 'b':
                    if not piecePinned or pinDirectoin == (-1,-1):
                        moves.append(Move((r,c),(r-1,c-1),self.board))
                elif (r-1,c-1) == self.enpassant_possible:
                    moves.append(Move((r,c),(r-1,c-1),self.board,is_enpassant_move=True))
            if c+1 <= 7 :
                if self.board[r-1][c+1][0] == 'b':
                    if not piecePinned or pinDirectoin == (-1,1):
                        moves.append(Move((r,c),(r-1,c+1),self.board))
                elif (r-1,c+1) == self.enpassant_possible:
                    moves.append(Move((r,c),(r-1,c+1),self.board,is_enpassant_move=True))
        else:
            if self.board[r+1][c]=="--":
                if not piecePinned or pinDirectoin == (1,0):
                    moves.append(Move((r,c),(r+1,c),self.board))
                    if r == 1 and self.board[r+2][c] == "--":
                        moves.append(Move((r,c),(r+2,c),self.board))
            if c-1 >= 0 :
                if self.board[r+1][c-1][0] == 'w':
                    if not piecePinned or pinDirectoin == (1,-1):
                        moves.append(Move((r,c),(r+1,c-1),self.board))
                elif (r+1,c-1) == self.enpassant_possible:
                    moves.append(Move((r,c),(r+1,c-1),self.board,is_enpassant_move=True))
            if c+1 <= 7 :
                if self.board[r+1][c+1][0] == 'w':
                    if not piecePinned or pinDirectoin == (1,1):
                        moves.append(Move((r,c),(r+1,c+1),self.board))
                elif (r+1,c+1) == self.enpassant_possible:
                    moves.append(Move((r,c),(r+1,c+1),self.board,is_enpassant_move=True))
        # still not make update pawn when arrirve last row
    
    def getRookMoves(self,r,c,moves):
        piecePinned = False
        pinDirectoin = ()
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0] == r and self.pins[i][1] == c :
                piecePinned = True
                pinDirectoin = (self.pins[i][2],self.pins[i][3])
                if self.board[r][c][1] != "Q":
                    self.pins.remove(self.pins[i])
                break
        directions = ((-1,0),(0,-1),(1,0),(0,1))
        enemyColor = "b" if self.white_to_move else "w"
        for d in directions:
            for i in range(1,8):
                end_row = r + d[0] * i 
                end_col = c + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8 :
                    if not piecePinned or pinDirectoin == d or pinDirectoin == (-d[0], -d[1]): 
                        endPiece = self.board[end_row][end_col]
                        if endPiece == "--":
                            moves.append(Move((r,c),(end_row, end_col),self.board))
                        elif endPiece[0] == enemyColor:
                            moves.append(Move((r,c),(end_row, end_col),self.board))
                            break
                        else:
                            break
                else:
                    break
                          
    def getKnightMoves(self,r,c,moves):
        piecePinned = False
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0] == r and self.pins[i][1] == c :
                piecePinned = True
                self.pins.remove(self.pins[i])
                break
        
        nightMoves = ((2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2))
        allyColor = "w" if self.white_to_move else "b"
        for nightMove in nightMoves:
            end_row = r + nightMove[0]
            end_col = c + nightMove[1]
            if 0 <= end_row < 8 and 0 <= end_col <8:
                if not piecePinned:
                    endPiece = self.board[end_row][end_col]
                    if endPiece[0] != allyColor:
                        moves.append(Move((r,c),(end_row,end_col),self.board))
    
    def getBishopMoves(self,r,c,moves):
        piecePinned = False
        pinDirectoin = ()
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0] == r and self.pins[i][1] == c :
                piecePinned = True
                pinDirectoin = (self.pins[i][2],self.pins[i][3])
                if self.board[r][c][1] != "Q":
                    self.pins.remove(self.pins[i])
                break
        directions = ((-1,-1),(1,-1),(1,1),(-1,1))
        enemyColor = "b" if self.white_to_move else "w"
        for d in directions:
            for i in range(1,8):
                end_row = r + d[0] * i 
                end_col = c + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8 :
                    if not piecePinned or pinDirectoin == d or pinDirectoin == (-d[0], -d[1]): 
                        endPiece = self.board[end_row][end_col]
                        if endPiece == "--":
                            moves.append(Move((r,c),(end_row, end_col),self.board))
                        elif endPiece[0] == enemyColor:
                            moves.append(Move((r,c),(end_row, end_col),self.board))
                            break
                        else:
                            break
                else:
                    break
    
    def getQueenMoves(self,r,c,moves):
        self.getBishopMoves(r,c,moves)
        self.getRookMoves(r,c,moves)
    
    def getKingMoves(self,r,c,moves):
        kingMoves = ((-1,0),(0,-1),(1,0),(0,1),(-1,-1),(-1,1),(1,-1),(1,1))
        allyColor = "w" if self.white_to_move else "b"
        for i in range(8):
            end_row = r + kingMoves[i][0]
            end_col = c + kingMoves[i][1]
            if 0 <= end_row < 8 and 0 <= end_col < 8 :
                endPiece = self.board[end_row][end_col]
                if endPiece[0] != allyColor :
                    if allyColor == "w":
                        self.white_king_location = (end_row , end_col)
                    else:
                        self.black_king_location = (end_row , end_col)
                    inCheck , pins , checks = self.checkForPinsAndChecks()
                    if not inCheck:
                        moves.append(Move((r,c),(end_row , end_col),self.board))
                    if allyColor == "w":
                        self.white_king_location = (r,c)  
                    else:
                        self.black_king_location = (r,c)
        
                     
# -----------------------------------------------------------------------
# -----------------------------------------------------------------------
# this class to cupture moves
class Move():
    # this for number rows from 1 to 8 start from white side
    ranksToRows ={"1":7,"2":6,"3":5,"4":4,"5":3,"6":2,"7":1,"8":0}
    rowsToRanks ={v : k for k , v in ranksToRows.items()}
    
    # this for number rows from 1 to 8 start from white side
    filesToCols = {"a":0,"b":1,"c":2,"d":3,"e":4,"f":5,"g":6,"h":7}
    colsToFiles = {v : k for k , v in filesToCols.items()}
    # -----------------------------------------------------------------------
    # define properties of Object
    def __init__(self , startSq , endSq , board , is_enpassant_move = False):
        self.start_row       = startSq[0]
        self.start_col       = startSq[1]
        self.end_row         = endSq[0]
        self.end_col         = endSq[1]
        self.piece_moved     = board[self.start_row][self.start_col]
        self.piece_captured  = board[self.end_row][self.end_col]
        self.moveID         = self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col
        
        self.is_pawn_promotion = (self.piece_moved == "wp" and self.end_row == 0) or (self.piece_moved == "bp" and self.end_row == 7)
        
        self.is_enpassant_move = is_enpassant_move
        if self.is_enpassant_move:
            self.piece_captured = "wp" if self.piece_moved == "bp" else "bp"
    
    def __eq__(self,other):
        if isinstance(other,Move):
            return self.moveID == other.moveID
        return False    
           
    def getRankFile(self , r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]

    def getChessNotation(self):
        # Get the name of the piece that moved, excluding pawns
        piece = ''
        if self.piece_moved[1] != 'p':  # Pawns are not denoted by their name
            piece = self.piece_moved[1].upper()

        # Check if a piece was captured
        capture = ''     
        if self.piece_captured != "--":
            capture = 'x'
            
        startSquare = self.getRankFile(self.start_row, self.start_col)

        # Get the ending square in rankfile notation
        endSquare = self.getRankFile(self.end_row, self.end_col)

        return piece + startSquare+" -> " + capture + endSquare

