"""
Rsponsible for storing all the info about the current state of the chess game. Also responsible for determining valid moves
and will keep a move log.
"""

Move_List = ["Node"]
AILost_Move_List = ["Null"]
AILostMove = "Null"
decision = {}

class GameState:
    def __init__(self):
        # Board is an 3x3 2d list, each element in list has 2 characters.        
        self.board = [
            ["bp", "bp", "bp"],
            ["--", "--", "--"],           
            ["wp", "wp", "wp"],
        ]
        self.white_to_move = True
        self.move_log = []   
        self.AIClicks = []
        self.noPossibleMoves = False
        self.reachedEnd = False           
        self.bp1Location = (0,0)
        self.bp2Location = (0,1)
        self.bp3Location = (0,2)         
    
    def makeMove(self,move):
        """
        Takes a Move as a parameter and executes it.
        (this will not work for castling, pawn promotion and en-passant)
        """        
        self.board[move.start_row][move.start_col] = "--"
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.move_log.append(move)  # log the move so we can undo it later
        self.white_to_move = not self.white_to_move  # switch players
        if (move.piece_moved == 'wp' and move.end_row == 0) or (move.piece_moved == 'bp' and move.end_row == 2):
            self.reachedEnd = True 
    
    def AIMove(self,AIMove,AILost):   
        global AILostMove,decision, AILost_Move_List     
        if AILost: 
            # print("True")           
            AILostMove = AIMove.getChessNotation()
            Move_List.pop()
            Move_List.pop() 
            moveseq = "".join([str(item) for item in Move_List])   
            if moveseq not in decision.keys():         
                decision[moveseq] = AILost_Move_List
            if AILostMove in decision[moveseq]:
                Move_List.pop()
                AILostMove = Move_List[-1]
                Move_List.pop()
                moveseq = "".join([str(item) for item in Move_List])
                if moveseq != '':
                    decision[moveseq].append(AILostMove)
            elif AILostMove not in decision[moveseq]:
                decision[moveseq].append(AILostMove)
        else:
                Move_List.append(AIMove.getChessNotation())                             
        # print("Moves: ", Move_List)
        print(decision)
    
    def LM(moveseq):
        global decision          
        if moveseq in decision.keys():
            return decision[moveseq]
        else:
            return AILost_Move_List
        
    # All possible moves with checks.
    def getValidMoves(self):
        moves = self.getAllPossibleMoves()
        if len(moves) == 0:
            self.noPossibleMoves = True
        else:
            self.noPossibleMoves = False
        return moves             

    # All possible moves without checks.
    def getAllPossibleMoves(self):
        moves = []
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                turn = self.board[row][col][0]
                if (turn == "w" and self.white_to_move) or (turn == "b" and not self.white_to_move):
                    piece = self.board[row][col][1]
                    if piece == 'p':
                        self.getPawnMoves (row,col,moves)        
        return moves 

    def getPawnMoves(self,row,col, moves):
        if self.white_to_move: #whitepawn
            if self.board[row-1][col]== "--":
                moves.append(Move((row,col), (row-1,col),self.board))
                if row == 2 and self.board[row-1][col] == "--":
                    moves.append(Move((row,col), (row-1,col), self.board))
            if col-1 >=0: #left capture
                if self.board[row-1][col-1][0]=='b':
                    moves.append(Move((row,col), (row-1,col-1), self.board))
            if col+1 <= 2: #right capture
                if self.board[row-1][col+1][0] == 'b':
                    moves.append(Move((row,col), (row-1,col+1), self.board))
        
        else: #blackpawn
            if self.board[row+1][col]== "--":
                moves.append(Move((row,col), (row+1,col),self.board))
                if row == 0 and self.board[row+1][col] == "--":
                    moves.append(Move((row,col), (row+1,col), self.board))
            if col-1 >=0: #left capture
                if self.board[row+1][col-1][0]=='w':
                    moves.append(Move((row,col), (row+1,col-1), self.board))
            if col+1 <= 2: #right capture
                if self.board[row+1][col+1][0] == 'w':
                    moves.append(Move((row,col), (row+1,col+1), self.board))
    
class Move():
    # in chess, fields on the board are described by two symbols, one of them being number between 1-8 (which is corresponding to rows)
    # and the second one being a letter between a-f (corresponding to columns), in order to use this notation we need to map our [row][col] coordinates
    # to match the ones used in the original chess game
    ranks_to_rows = {"1": 2, "2": 1, "3": 0}
    rows_to_ranks = {v: k for k, v in ranks_to_rows.items()}
    files_to_cols = {"a": 0, "b": 1, "c": 2}
    cols_to_files = {v: k for k, v in files_to_cols.items()}

    def __init__(self, start_square, end_square, board):
        self.start_row = start_square[0]
        self.start_col = start_square[1]
        self.end_row = end_square[0]
        self.end_col = end_square[1]
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]
        self.moveID = self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col 
                             
        
    """
    Overring the equals method
    """
    def __eq__ (self,other):
        if isinstance(other,Move):
            return self.moveID == other.moveID
        return False
    
    def getChessNotation(self):
        return self.getRankFile(self.start_row, self.start_col) + self.getRankFile(self.end_row, self.end_col)
        

    def getRankFile(self, row, col):
        return self.cols_to_files[col] + self.rows_to_ranks[row]