"""
Main Driver file. Responsible for inputs and displaying the current GameState Objects.
"""
from glob import glob
from turtle import color
import matplotlib
import pygame as p
import InvcEngine, ReLearning
import pyautogui
import Menu, pylab
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.backends.backend_agg as agg
from tabulate import tabulate
matplotlib.use("Agg")

Game_WIDTH, Game_HEIGHT= pyautogui.size()
BOARD_WIDTH = BOARD_HEIGHT =  Game_HEIGHT//3
DIMENSION = 3
SQUARE_SIZE = BOARD_HEIGHT // DIMENSION
Pad_Left = (Game_WIDTH//2) - (BOARD_WIDTH//2) 
Pad_Top = (Game_HEIGHT//2) - (BOARD_HEIGHT//2)
MAX_FPS = 30
IMAGES = {}
Win_Lose = []
AI_WP = [0]
Game_Rounds = [0]
Game_Roundsplot = [0]
Rounds = 0
PlayerWin = 0


def loadImages():
    """
    Initialize a global directory of images.
    This will be called exactly once in the main.
    """
    pieces = ['wp','bp']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("Inv City/Images/" + piece + ".png"), (SQUARE_SIZE, SQUARE_SIZE))
        # To access, IMAGES['wp']

"""
Main driver of the code. This will handle user input and updating the graphics
"""
def main():
    global Rounds, Win_Lose, PlayerWin
    p.init()
    screen = p.display.set_mode((Game_WIDTH, Game_HEIGHT),p.FULLSCREEN)

    background = p.transform.scale(p.image.load("Inv City/Images/b.jpg"),(Game_WIDTH,Game_HEIGHT)) #try

    clock = p.time.Clock()
    screen.fill(p.Color("White"))

    game_state = InvcEngine.GameState()
    valid_moves = game_state.getValidMoves()    
    move_made = False #flag variable when a move is made
    AILost = False
    loadImages()
    running = True
    square_selected = ()  # no square is selected initially, this will keep track of the last click of the user (tuple(row,col))
    player_clicks = []  # this will keep track of player clicks (two tuples)
    gameOver = False    
    click = False
    while running:
        playerOne = Menu.p1()
        playerTwo = Menu.p2()
        humanTurn = (game_state.white_to_move and playerOne) or (not game_state.white_to_move and playerTwo)
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver and humanTurn:
                    location = p.mouse.get_pos() #(x,y) location of mouse, need to take care if the game does not have full screen (has side panel)
                    col = (location[0]-Pad_Left)//SQUARE_SIZE
                    row = (location[1]-Pad_Top)//SQUARE_SIZE
                    if square_selected == (row, col) or col >= 3 or row>=3 or col <= -1 or row<=-1:  # user clicked the same square twice
                        square_selected = ()  # deselect
                        player_clicks = []  # clear clicks
                    else:
                        square_selected = (row, col)
                        player_clicks.append(square_selected)  # append for both 1st and 2nd click
                    if len(player_clicks) == 2: 
                        move = InvcEngine.Move(player_clicks[0], player_clicks[1], game_state.board)
                        # print("Moves: ",InvcEngine.Move_List)                         
                        if move in valid_moves: 
                            game_state.makeMove(move)
                            move_made = True    
                            InvcEngine.Move_List.append(move.getChessNotation())  
                            if playerTwo == True and game_state.white_to_move:
                                AIMove = move                            
                            square_selected= () #reset user clicks  
                            player_clicks= []                            
                        else:
                            player_clicks = [square_selected]

            elif e.type == p.KEYDOWN:
                if e.key ==p.K_ESCAPE:
                    Menu.menu(screen,Game_WIDTH, Game_HEIGHT,Pad_Left, Pad_Top,click)  
                         
            screen.blit(background,(0,0)) #background image

        if gameOver:                     
            game_state = InvcEngine.GameState()
            valid_moves = game_state.getValidMoves()
            square_selected = ()
            player_clicks = []                  
            InvcEngine.AILostMove = "Null"            
            move_made = False
            gameOver = False
            humanTurn = True                             
            if AILost:
                Win_Lose.append("U_W")
                game_state.AIMove(AIMove,AILost) 
                AILost = False
                PlayerWin = PlayerWin + 1                                     
            elif not AILost:
                Win_Lose.append("U_L")
                AILost = False                    
            Rounds = Rounds + 1
            print(Rounds, Win_Lose) 
            Game_Rounds.append(Rounds)
            Game_Roundsplot.append(Rounds)
            print("AI:", 100-((PlayerWin/Rounds)*100), "Player:", (PlayerWin/Rounds)*100 )
            AI_WP.append(100-((PlayerWin/Rounds)*100))
            InvcEngine.Move_List = ["Node"]
            InvcEngine.AILost_Move_List = ["Null"]
            p.time.wait(1000)           
                    
        #AI move finder
        if  not humanTurn and not gameOver and not game_state.white_to_move:                        
            AIMove = ReLearning.findBestMove(valid_moves)            
            if AIMove is None:
                print("random Move")
                AIMove = ReLearning.findRandomMove(valid_moves)
            game_state.makeMove(AIMove) 
            game_state.AIMove(AIMove,AILost)           
            move_made = True
        
        elif not humanTurn and not gameOver and game_state.white_to_move:
            pAIMove = ReLearning.findRandomMove(valid_moves) 
            game_state.makeMove(pAIMove)
            InvcEngine.Move_List.append(pAIMove.getChessNotation())
            move_made = True 
                    
        if move_made: 
            animateMove(game_state.move_log[-1],screen, game_state.board,clock)
            valid_moves = game_state.getValidMoves()  
            move_made = False
        
        drawGameState(screen, game_state, valid_moves, square_selected) 

        if game_state.reachedEnd:            
            gameOver = True
            if game_state.white_to_move:
                drawEndGameText(screen, 'A I     w i n s')                
            else:
                drawEndGameText(screen, 'Y o u      w i n')
                AILost = True
                
        elif game_state.noPossibleMoves:
            gameOver = True
            if game_state.white_to_move:
                drawEndGameText(screen, 'A I     w i n s')       
            else:
                drawEndGameText(screen, 'Y o u     w i n')
                AILost = True                        
     
        clock.tick(MAX_FPS)
        p.display.flip()


def Graph(screen):
    global AI_WP, Game_Rounds
    fig = pylab.figure(figsize=[4, 4], dpi=100, )
    Y = [0,10,20,30,40,50,60,70,80,90,100] #
    plt.yticks(Y,Y)
    plt.plot(Game_Rounds, AI_WP)    
    fig.patch.set_visible(False)
    canvas = agg.FigureCanvasAgg(fig)
    canvas.draw() 
    renderer = canvas.get_renderer()
    raw_data = renderer.tostring_rgb()
    size = canvas.get_width_height()
    # Rect = p.Rect(0,0, 100, 25)
    Rect = p.Rect(950/1350*Game_WIDTH, 140/685*Game_HEIGHT, 100, 25)
    surf = p.image.fromstring(raw_data, size, "RGB")
    p.draw.rect(screen,(255,0,0),Rect)
    # surf = p.Surface((500, 500))
    screen.blit(surf, Rect)
    p.display.flip()

def text(screen):
    Text_Display("-- Notification --", 25, screen, "Helvetica",
                 500, Pad_Left, Game_HEIGHT-450, Pad_Top)
    Text_Display("Hi Human!", 20, screen, "Helvetica",
                 500, Pad_Left, Game_HEIGHT-400, Pad_Top)
    Text_Display("The Neural Hub of the Centroids have taken over",
                 20, screen, "Helvetica", 480, Pad_Left, Game_HEIGHT-380, Pad_Top)
    Text_Display("most of the control of the conciousness chips.", 20,
                 screen, "Helvetica", 480, Pad_Left, Game_HEIGHT-360, Pad_Top)
    Text_Display("The malware isn't working anymore.", 20, screen,
                 "Helvetica", 480, Pad_Left, Game_HEIGHT-340, Pad_Top)
    Text_Display("At any possible means you have to ", 20, screen,
                 "Helvetica", 480, Pad_Left, Game_HEIGHT-320, Pad_Top)
    Text_Display("stop the AI before it completely ", 20, screen,
                 "Helvetica", 480, Pad_Left, Game_HEIGHT-300, Pad_Top)
    Text_Display("takes over it self!", 20, screen,
                 "Helvetica", 480, Pad_Left, Game_HEIGHT-280, Pad_Top)
    Text_Display("The graph at your right side will guide you.... ",
                 20, screen, "Helvetica", 480, Pad_Left, Game_HEIGHT-240, Pad_Top)
    Text_Display("Dont let the winning line of AI to get stagnant. ",
                 20, screen, "Helvetica", 480, Pad_Left, Game_HEIGHT-220, Pad_Top)
    Text_Display("Fight with everything you got. Remember  win are our",
                 20, screen, "Helvetica", 480, Pad_Left, Game_HEIGHT-200, Pad_Top)
    Text_Display("last hope! All the best.", 20, screen,"Helvetica",
                 480, Pad_Left, Game_HEIGHT-180, Pad_Top)
    Text_Display("You go first.", 20, screen, "Helvetica",
                 480, Pad_Left, Game_HEIGHT-140, Pad_Top)

    if Rounds>0:
        Text_Display("AI %: ", 20, screen, "Helvetica",
                    Game_WIDTH-70, Pad_Left, Game_HEIGHT-80, Pad_Top)
        Text_Display(str(round(100-((PlayerWin/Rounds)*100),1)), 20, screen, "Helvetica",
                    Game_WIDTH+15, Pad_Left, Game_HEIGHT-80, Pad_Top)    

        Text_Display("You %: ", 20, screen, "Helvetica",
                    Game_WIDTH-80, Pad_Left, Game_HEIGHT-50, Pad_Top)
        Text_Display(str(round((PlayerWin/Rounds)*100,1)), 20, screen, "Helvetica",
                    Game_WIDTH+15, Pad_Left, Game_HEIGHT-50, Pad_Top)


def drawGameState(screen, game_state, valid_moves, square_selected):
    """
    Responsible for all the graphics within current game state.
    """
    drawBoard(screen)  # draw squares on the board
    highlightSquares(screen,game_state, valid_moves, square_selected)
    drawPieces(screen, game_state.board)  # draw pieces on top of those squares
    Graph(screen)
    text(screen)

def drawBoard(screen):
    global colors
    colors = [p.Color(209,209,209), p.Color(21,13,13)]
    for row in range(DIMENSION):        
        for column in range(DIMENSION):            
            color = colors[((row + column) % 2)]                 
            p.draw.rect(screen, color,p.Rect((column * SQUARE_SIZE)+Pad_Left, (row * SQUARE_SIZE)+Pad_Top, SQUARE_SIZE, SQUARE_SIZE))
                    
"""
Highlight square selected and moves for piece selected
"""
def highlightSquares(screen, game_state, valid_moves,square_selected):
    if square_selected !=():
        row,col = square_selected
        if game_state.board[row][col][0] == ('w' if game_state.white_to_move else 'b'): # making sure if sqselected canbe moved
            #highlight the selected sq
            s=p.Surface((SQUARE_SIZE, SQUARE_SIZE))
            s.set_alpha(100) #transparency value
            s.fill(p.Color('blue'))
            screen.blit(s,((col*SQUARE_SIZE)+Pad_Left, (row*SQUARE_SIZE)+Pad_Top))
            #highlight moves
            s.fill(p.Color('yellow'))
            for move in valid_moves:
                if move.start_row == row and move.start_col == col:
                    screen.blit(s,((move.end_col*SQUARE_SIZE)+Pad_Left, (move.end_row*SQUARE_SIZE)+Pad_Top))
                 
def drawPieces(screen, board):
    """
    Draw the pieces on the board using the current game_state.board
    """
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            piece = board[row][column]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect((column * SQUARE_SIZE)+Pad_Left, (row * SQUARE_SIZE)+Pad_Top, SQUARE_SIZE, SQUARE_SIZE))


"""
Animating a Move
"""
def animateMove(move, screen, board,clock):
    global colors
    dR = move.end_row-move.start_row
    dC = move.end_col-move.start_col
    framesPerSquare = 10
    frameCount = (abs(dR)+abs(dC))*framesPerSquare
    for frame in range(frameCount + 1):
        row,col = (move.start_row + dR*frame/frameCount,move.start_col + dC*frame/frameCount)
        drawBoard(screen)
        drawPieces(screen, board)
        # Graph(screen)
        text(screen)
        color = colors[(move.end_row + move.end_col) % 2]
        end_square = p.Rect((move.end_col * SQUARE_SIZE)+Pad_Left, (move.end_row * SQUARE_SIZE)+Pad_Top, SQUARE_SIZE, SQUARE_SIZE)
        p.draw.rect(screen,color,end_square)
        screen.blit(IMAGES[move.piece_moved], p.Rect((col * SQUARE_SIZE)+Pad_Left, (row * SQUARE_SIZE)+Pad_Top, SQUARE_SIZE, SQUARE_SIZE))
        p.display.flip()
        clock.tick(60)
    # pass

def drawEndGameText(screen, Text):
    font = p.font.SysFont("Helvetica", 25, True, False)
    textObject = font.render(Text, 0, p.Color('Black'))
    textLocation = p.Rect(Pad_Left, Pad_Top-300, BOARD_WIDTH, BOARD_HEIGHT).move(BOARD_WIDTH / 2 - textObject.get_width() / 2,
                                                                 (BOARD_HEIGHT / 2 - textObject.get_height() / 2)*2.3)
    screen.blit(textObject, textLocation)
    textObject = font.render(Text, 0, p.Color('White'))
    screen.blit(textObject, textLocation.move(1, 1))

def Text_Display(Text,size,screen,font, Game_WIDTH,Pad_Left,Game_HEIGHT,Pad_Top):
    font = p.font.SysFont("Helvetica", size, True, False)
    textObject = font.render(Text, 0, p.Color('Grey'))
    textLocation = p.Rect(Pad_Left, Pad_Top, Game_WIDTH//2-Pad_Left+19,Game_HEIGHT-150).move(Game_WIDTH // 2 - textObject.get_width() // 2-Pad_Left+19,
                                                                 Game_HEIGHT-230 - textObject.get_height()-150)
    screen.blit(textObject, textLocation)

if __name__=="__main__":
    main()
