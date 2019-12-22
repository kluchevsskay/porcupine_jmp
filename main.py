import pygame
from pygame.locals import *
import sys
import random

FPS = 50


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)


class DoodleJump:

    def __init__(self):
        # создание экрана, спрайтов и шрифта
        self.screen = pygame.display.set_mode((1000, 1000))
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


    def event(self, event):
        """обработка событий"""
        camera = Camera()

        # изменяем ракурс камеры
        camera.update(player)

        # обновляем положение всех спрайтов
        for sprite in all_sprites:
            camera.apply(sprite)
        if event.type == QUIT:
            sys.exit()
        # elif event.type == KEYUP:
        # if event.key == K_ESCAPE:
        # что-то делается
