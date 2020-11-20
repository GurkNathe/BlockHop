import pygame, sys
from Player import Player
from Back import Back
from Platforms import Platforms

#Level selector made from https://stackoverflow.com/questions/31753910/python-pygame-level-select-pages
pygame.init()

display_width = 800
display_height = 600

white = (255,255,255)
black = (0,0,0)
grey = (128,128,128)
red = (175,0,0)
green = (34,177,76)
yellow = (175,175,0)
blue = (30,144,255)
light_green = (0,255,0)
light_red = (255,0,0)
light_yellow = (255,255,0)
light_blue = (0,191,255)
light_grey = (200,200,200)

smallFont = pygame.font.SysFont("timesnewroman", 20)
medFont = pygame.font.SysFont("timesnewroman", 45)
largeFont = pygame.font.SysFont("castellar", 55)

FPS = 20
FramePerSec = pygame.time.Clock()

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Block Hop")

pygame.display.flip()

def text_objects(text, color, size):
    if size == "small":
        textSurf = smallFont.render(text, True, color)
    elif size == "medium":
        textSurf = medFont.render(text, True, color)
    elif size == "large":
        textSurf = largeFont.render(text, True, color)

    return textSurf, textSurf.get_rect()


def messageToScreen(msg, color, y_displace = 0, size = "small"):
    textSurface, textRect = text_objects(msg, color, size)
    textRect.center = (display_width/2), (display_height/2) + y_displace
    gameDisplay.blit(textSurface, textRect)

def text_to_button(msg, color, buttonX, buttonY, buttonWidth, buttonHeight, size = "small"):
    textSurface, textRect = text_objects(msg, color, size)
    textRect.center = ((buttonX + (buttonWidth/2), buttonY + (buttonHeight/2)))
    gameDisplay.blit(textSurface, textRect)

def button(text, x, y, width, height, inactiveColor , activeColor, textColor = black, action = None):
    cur = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x+ width > cur[0] > x and y + height > cur[1] > y:
        pygame.draw.rect(gameDisplay, activeColor, (x,y,width,height))
        if click[0] == 1 and action != None:
            if action == "quit":
                pygame.quit()
            if action == "directions":
                gameDisplay.fill(white)
                pygame.display.update()
                directions()
            if action == "lvl":
                gameDisplay.fill(white)
                pygame.display.update()
                levelScreen()
            if action == "main":
                gameDisplay.fill(white)
                pygame.display.update()
                startScreen()
            if action == "lvl1":
                gameDisplay.fill(white)
                pygame.display.update()
                game("./levels/level1.txt")
            elif action == "lvl2":
                gameDisplay.fill(white)
                pygame.display.update()
                game("./levels/level2.txt")
            elif action == "lvl3":
                gameDisplay.fill(white)
                pygame.display.update()
                game("./levels/level3.txt")
            elif action == "lvl4":
                gameDisplay.fill(white)
                pygame.display.update()
                game("./levels/level4.txt")
            elif action == "lvl5":
                gameDisplay.fill(white)
                pygame.display.update()
                game("./levels/level5.txt")
            elif action == "lvl6":
                gameDisplay.fill(white)
                pygame.display.update()
                game("./levels/level6.txt")
            elif action == "lvl7":
                gameDisplay.fill(white)
                pygame.display.update()
                game("./levels/level7.txt")
            elif action == "lvl8":
                gameDisplay.fill(white)
                pygame.display.update()
                game("./levels/level8.txt")
            elif action == "lvl9":
                gameDisplay.fill(white)
                pygame.display.update()
                game("./levels/level9.txt")
            elif action == "lvl10":
                gameDisplay.fill(white)
                pygame.display.update()
                game("./levels/level10.txt")
            elif action == "lvl11":
                gameDisplay.fill(white)
                pygame.display.update()
                game("./levels/level11.txt")
            elif action == "lvl12":
                gameDisplay.fill(white)
                pygame.display.update()
                game("./levels/level12.txt")

    else:
        pygame.draw.rect(gameDisplay, inactiveColor, (x,y,width,height))

    text_to_button(text,textColor,x,y,width,height)
    
#getting platforms form level file
def get_level(background, level, P1):
    with open(level) as test:
        lines = test.readlines()
        for line in lines:
            plat_type, x_size, y_size, x_coord, y_coord = line.split(" ")
            background.add(Platforms(int(plat_type),
                                    int(x_size),
                                    int(y_size),
                                    int(y_coord),
                                    int(x_coord),
                                    P1))
    return background
    
#Handles keeping the window open and running, and when to close window
def game(level):
    background = pygame.sprite.Group()
    P1 = Player(display_width, display_height, 200, "./images/Players/block.png", background, level)
    background = get_level(background, level, P1)
    back = Back(display_width, display_height)
    while(True):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif pygame.key.get_pressed()[pygame.K_ESCAPE]:
                gameDisplay.fill(white)
                pygame.display.update()
                levelScreen()
                break;
            elif P1.goal:
                gameDisplay.fill(white)
                pygame.display.update()
                winScreen()
                break;
                
        
        P1.spaced()
        P1.jump()
        P1.update()
        
        back.draw(gameDisplay)
        background.draw(gameDisplay)
        P1.draw(gameDisplay)
        
        pygame.display.update()
        FramePerSec.tick(FPS)

def winScreen():
    win = True
    
    while win:
        messageToScreen("You Completed the Level!", black, 0, size = "medium")
        messageToScreen("Press ESC to go back to level selector.", black, -40, size = "small")
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                win = False
                pygame.quit()
                sys.exit()
            elif pygame.key.get_pressed()[pygame.K_ESCAPE]:
                win = False
                gameDisplay.fill(white)
                pygame.display.update()
                levelScreen()
                break;

def levelScreen():
    level = True

    while level:
        global levelnumber
        levelnumber = 1 
        gameDisplay.fill(white)
        messageToScreen("Level Select", black, -200, size = "large")
        button("Level 1", 185, 150, 100, 50, (0, 128, 0), (0, 64, 0), action = "lvl1")
        button("Level 2", 295, 150, 100, 50, (0, 128, 0), (0, 64, 0), action = "lvl2")
        button("Level 3", 405, 150, 100, 50, (100, 160, 0), (50, 80, 0), action = "lvl3")
        button("Level 4", 515, 150, 100, 50, (100, 160, 0), (50, 80, 0), action = "lvl4")
        button("Level 5", 185, 270, 100, 50, (160, 200, 0), (50, 80, 0), action = "lvl5")
        button("Level 6", 295, 270, 100, 50, (160, 200, 0), (50, 80, 0), action = "lvl6")
        button("Level 7", 405, 270, 100, 50, (200, 200, 0), (100, 100, 0), action = "lvl7")
        button("Level 8", 515, 270, 100, 50, (244, 232, 104), (120, 110, 70), action = "lvl8")
        button("Level 9", 185, 390, 100, 50, (255, 220, 0), (130, 110, 0), action = "lvl9")
        button("Level 10", 295, 390, 100, 50, (255, 200, 0), (130, 100, 0), action = "lvl10")
        button("Level 11", 405, 390, 100, 50, (255, 100, 0), (130, 50, 0), action = "lvl11")
        button("Level 12", 515, 390, 100, 50, (255, 0, 0), (130, 0, 0), action = "lvl12")
        button("Back", 200, 500, 150, 50, light_blue, blue, action = "main")
        button("Quit", 450, 500, 150, 50, light_blue, blue, action = "quit")
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                level = False
                pygame.quit()
            elif pygame.key.get_pressed()[pygame.K_ESCAPE]:
                level = False
                gameDisplay.fill(white)
                pygame.display.update()
                startScreen()

def directions():
    directions = True

    while directions:

        gameDisplay.fill(white)
        messageToScreen("Directions", black, -200, size = "large")
        messageToScreen("To move character, use ← and → keys for side-to-side movement.", black, -160)
        messageToScreen("To jump, use ↑ or space bar.", black, -130)
        messageToScreen("There are red platforms, if you land on them, you will die.", black, -100)
        messageToScreen("If you jump/fall off diagonally on platforms there's a chance you'll teleport to a place nearby.", black, -70)
        messageToScreen("This could be in a platform, under a platform, or at another platform.", black, -40)
        messageToScreen("If you jump and hit your head on a platform a good distance above, you will fall to your death.", black, -10)
        messageToScreen("If you die on a level, you will be sent back to the start.", black, 20)
        messageToScreen("To go back to level selector, press the escape key.", black, 50)
        messageToScreen("Your goal is to jump across the platforms avoiding the obstacles and reaching the goal.", black, 80)
        messageToScreen("Have Fun!!!", blue, 140, size = "medium")
        button("Back", 150, 500, 150, 50, light_blue, blue, action = "main")
        button("Quit", 550, 500, 150, 50, light_blue, blue, action = "quit")
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                directions = False
                pygame.quit()
            elif pygame.key.get_pressed()[pygame.K_ESCAPE]:
                directions = False
                gameDisplay.fill(white)
                pygame.display.update()
                startScreen()


def startScreen():

    game = True
    while game:
        gameDisplay.fill(white)

        messageToScreen("Block Hop", black, -100, size = "large")
        button("Level Select",150, 300,150,50, light_blue, blue, action = "lvl")
        button("Directions",350, 300,150,50, light_blue, blue, action = "directions")
        button("Quit Game",550, 300,150,50, light_blue, blue, action = "quit")

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
                game = False
                pygame.quit()
startScreen()