import random
import InvcEngine

"""
Movements
"""
def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves)-1)]
    

def findBestMove(valid_moves):
    bestMove = None
    global count
    moveseq = "".join([str(item) for item in InvcEngine.Move_List])
    lostmoveDecision = InvcEngine.GameState.LM(moveseq)
    random.shuffle(valid_moves) 
    for playerMove in valid_moves:            
        if InvcEngine.Move.getChessNotation(playerMove) not in lostmoveDecision:                
            bestMove = playerMove
            break             
    return bestMove


