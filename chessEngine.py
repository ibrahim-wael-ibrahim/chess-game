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
        self.movesDictinary ={
            "p":self.getPawnMoves,
            "R":self.getRookMoves,
            "N":self.getNightMoves,
            "B":self.getBishopMoves,
            "Q":self.getQueenMoves,
            "K":self.getKingMoves
        }
        self.whiteToMove = True
        self.moveLog = [] 
        self.whiteKingLoction = (7,4)
        self.blackKingLoction = (0,4)
        # self.checkMate = False
        # self.staleMate = False
        self.inCheck = False
        self.pins =[]
        self.checks =[]
        
    def makeMove(self,move):
        if self.board[move.startRow][move.startCol] != "--":
            self.board[move.startRow][move.startCol] = "--"
            self.board[move.endRow][move.endCol]     = move.pieceMoved
            self.moveLog.append(move)
            self.whiteToMove = not self.whiteToMove
            if move.pieceMoved == "wK":
                self.whiteKingLoction = (move.endRow,move.endCol)
            elif move.pieceMoved == "bK":
                self.blackKingLoction = (move.endRow , move.endCol)
                      
    def undoMove(self):
        if len(self.moveLog) != 0 :
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol]     = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove
            if move.pieceMoved == "wK":
                self.whiteKingLoction = (move.startRow,move.startCol)
            elif move.pieceMoved == "bK":
                self.blackKingLoction = (move.startRow , move.startCol)           
    
    def getValidMoves(self):
        moves =[]
        self.inCheck , self.pins , self.checks = self.checkForPinsAndChecks()
        if self.whiteToMove:
            KingRow = self.whiteKingLoction[0]
            KingCol = self.whiteKingLoction[1]
        else:
            KingRow = self.blackKingLoction[0]
            KingCol = self.blackKingLoction[1]
        if self.inCheck:
            if len(self.checks) == 1 :
                moves = self.getAllPossibleMoves()
                check = self.checks[0]
                checkRow = check[0]
                checkCol = check[1]
                pieceChecking = self.board[checkRow][checkCol]
                validSquares =[]
                if pieceChecking[1] == "N":
                    validSquares = [(checkRow , checkCol)]
                else:
                    for i in range(1,8):
                        validSquare = (KingRow + check[2] * i , KingCol + check[3] * i)
                        validSquares.append(validSquare)
                        if validSquare[0] == checkRow and validSquare[1] == checkCol:
                            break
                for i in range(len(moves)-1,-1,-1):
                    if moves[i].pieceMoved[1] != "K":
                        if not (moves[i].endRow,moves[i].endCol) in validSquares:
                            moves.remove(moves[i])
            else:
                self.getKingMoves(KingRow,KingCol,moves)
        else:
            moves = self.getAllPossibleMoves()
        
        return moves
                             
                        
                    
            
    def checkForPinsAndChecks(self):
        pins = []
        checks = []
        inCheck = False
        if self.whiteToMove:
            enemyColor ="b"
            allyColor  ="w"
            startRow   = self.whiteKingLoction[0]
            startCol   = self.whiteKingLoction[1]
        else:
            enemyColor ="W"
            allyColor  ="b"
            startRow   = self.blackKingLoction[0]
            startCol   = self.blackKingLoction[1]
        directions = ((-1,0),(0,-1),(1,0),(0,1),(-1,-1),(-1,1),(1,-1),(1,1))
        for j in range(len(directions)):
            d = directions[j]
            possiblePin = ()
            for i in range(1,8):
                endRow = startRow + d[0] * i
                endCol = startCol + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8 :
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] == allyColor:
                        if possiblePin == ():
                            possiblePin = (endRow, endCol , d[0] , d[1])
                        else:
                            break
                    elif endPiece[0] == enemyColor:
                        type = endPiece[1]
                        if (0 <= j <= 3 and type == "R") or \
                            ( 4 <= j <= 7 and type == "B" ) or \
                            (i == 1 and type == 'p' and ((enemyColor == "w" and 6 <= j <=7) or (enemyColor == 'b' and 4 <= j <=5))) or \
                            (type == "Q") or (i==1 and type == "K"):
                            if possiblePin == ():
                                inCheck = True
                                checks.append((endRow , endCol ,d[0] ,d[1]))
                                break
                            else:
                                pins.append(possiblePin)
                                break
                        else:
                            break
                        
        nightMoves = ((-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1))
        for move in nightMoves:
            endRow = startRow + move[0]
            endCol = startCol + move[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8 :
                endPiece = self.board[endRow][endCol]
                if endPiece[0] == enemyColor and endPiece[1] == "N":
                    inCheck = True
                    checks.append((endRow, endCol , move[0] , move[1]))
        return inCheck , pins , checks                                
                                        
                            
                

        
        
        
        
        
        
        
        
        
        
        
        
        
              
        # --------------------------------------------------- => anthor way to make check
        # moves = self.getAllPossibleMoves()
        # for i in range(len(moves)-1,-1,-1):
        #     self.makeMove(moves[i])
            
        #     self.whiteToMove = not self.whiteToMove
        #     if self.inCheck():
        #         print("This move will make Chack")
        #         moves.remove(moves[i])
        #     self.whiteToMove = not self.whiteToMove
        #     self.undoMove()
        # if len(moves) == 0:
        #     if self.inCheck():
        #         self.checkMate = True
        #         print("Check Mate")
        #     else:
        #         self.staleMate = True
        #         print("stale Mate")
                
        # else:
        #     self.checkMate = False
        #     self.staleMate = False        
        # return moves
    # ----------------------------------------------------------------------------------
# this function to make check
    # def inCheck(self):
    #     if self.whiteToMove:
    #         return self.squareUnderAttack(self.whiteKingLoction[0],self.whiteKingLoction[1])
    #     else:
    #         return self.squareUnderAttack(self.blackKingLoction[0],self.blackKingLoction[1])
            
    # def squareUnderAttack(self,r,c):
    #     self.whiteToMove = not self.whiteToMove
    #     oppMoves = self.getAllPossibleMoves()
    #     self.whiteToMove = not self.whiteToMove
    #     for move in oppMoves :
    #         if move.endRow == r and move.endCol == c :
    #             return True
    #     return False
 
    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.movesDictinary[piece](r,c,moves)
        # for move in moves :
        #     print(move.getChessNotation())
        return moves
    
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
        
        if self.whiteToMove:
            if self.board[r-1][c]=="--":
                if not piecePinned or pinDirectoin == (-1,0):
                    moves.append(Move((r,c),(r-1,c),self.board))
                    if r == 6 and self.board[r-2][c] == "--":
                        moves.append(Move((r,c),(r-2,c),self.board))
            if c-1 >= 0 :
                if self.board[r-1][c-1][0] == 'b':
                    if not piecePinned or pinDirectoin == (-1,-1):
                        moves.append(Move((r,c),(r-1,c-1),self.board))
            if c+1 <= 7 :
                if self.board[r-1][c+1][0] == 'b':
                    if not piecePinned or pinDirectoin == (-1,1):
                        moves.append(Move((r,c),(r-1,c+1),self.board))
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
            if c+1 <= 7 :
                if self.board[r+1][c+1][0] == 'w':
                    if not piecePinned or pinDirectoin == (1,1):
                        moves.append(Move((r,c),(r+1,c+1),self.board))
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
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1,8):
                endRow = r + d[0] * i 
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8 :
                    if not piecePinned or pinDirectoin == d or pinDirectoin == (-d[0], -d[1]): 
                        endPiece = self.board[endRow][endCol]
                        if endPiece == "--":
                            moves.append(Move((r,c),(endRow, endCol),self.board))
                        elif endPiece[0] == enemyColor:
                            moves.append(Move((r,c),(endRow, endCol),self.board))
                            break
                        else:
                            break
                else:
                    break
                          
    def getNightMoves(self,r,c,moves):
        piecePinned = False
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0] == r and self.pins[i][1] == c :
                piecePinned = True
                self.pins.remove(self.pins[i])
                break
        
        nightMoves = ((2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2))
        allyColor = "w" if self.whiteToMove else "b"
        for nightMove in nightMoves:
            endRow = r + nightMove[0]
            endCol = c + nightMove[1]
            if 0 <= endRow < 8 and 0 <= endCol <8:
                if not piecePinned:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] != allyColor:
                        moves.append(Move((r,c),(endRow,endCol),self.board))
    
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
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1,8):
                endRow = r + d[0] * i 
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8 :
                    if not piecePinned or pinDirectoin == d or pinDirectoin == (-d[0], -d[1]): 
                        endPiece = self.board[endRow][endCol]
                        if endPiece == "--":
                            moves.append(Move((r,c),(endRow, endCol),self.board))
                        elif endPiece[0] == enemyColor:
                            moves.append(Move((r,c),(endRow, endCol),self.board))
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
        allyColor = "w" if self.whiteToMove else "b"
        for i in range(8):
            endRow = r + kingMoves[i][0]
            endCol = c + kingMoves[i][1]
            if 0 <= endRow < 8 and 0 <= endCol < 8 :
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor :
                    if allyColor == "w":
                        self.whiteKingLoction = (endRow , endCol)
                    else:
                        self.blackKingLoction = (endRow , endCol)
                    inCheck , pins , checks = self.checkForPinsAndChecks()
                    if not inCheck:
                        moves.append(Move((r,c),(endRow , endCol),self.board))
                    if allyColor == "w":
                        self.whiteKingLoction = (r,c)  
                    else:
                        self.blackKingLoction = (r,c)
        # kingMoves = ((-1,0),(0,-1),(1,0),(0,1),(-1,-1),(-1,1),(1,-1),(1,1))
        # allyColor = "w" if self.whiteToMove else "b"
        # for i in range(8):
        #     endRow = r + kingMoves[i][0]
        #     endCol = c + kingMoves[i][1]
        #     if 0 <= endRow < 8 and 0 <= endCol <8:
        #         endPiece = self.board[endRow][endCol]
        #         if endPiece[0] != allyColor:
        #             moves.append(Move((r,c),(endRow,endCol),self.board))
            
        # # enemyColor = "b" if self.whiteToMove else "w"
        # # for d in directions:
        # #     endRow = r + d[0]
        # #     endCol = c + d[1]
        # #     if 0 <= endRow < 8 and 0 <= endCol < 8 :
        # #         endPiece = self.board[endRow][endCol]
        # #         if endPiece == "--":
        # #             moves.append(Move((r,c),(endRow, endCol),self.board))
        # #         elif endPiece[0] == enemyColor:
        # #             moves.append(Move((r,c),(endRow, endCol),self.board))
        # #         else:
        # #             continue
        # #     else:
        # #         continue
                     
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
    def __init__(self , startSq , endSq , board):
        self.startRow       = startSq[0]
        self.startCol       = startSq[1]
        self.endRow         = endSq[0]
        self.endCol         = endSq[1]
        self.pieceMoved     = board[self.startRow][self.startCol]
        self.pieceCaptured  = board[self.endRow][self.endCol]
        self.moveID         = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
        
    def __eq__(self,other):
        if isinstance(other,Move):
            return self.moveID == other.moveID
        return False    
           
    def getRankFile(self , r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]

    def getChessNotation(self):
        # Get the name of the piece that moved, excluding pawns
        piece = ''
        if self.pieceMoved[1] != 'p':  # Pawns are not denoted by their name
            piece = self.pieceMoved[1].upper()

        # Check if a piece was captured
        capture = ''
        if self.pieceCaptured != "--":
            capture = 'x'
            
        startSquare = self.getRankFile(self.startRow, self.startCol)

        # Get the ending square in rankfile notation
        endSquare = self.getRankFile(self.endRow, self.endCol)

        return piece + startSquare+" -> " + capture + endSquare

