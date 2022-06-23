import pygame
from pygame.locals import *

#Base class
class Plant:
    def __init__(self):
        self.cost = 0.00
        self.seeds = 0
        self.newplants = 0

#Plant for the potato
class Potato(Plant):
    def __init__(self):
        self.cost = 0.75
        self.seeds = 300
        self.newplants = 5

#Load images
Grass = pygame.image.load("Grass.png")
Potato = pygame.image.load("Potato.png")

#Variables to setup
farm = [[Potato()]]

#Main loop
def main():
    while True:
        pass

