from matplotlib.pyplot import draw
import pygame as p

def draw_text(text, font, color, surface, x,y):
    textobj= font.render(text,1,color)
    textrect= textobj.get_rect()
    textrect.topleft = (x,y)
    surface.blit(textobj, textrect)

playerOne = True #If human is playing it is true
playerTwo = False #False if AI is playing black
def p1():
    return playerOne
def p2():
    return playerTwo

def menu(screen,Game_WIDTH, Game_HEIGHT,Pad_Left, Pad_Top,click):
    global playerOne, playerTwo
    pause = True
    s=p.Surface((Game_WIDTH, Game_HEIGHT))
    s.set_alpha(200) #transparency value
    screen.blit(s,(0,0))
    background = p.transform.scale(p.image.load("Inv City/Images/AdamC2.png"),(800,Game_HEIGHT)) #try
    screen.blit(background,(0,0))
    while pause:
        font = p.font.SysFont("Helvetica", 25, True, False)
        fontMM = p.font.SysFont("Helvetica", 40, True, False)
        fontOF = p.font.SysFont("Helvetica", 20, True, False)
        MainMenu = fontMM.render('Main Menu', 0, p.Color('White'))
        Instructions = font.render('About Game', 0, p.Color('White'))
        Credits = font.render('How to play', 0, p.Color('White'))
        Settings = font.render('Credits', 0, p.Color('White'))
        Quit = font.render('Quit', 0, p.Color('White'))
        On = fontOF.render(' On', 0, p.Color('White'))
        Off = fontOF.render(' Off', 0, p.Color('White'))
        Automate= fontOF.render(' Automate: ', 0, p.Color('White'))
        TwoPlayer= fontOF.render(' Two Player : ', 0, p.Color('White'))

        mx,my = p.mouse.get_pos()

        MainMenuB =     p.Rect(Game_WIDTH//2-Pad_Left,Game_HEIGHT//2-Pad_Top-30,480,50)
        InstructionsB = p.Rect(Game_WIDTH//2-Pad_Left+50,Game_HEIGHT//2-Pad_Top+130-30,200,35)
        CreditsB =      p.Rect(Game_WIDTH//2-Pad_Left+50,Game_HEIGHT//2-Pad_Top+230-30,200,35)
        SettingsB =     p.Rect(Game_WIDTH//2-Pad_Left+50,Game_HEIGHT//2-Pad_Top+330-30,200,35)
        QuitB =         p.Rect(Game_WIDTH//2-Pad_Left+50,Game_HEIGHT//2-Pad_Top+430-30,200,35)
        AutoB =         p.Rect(Game_WIDTH//2-115,Game_HEIGHT-72,35,28)
        TwopB =         p.Rect(Game_WIDTH//2+100,Game_HEIGHT-72,35,28)
        AutomateB =     p.Rect(Game_WIDTH//2-200,Game_HEIGHT-72,100,25)
        TwoPlayerB =    p.Rect(Game_WIDTH//2,Game_HEIGHT-72,120,25)

        p.draw.rect(screen, (0, 0, 0),AutomateB,0)
        screen.blit(Automate, AutomateB)
        p.draw.rect(screen, (0, 0, 0),TwoPlayerB,0)
        screen.blit(TwoPlayer, TwoPlayerB)

        if playerOne == False:
            p.draw.rect(screen, (0, 0, 0),AutoB,0)
            screen.blit(On, AutoB)
        elif playerOne == True:
            p.draw.rect(screen, (0, 0, 0),AutoB,0)
            screen.blit(Off, AutoB)
        if playerTwo == True:
            p.draw.rect(screen, (0, 0, 0),TwopB,0)
            screen.blit(On, TwopB)
        elif playerTwo == False:
            p.draw.rect(screen, (0, 0, 0),TwopB,0)
            screen.blit(Off, TwopB)
        # MoreB = p.draw.circle(screen, (225,0,0), (150,50), 20)

        if InstructionsB.collidepoint((mx,my)):
            draw_text('  >',p.font.SysFont('Arial',20),(255,255,255),screen,Game_WIDTH//2-Pad_Left+20,Game_HEIGHT//2-Pad_Top+133-30)
            Text_Display("-- About Game --",20,screen,font, Game_WIDTH+870,Pad_Left,Game_HEIGHT-480,Pad_Top)
            Text_Display("*Invasion City* is a 3*3 grid game that helps us to explore",16,screen,font, Game_WIDTH+870,Pad_Left,Game_HEIGHT-440,Pad_Top)
            Text_Display(" Reinforcement Learning strategies. It tries to examine",16,screen,font, Game_WIDTH+870,Pad_Left,Game_HEIGHT-420,Pad_Top)
            Text_Display("the machine logic as it learns. It demonstrates how an ",16,screen,font, Game_WIDTH+870,Pad_Left,Game_HEIGHT-400,Pad_Top)
            Text_Display("artificial intelligence can develop and learn to pay. ",16,screen,font, Game_WIDTH+870,Pad_Left,Game_HEIGHT-380,Pad_Top)
            Text_Display("The machine learns fromthe mistakes it makes and ",16,screen,font, Game_WIDTH+870,Pad_Left,Game_HEIGHT-360,Pad_Top)
            Text_Display(" becomes unbeatable.",16,screen,font, Game_WIDTH+870,Pad_Left,Game_HEIGHT-340,Pad_Top)
        elif CreditsB.collidepoint((mx,my)):
            draw_text('  >',p.font.SysFont('Arial',20),(255,255,255),screen,Game_WIDTH//2-Pad_Left+20,Game_HEIGHT//2-Pad_Top+233-30)
            Text_Display("-- How to play --",20,screen,font, Game_WIDTH+870,Pad_Left,Game_HEIGHT-480,Pad_Top)
            Text_Display("• You play white, the AI plays black ",16,screen,font, Game_WIDTH+870,Pad_Left,Game_HEIGHT-440,Pad_Top)
            Text_Display("• White always starts ",16,screen,font, Game_WIDTH+870,Pad_Left,Game_HEIGHT-420,Pad_Top)
            Text_Display("• On your turn, there are two types of valid moves: ",16,screen,font, Game_WIDTH+870,Pad_Left,Game_HEIGHT-400,Pad_Top)
            Text_Display("• Move one of your pawns 1 square straight ahead if free ",16,screen,font, Game_WIDTH+870,Pad_Left,Game_HEIGHT-380,Pad_Top)
            Text_Display("• Move one of your pawns 1 square diagonally ahead if",16,screen,font, Game_WIDTH+870,Pad_Left,Game_HEIGHT-360,Pad_Top)
            Text_Display("occupied by the opponent and capture the piece",16,screen,font, Game_WIDTH+870,Pad_Left,Game_HEIGHT-340,Pad_Top)
            Text_Display("• The game is won in one of three ways:",16,screen,font, Game_WIDTH+870,Pad_Left,Game_HEIGHT-320,Pad_Top)
            Text_Display(" • Moving a pawn to the opposite end of the board",16,screen,font, Game_WIDTH+870,Pad_Left,Game_HEIGHT-300,Pad_Top)
            Text_Display("• Capturing all enemy pawns",16,screen,font, Game_WIDTH+870,Pad_Left,Game_HEIGHT-280,Pad_Top)
            Text_Display("• Achieving a position in which the enemy can't move ",16,screen,font, Game_WIDTH+870,Pad_Left,Game_HEIGHT-260,Pad_Top)
            Text_Display("•Now challenge yourself to see how many games ",16,screen,font, Game_WIDTH+870,Pad_Left,Game_HEIGHT-240,Pad_Top)
            Text_Display(" you can win before the machine becomes unbeatable",16,screen,font, Game_WIDTH+870,Pad_Left,Game_HEIGHT-220,Pad_Top)
        elif SettingsB.collidepoint((mx,my)):
            draw_text('  >',p.font.SysFont('Arial',20),(255,255,255),screen,Game_WIDTH//2-Pad_Left+20,Game_HEIGHT//2-Pad_Top+333-30)
            Text_Display("-- Credits --",20,screen,font, Game_WIDTH+870,Pad_Left,Game_HEIGHT-480,Pad_Top)
            Text_Display("*TEAM INVASION CITY* ",20,screen,font, Game_WIDTH+870,Pad_Left,Game_HEIGHT-440,Pad_Top)
            Text_Display("Avrodeep Saha",16,screen,font, Game_WIDTH+870,Pad_Left,Game_HEIGHT-420,Pad_Top)
            Text_Display("Shivam Sharma",16,screen,font, Game_WIDTH+870,Pad_Left,Game_HEIGHT-400,Pad_Top)
            Text_Display("Siddhartha Sharma",16,screen,font, Game_WIDTH+870,Pad_Left,Game_HEIGHT-380,Pad_Top)
            Text_Display("Mansi Sahu",16,screen,font, Game_WIDTH+870,Pad_Left,Game_HEIGHT-360,Pad_Top)
            
        elif QuitB.collidepoint((mx,my)):
            draw_text('  >',p.font.SysFont('Arial',20),(255,255,255),screen,Game_WIDTH//2-Pad_Left+20,Game_HEIGHT//2-Pad_Top+433-30)
            Text_Display("Exit Game?",20,screen,font, Game_WIDTH+870,Pad_Left,Game_HEIGHT-480,Pad_Top)
            Text_Display("Click to Exit",16,screen,font, Game_WIDTH+870,Pad_Left,Game_HEIGHT-460,Pad_Top)
            if click:
                quit() 

        elif AutoB.collidepoint((mx,my)):
            p.draw.line(screen, (0,255,0),(Game_WIDTH//2-170,Game_HEIGHT-50),(Game_WIDTH-766,Game_HEIGHT-50),2)
            if click and playerOne:
                playerOne = False                
            elif click and not playerOne:
                playerOne = True
        elif TwopB.collidepoint((mx,my)):
            p.draw.line(screen, (0,255,0),(Game_WIDTH//2+30,Game_HEIGHT-50),(Game_WIDTH-553,Game_HEIGHT-50),2)
            if click and not playerTwo:
                playerTwo = True
                playerOne = True 
            elif click and playerTwo:
                playerTwo = False
                # playerOne = False 

        else:
            cover1 = p.Rect(Game_WIDTH//2-Pad_Left+19,Game_HEIGHT//2-Pad_Top+130-30,30,35)
            cover2 = p.Rect(Game_WIDTH//2-Pad_Left+19,Game_HEIGHT//2-Pad_Top+230-30,30,35)
            cover3 = p.Rect(Game_WIDTH//2-Pad_Left+19,Game_HEIGHT//2-Pad_Top+330-30,30,35)
            cover4 = p.Rect(Game_WIDTH//2-Pad_Left+19,Game_HEIGHT//2-Pad_Top+430-30,30,35)
            cover5 = p.Rect(Game_WIDTH//2+250,Game_HEIGHT-650,600, 550) #Menu text window
            cover05 = p.Rect(Game_WIDTH//2+250,Game_HEIGHT-650,2, 550)
            cover005 = p.Rect(Game_WIDTH//2+650,Game_HEIGHT-650,2, 550)
            p.draw.rect(screen,(0,0,0),cover1)
            p.draw.rect(screen,(0,0,0),cover2)
            p.draw.rect(screen,(0,0,0),cover3)
            p.draw.rect(screen,(0,0,0),cover4)
            p.draw.rect(screen,(0,0,0),cover5)
            p.draw.rect(screen,(0,255,0),cover05)
            p.draw.rect(screen,(0,255,0),cover005)
        
        p.draw.line(screen, (0,255,0),(Game_WIDTH//2+250,Game_HEIGHT-650),(Game_WIDTH-300,Game_HEIGHT-650),2)
        p.draw.line(screen, (0,255,0),(Game_WIDTH//2+500,667),(Game_WIDTH-32,667),2)
        p.draw.rect(screen, (0,0,0), MainMenuB,0)
        screen.blit(MainMenu, MainMenuB)
        p.draw.rect(screen, (0, 0, 0), InstructionsB,0)
        screen.blit(Instructions, InstructionsB)
        p.draw.rect(screen, (0, 0, 0), CreditsB,0)
        screen.blit(Credits, CreditsB)
        p.draw.rect(screen, (0, 0, 0), SettingsB,0)
        screen.blit(Settings, SettingsB)
        p.draw.rect(screen, (0, 0, 0), QuitB,0)
        screen.blit(Quit, QuitB)

        
        click = False
        for event in p.event.get():
            if event.type ==  p.KEYDOWN:
                if event.key ==p.K_ESCAPE:
                    pause = False
            if event.type == p.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True    
        p.display.update()

def Text_Display(Text,size,screen,font, Game_WIDTH,Pad_Left,Game_HEIGHT,Pad_Top):
    font = p.font.SysFont("Helvetica", size, True, False)
    textObject = font.render(Text, 0, p.Color('Grey'))
    textLocation = p.Rect(Pad_Left, Pad_Top, Game_WIDTH//2-Pad_Left+19,Game_HEIGHT-150).move(Game_WIDTH // 2 - textObject.get_width() // 2-Pad_Left+19,
                                                                 Game_HEIGHT-230 - textObject.get_height()-150)
    screen.blit(textObject, textLocation)

def quit():
    p.quit()
# Game_WIDTH//2-Pad_Left+19,Game_HEIGHT-150,Game_WIDTH-380