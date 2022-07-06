import pygame, sys, time
from pygame.locals import *
pygame.init()

#Base class
class Crop:
    def __init__(self):
        self.cost = 0.00
        self.seeds = 0
        self.img = None
    def __eq__(self, other):
        if self.img == other.img:
            return True
        return False

#Plant for the potato
class Potato(Crop):
    def __init__(self):
        self.cost = 0.75
        self.seeds = 10
        self.img = potato
    def __hash__(self):
        return 0

class Cucumber(Crop):
    def __init__(self):
        self.cost = 0.42
        self.seeds = 15
        self.img = cucumber
    def __hash__(self):
        return 1

class Bean(Crop):
    def __init__(self):
        self.cost = 0.75
        self.seeds = 35
        self.img = bean
    def __hash__(self):
        return 2

class Tomato(Crop):
    def __init__(self):
        self.cost = 1.03
        self.seeds = 110
        self.img = tomato
    def __hash__(self):
        return 3

class Zuchinni(Crop):
    def __init__(self):
        self.cost = 1.20
        self.seeds = 44
        self.img = zuchinni
    def __hash__(self):
        return 4

class Seeds:
    def __init__(self):
        self.potatoSeeds = 0
        self.beanSeeds = 0
        self.tomatoSeeds = 0
        self.cucumberSeeds = 0
        self.zuchinniSeeds = 0
        self.typeDict = {Potato():self.potatoSeeds, 
                Bean():self.beanSeeds, 
                Tomato():self.tomatoSeeds, 
                Cucumber():self.cucumberSeeds, 
                Zuchinni():self.zuchinniSeeds}
    def update(self):
        self.typeDict = {Potato():self.potatoSeeds, 
                Bean():self.beanSeeds, 
                Tomato():self.tomatoSeeds, 
                Cucumber():self.cucumberSeeds, 
                Zuchinni:self.zuchinniSeeds}
    def add_seeds (self, Type, added):
        if Type == Potato():
            self.potatoSeeds += added
        if Type == Bean():
            self.beanSeeds += added
        if Type == Tomato():
            self.tomatoSeeds += added
        if Type == Cucumber():
            self.cucumberSeeds += added
        if Type == Zuchinni():
            self.zuchinniSeeds += added
    def get_type (self, Type):
        self.update()
        for plant in self.typeDict.keys():
            if plant == Type:
                return self.typeDict[plant]
        return False

#Empty Land for more crops
class Land(Crop):
    def __init__(self):
        super().__init__()
        self.img = grass

#Set up text
font = pygame.font.Font(None, 50)

#Load images
grass = pygame.image.load("Grass.png")
potato = pygame.image.load("Potato.png")
bean = pygame.image.load("Bean.png")
tomato = pygame.image.load("Tomato.png")
cucumber = pygame.image.load("Cucumber.png")
zuchinni = pygame.image.load("Zuchinni.png")
bg = pygame.image.load("Background.png")
BuyLand = pygame.image.load("BuyLand.png")
potatoSeed = pygame.image.load("PotatoSeed.png")
beanSeed = pygame.image.load("BeanSeed.png")
tomatoSeed = pygame.image.load("TomatoSeed.png")
cucumberSeed = pygame.image.load("CucumberSeed.png")
zuchinniSeed = pygame.image.load("ZuchinniSeed.png")
Seed = pygame.image.load("Seed.png")
store = pygame.image.load("Store.png")
ShopTemplate = pygame.image.load("ShopTemplate.png")
ShopLayer = pygame.image.load("ShopLayer.png")

#Set up canvas
canvas = pygame.display.set_mode((1360, 660))
pygame.display.set_caption("!Potatoes!")

#Variables to setup
yellow = (200, 200, 0)

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
    GrowingPotatoes = []
    SellOrBuy = False
    seeds = Seeds()
    NumSellSeeds = False
    sellseeds = 0
    SeedSelectType = Potato()
    Storemode = False

    #Time
    #2 second = one day(relatively)
    #30 days = one month
    #12 months = one year
    #You get one year(720 seconds) to return your money
    borrowtime = 0
    NotEnoughMoneyMsg = False
    Borrowing = False
    BorrowingMessage = False
    LoseFarmMsg = False
    borrowedval = 0 
    interest = 10
    AlreadyBorrowingMsg = False

    while True:
        #Basic Images that need to be placed
        canvas.fill((255, 255, 255))
        canvas.blit(bg, (0, 100))
        canvas.blit(BuyLand, (0, 0))
        text = font.render("$" + str(money), True, yellow, None)
        canvas.blit(text, (0, 50))
        canvas.blit(store, (1060, 0))
        canvas.blit(potatoSeed, (200, 0))
        canvas.blit(beanSeed, (350, 0))
        canvas.blit(tomatoSeed, (500, 0))
        canvas.blit(cucumberSeed, (650, 0))
        canvas.blit(zuchinniSeed, (800, 0))
        if Storemode:
            canvas.blit(ShopLayer, (600, 330))
            canvas.blit(potatoSeed, (605, 335))
            canvas.blit(beanSeed, (655, 335))
            canvas.blit(tomatoSeed, (705, 335))
            canvas.blit(cucumberSeed, (605, 390))
            canvas.blit(zuchinniSeed, (655, 390))
            canvas.blit(ShopTemplate, (600, 330))
        potatotext = font.render(str(seeds.potatoSeeds), True, yellow, None)
        beantext = font.render(str(seeds.beanSeeds), True, yellow, None)
        tomatotext = font.render(str(seeds.tomatoSeeds), True, yellow, None)
        cucumbertext = font.render(str(seeds.cucumberSeeds), True, yellow, None)
        zuchinnitext = font.render(str(seeds.zuchinniSeeds), True, yellow, None)
        canvas.blit(potatotext, (250, 0))
        canvas.blit(beantext, (400, 0))
        canvas.blit(tomatotext, (550, 0))
        canvas.blit(cucumbertext, (700, 0))
        canvas.blit(zuchinnitext, (850, 0))
        if time.time() - borrowtime > 720:
            if Borrowing:
                farm = [[Potato()]]
                money = 0
                LoseFarmMsg = True
                BorrowingMessage = False
                AskBorrow = False
                AskDismiss = False
                money += (seeds.potatoSeeds + seeds.beanSeeds + seeds.tomatoSeeds + seeds.cucumberSeeds + seeds.zuchinniSeeds) * 0.25
                seeds.potatoSeeds = 0
                seeds.beanSeeds = 0
                seeds.tomatoSeeds = 0
                seeds.cucumberSeeds = 0
                seeds.zuchinni = 0
                GrowingPotatoes = []
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
                    AlreadyBorrowingMsg = False
                    NotEnoughMoneyMsg = False
                if event.key == K_b:
                    AskDismiss = False
                    BorrowingMessage = False
                    if not Borrowing:
                        AskBorrow = True
                        AlreadyBorrowingMsg = False
                    else:
                        AlreadyBorrowingMsg = True
                        AskBorrow = False
                if event.key == K_r and Borrowing:
                    if money >= borrowedval * 1.1:
                        Borrowing = False
                        AskBorrow = False
                        AlreadyBorrowingMsg = False
                        money -= borrowedval * 1.1
                    else:
                        NotEnoughMoneyMsg = True
                if event.key == K_s:
                    PlantingMode = False
                    NumSellSeeds = True
                    SellOrBuy = False
                if event.key == K_p:
                    PlantingMode = True
                    NumSellSeeds = False
                    SellOrBuy = False
                if event.key == K_0:
                    if AskBorrow:
                        borrowval *= 10
                    if NumSellSeeds:
                        sellseeds *= 10
                if event.key == K_1:
                    if AskBorrow:
                        borrowval *= 10
                        borrowval += 1
                    if NumSellSeeds:
                        sellseeds *= 10
                        sellseeds += 1
                if event.key == K_2:
                    if AskBorrow:
                        borrowval *= 10
                        borrowval += 2
                    if NumSellSeeds:
                        sellseeds *= 10
                        sellseeds += 2
                if event.key == K_3:
                    if AskBorrow:
                        borrowval *= 10
                        borrowval += 3
                    if NumSellSeeds:
                        sellseeds *= 10
                        sellseeds += 3
                if event.key == K_4:
                    if AskBorrow:
                        borrowval *= 10
                        borrowval += 4
                    if NumSellSeeds:
                        sellseeds *= 10
                        sellseeds += 4
                if event.key == K_5:
                    if AskBorrow:
                        borrowval *= 10
                        borrowval += 5
                    if NumSellSeeds:
                        sellseeds *= 10
                        sellseeds += 5
                if event.key == K_6:
                    if AskBorrow:
                        borrowval *= 10
                        borrowval += 6
                    if NumSellSeeds:
                        sellseeds *= 10
                        sellseeds += 6
                if event.key == K_7:
                    if AskBorrow:
                        borrowval *= 10
                        borrowval += 7
                    if NumSellSeeds:
                        sellseeds *= 10
                        sellseeds += 7
                if event.key == K_8:
                    if AskBorrow:
                        borrowval *= 10
                        borrowval += 8
                    if NumSellSeeds:
                        sellseeds *= 10
                        sellseeds += 8
                if event.key == K_9:
                    if AskBorrow:
                        borrowval *= 10
                        borrowval += 9
                    if NumSellSeeds:
                        sellseeds *= 10
                        sellseeds += 9
                if event.key == K_RETURN:
                    if AskBorrow:
                        if borrowval != 0:
                            money += borrowval
                            borrowtime = time.time()
                            borrowedval = borrowval
                            Borrowing = True
                            BorrowingMessage = True
                            AskBorrow = False
                            AskDismiss = False
                            AlreadyBorrowingMsg = False
                            WeightedVal = 1/10
                            borrowval = 0
                        else:
                            BorrowingMessage = False
                            AskBorrow = False
                            AskDismiss = False
                            AlreadyBorrowingMsg = False
                            borrowval = 0
                            WeightedVal = 1/10
                    if NumSellSeeds:
                        if sellseeds != 0:
                            if sellseeds <= seeds.get_type(SeedSelectType):
                                money += 0.25 * sellseeds
                                seeds.add_seeds(SeedSelectType, -sellseeds)
                                sellseeds = 0
                            else:
                                print (-seeds.get_type(SeedSelectType))
                                money += 0.25 * seeds.get_type(SeedSelectType)
                                seeds.add_seeds(SeedSelectType, -seeds.get_type(SeedSelectType))
                                sellseeds = 0
                        NumSellSeeds = False
                        AskBorrow = False
                        AskDismiss = False
                        BorrowingMessage = False
                        AlreadyBorrowingMsg = False
                            
                            
                if event.key == K_q:
                    if AskBorrow:
                        AskBorrow = False
                        borrowval = 0
                    if SellOrBuy:
                        SellOrBuy = False
                    if NumSellSeeds:
                        NumSellSeeds = False
                        sellseeds = 0

            #If the user presses the mouse
            if event.type == MOUSEBUTTONDOWN:
                mpos = pygame.mouse.get_pos()

                #User wants to buy land
                if pygame.Rect(0, 0, 200, 50).collidepoint(mpos):
                    if money < 1:
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
                        money -= 1
                elif pygame.Rect(1060, 0, 300, 100).collidepoint(mpos):
                    Storemode = not Storemode
                elif pygame.Rect(200, 0, 50, 50).collidepoint(mpos) and seeds.potatoSeeds != 0:
                    SellOrBuy = True
                    SeedSelectType = Potato()
                elif pygame.Rect(350, 0, 50, 50).collidepoint(mpos) and seeds.beanSeeds != 0:
                    SellOrBuy = True
                    SeedSelectType = Bean()
                elif pygame.Rect(500, 0, 50, 50).collidepoint(mpos) and seeds.tomatoSeeds != 0:
                    SellOrBuy = True
                    SeedSelectType = Tomato()
                elif pygame.Rect(650, 0, 50, 50).collidepoint(mpos) and seeds.cucumberSeeds != 0:
                    SellOrBuy = True
                    SeedSelectType = Cucumber()
                elif pygame.Rect(800, 0, 50, 50).collidepoint(mpos) and seeds.zuchinniSeeds != 0:
                    SellOrBuy = True
                    SeedSelectType = Zuchinni()
                elif Storemode:
                    #canvas.blit(potatoSeed, (605, 335))
                    #canvas.blit(beanSeed, (655, 335))
                    #canvas.blit(tomatoSeed, (705, 335))
                    #canvas.blit(cucumberSeed, (605, 390))
                    #canvas.blit(zuchinniSeed, (655, 390))
                    if pygame.Rect(40, 40, 605, 335).collidepoint(mpos) and money >= 1:
                        seeds.potatoSeeds += 1
                        money -= 1
                    if pygame.Rect(40, 40, 655, 335).collidepoint(mpos) and money >= 3000:
                        seeds.beanSeeds += 1
                        money -= 3000
                    if pygame.Rect(40, 40, 705, 335).collidepoint(mpos) and money >= 3000:
                        seeds.tomatoSeeds += 1
                        money -= 3000
                    if pygame.Rect(40, 40, 605, 390).collidepoint(mpos) and money >= 3000:
                        seeds.cucumberSeeds += 1
                        money -= 3000
                    if pygame.Rect(40, 40, 655, 390).collidepoint(mpos) and money >= 3000:
                        seeds.zuchinniSeeds += 1
                        money -= 3000 
                else:
                    gpos = (int(mpos[0] / 50), (int(mpos[1] / 50)) - 2) #Grid Position
                    if len(farm) > gpos[0] and len(farm[gpos[0]]) > gpos[1]:
                        OccupiedLand = False
                        for land in GrowingPotatoes:
                            if land[2] == [gpos[0], gpos[1]]:
                                OccupiedLand = True
                        if len(GrowingPotatoes) == 0:
                            OccupiedLand = False
                        if farm[gpos[0]][gpos[1]].cost != 0: #Make sure it isn't plain land for selling
                            money += farm[gpos[0]][gpos[1]].cost
                            if farm[gpos[0]][gpos[1]].img != None:
                                seeds.add_seeds(farm[gpos[0]][gpos[1]], farm[gpos[0]][gpos[1]].seeds)
                            farm[gpos[0]][gpos[1]] = Land()
                        elif not OccupiedLand and seeds.get_type(SeedSelectType) > 0:
                            GrowingPotatoes.append([SeedSelectType, time.time(), [gpos[:][0], gpos[:][1]]])
                            #Right now, Potato is the only vegetable
                            seeds.add_seeds(SeedSelectType, -1)

        #Display loop
        for x in range(len(farm)):
            for y in range(len(farm[x])):
                canvas.blit(grass, (x * 50, y * 50 + 100))
                canvas.blit(farm[x][y].img, (x * 50, y * 50 + 100))
        deleteIndexes = []
        #Growing Loop
        for land in range(len(GrowingPotatoes)):
            if time.time() - GrowingPotatoes[land][1] >= 60:
                farm[GrowingPotatoes[land][2][0]][GrowingPotatoes[land][2][1]] = GrowingPotatoes[land][0]
                deleteIndexes.append(land)
        for index in deleteIndexes:
            del GrowingPotatoes[index]

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

        if AlreadyBorrowingMsg:
            text = font.render("You are already borrowing money. Therefore, you cannot borrow more money", True, yellow, None)
            text2 = font.render("Press d to dismiss", True, yellow, None)
            canvas.blit(text, (50, 330))
            canvas.blit(text, (50, 330))
            canvas.blit(text2, (50, 380))
        if SellOrBuy:
            text = font.render("Would you like to sell, or plant these seeds?", True, yellow, None)
            text2 = font.render("Press s to sell, p to plant, or q to quit this message ", True, yellow, None)
            canvas.blit(text, (50, 330))
            canvas.blit(text2, (50, 380))

        if NumSellSeeds:
            text = font.render("How many seeds would you like to sell?", True, yellow, None)
            text2 = font.render("___________________________________________", True, yellow, None)
            text3 = font.render(str(sellseeds), True, yellow, None)
            canvas.blit(text, (50, 330))
            canvas.blit(text2, (50, 380))
            canvas.blit(text3, (50, 380))

        if NotEnoughMoneyMsg:
            text = font.render("You do not have enough money to return this money.", True, yellow, None)
            text2 = font.render("You must earn more money. Press d to dismiss", True, yellow, None)
            canvas.blit(text, (50, 330))
            canvas.blit(text2, (50, 380))

        #A query asking how much money the user wants to borrow
        #Update screen
        pygame.display.update()
main()
