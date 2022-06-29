#ADD GITHUB
#+ Start off with one square of land with Potatoes
#+ You can buy land
#+ Borrow money
#+ Harvest your potatoes.
#+ Sell potatoes(and other plants)
#- Sell seeds
#- And get more types of plants, such as
#   - Cucumbers
#   - Beans
#   - Tomatoes
#   - Zucchini
#- These plants give:(items)

import pygame, sys, time
from pygame.locals import *
pygame.init()

#Base class
class Crop:
    def __init__(self):
        self.cost = 0.00
        self.seeds = 0
        self.newplants = 0
        self.img = None

#Plant for the potato
class Potato(Crop):
    def __init__(self):
        self.cost = 0.75
        self.seeds = 300
        self.newplants = 5
        self.img = potato

#Empty Land for more crops
class Land(Crop):
    def __init__(self):
        self.img = grass

#Set up text
font = pygame.font.Font(None, 50)

#Load images
grass = pygame.image.load("Grass.png")
potato = pygame.image.load("Potato.png")
bg = pygame.image.load("Background.png")
BuyLand = pygame.image.load("BuyLand.png")

#Set up canvas
canvas = pygame.display.set_mode((1360, 660))
pygame.display.set_caption("!Potatoes!")

#Variables to setup
yellow = (255, 255, 0)

#Errors
ERR1 = "ERR1 : This feature is not available"

#Main loop
def main():
    #Some variables that are annoying and need to be here
    money = 0
    AskDismiss = False
    AskBorrow = False
    borrowval = 0
    farm = [[Potato()]]


    #Time
    #2 second = one day(relatively)
    #30 days = one month
    #12 months = one year
    #You get one year(720 seconds) to return your money
    borrowtime = 0
    Borrowing = False
    BorrowingMessage = False
    LoseFarmMsg = False
    borrowedval = 0 
    interest = 10
    potatoSeeds = 0

    while True:
        #Basic Images that need to be placed
        canvas.fill((255, 255, 255))
        canvas.blit(bg, (0, 100))
        canvas.blit(BuyLand, (0, 0))
        text = font.render("$" + str(money), True, yellow, None)
        canvas.blit(text, (0, 50))
        if time.time() - borrowtime > 720 and Borrowing:
            farm = [[Potato()]]
            money = 0
            LoseFarmMsg = True
            BorrowingMessage = False
            AskBorrow = False
            AskDismiss = False
            for x in range(len(farm)):
                for y in range(len(farm[x])):
                    money += farm[y][x].cost
        #Event loop
        for event in pygame.event.get():

            #If the user wants to quit the window
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            #If the user presses a key
            if event.type == KEYDOWN:
                if event.key == K_d:
                    AskDismiss = False
                    BorrowingMessage = False
                    LoseFarmMsg = False
                if event.key == K_b:
                    AskDismiss = False
                    BorrowingMessage = False
                    if not Borrowing:
                        AskBorrow = True
                if event.key == K_0:
                    if AskBorrow:
                        borrowval *= 10
                if event.key == K_1:
                    if AskBorrow:
                        borrowval *= 10
                        borrowval += 1
                if event.key == K_2:
                    if AskBorrow:
                        borrowval *= 10
                        borrowval += 2
                if event.key == K_3:
                    if AskBorrow:
                        borrowval *= 10
                        borrowval += 3
                if event.key == K_4:
                    if AskBorrow:
                        borrowval *= 10
                        borrowval += 4
                if event.key == K_5:
                    if AskBorrow:
                        borrowval *= 10
                        borrowval += 5
                if event.key == K_6:
                    if AskBorrow:
                        borrowval *= 10
                        borrowval += 6
                if event.key == K_7:
                    if AskBorrow:
                        borrowval *= 10
                        borrowval += 7
                if event.key == K_8:
                    if AskBorrow:
                        borrowval *= 10
                        borrowval += 8
                if event.key == K_9:
                    if AskBorrow:
                        borrowval *= 10
                        borrowval += 9
                if event.key == K_RETURN:
                    if AskBorrow:
                        if borrowval != 0:
                            money += borrowval
                            borrowtime = time.time()
                            borrowedvals = borrowval
                            Borrowing = True
                            BorrowingMessage = True
                            AskBorrow = False
                            AskDismiss = False
                            WeightedVal = 1/10
                            borrowval = 0
                        else:
                            BorrowingMessage = False
                            AskBorrow = False
                            AskDismiss = False
                            borrowval = 0
                            WeightedVal = 1/10
                if event.key == K_q:
                    if AskBorrow:
                        AskBorrow = False
                        borrowval = 0

            #If the user presses the mouse
            if event.type == MOUSEBUTTONDOWN:
                mpos = pygame.mouse.get_pos()

                #User wants to buy land
                if pygame.Rect(0, 0, 200, 50).collidepoint(mpos):
                    if money < 850:
                        AskDismiss = True
                    else:
                        if len(farm) < 27:
                            farm.append([Land()])
                        else:
                            exited = False
                            for x in range(27):
                                if len(farm[x]) == len(farm[-1]):
                                    exited = True
                                    farm[x].append(Land())
                                    break
                            if not exited:
                                farm[-1].append(Land())
                        money -= 850
                else:
                    gpos = (int(mpos[0] / 50), (int(mpos[1] / 50)) - 2) #Grid Position
                    print (gpos)
                    if len(farm) > gpos[0] and len(farm[gpos[0]]) > gpos[1]:
                        if farm[gpos[0]][gpos[1]].cost != 0: #Make sure it isn't plain land for selling
                            money += farm[gpos[1]][gpos[0]].cost
                            farm[gpos[1]][gpos[0]] = Land()

        #Display loop
        for x in range(len(farm)):
            for y in range(len(farm[x])):
                canvas.blit(grass, (x * 50, y * 50 + 100))
                canvas.blit(farm[x][y].img, (x * 50, y * 50 + 100))

        #A query asking whether or not the user wants to borrow money or dismiss the query
        if AskDismiss:
            text = font.render("You do not have enough money to buy more land", True, yellow, None)
            text2 = font.render("Would you like to borrow some money from the bank?", True, yellow, None)
            text3 = font.render("If yes, press b(orrow), otherwise, press d(ismiss)", True, yellow, None)
            canvas.blit (text, (50, 330))
            canvas.blit (text2, (50, 380))
            canvas.blit (text3, (50, 420))
        #A query asking how much money the user wants to borrow
        if AskBorrow:
            text = font.render("How much money would you like to borrow?", True, yellow, None)
            text2 = font.render("________________________________________", True, yellow, None)
            text3 = font.render(str(borrowval), True, yellow, None)
            canvas.blit(text, (50, 330))
            canvas.blit(text2, (50, 380))
            canvas.blit(text3, (50, 380))
        #A message telling that you have to return your money in a year(if you borrow)
        if BorrowingMessage:
            text = font.render("You have one year to return your money with 10 percent interest", True, yellow, None)
            text2 = font.render("Press d to dismiss", True, yellow, None)
            canvas.blit(text, (50, 330))
            canvas.blit(text2, (50, 380))

        if LoseFarmMsg:
            text = font.render("You have failed to return your money with 10 percent interest", True, yellow, None)
            text2 = font.render("You will lose your farm and all your", True, yellow, None) 
            text3 = font.render("Plants will be sold. Press d to dismiss.", True, yellow, None)
            canvas.blit(text, (50, 330))
            canvas.blit(text2, (50, 380))
            canvas.blit(text3, (50, 420))


        #A query asking how much money the user wants to borrow
        #Update screen
        pygame.display.update()
main()
