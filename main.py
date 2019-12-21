import pygame
from pygame.locals import *
import sys
import random


class DoodleJump:

    def __init__(self):

        # создание экрана, спрайтов и шрифта
        self.screen = pygame.display.set_mode((800, 600))
        pygame.font.init()
        self.score = 0
        self.font = pygame.font.SysFont("Arial", 25)
        self.platform = pygame.image.load("data/platform.png").convert_alpha()
        self.blue = pygame.image.load("data/blue.png").convert_alpha()
        self.broken = pygame.image.load("data/broken.png").convert_alpha()
        self.broken_1 = pygame.image.load("data/broken_1.png").convert_alpha()
        self.playerRight = pygame.image.load("data/Melissa_Jump2_R.png").convert_alpha()
        self.playerRight_1 = pygame.image.load("data/Melissa_Fall2_R.png").convert_alpha()
        self.playerLeft = pygame.image.load("data/Melissa_Jump2_L.png").convert_alpha()
        self.playerLeft_1 = pygame.image.load("data/Melissa_Fall2_L.png").convert_alpha()
        self.spring = pygame.image.load("data/spring.png").convert_alpha()
        self.spring_1 = pygame.image.load("data/spring_1.png").convert_alpha()
