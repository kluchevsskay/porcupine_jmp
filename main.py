import pygame
from pygame.locals import *
import sys
import random
import os
import time

WIDTH = 480
HEIGHT = 600
FPS = 60

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Начало!")
clock = pygame.time.Clock()
font_name = pygame.font.match_font('arial')
WHITE = (255, 255, 255)


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def show_go_screen():
    theme_sound = pygame.mixer.Sound("data/sounds/theme.wav")
    theme_sound.play()
    draw_text(screen, "Начало!", 64, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, "Используйте стрелки для премещения ", 22,
              WIDTH / 2, HEIGHT / 2)
    draw_text(screen, "Нажмите на стрелку вверх и закройте", 18, WIDTH / 2, HEIGHT * 3 / 4)
    draw_text(screen, "это окно для начала игры", 18, WIDTH / 2, HEIGHT * 4 / 5)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False


class Key(pygame.sprite.Sprite):
    """ класс ключей-денег-называйтеЭтоКакХотите"""

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = pygame.image.load("data/images/key.png").convert_alpha()
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.flag_taken = False
        self.image.blit(screen, (30, 56))

    def taken(self):
        self.flag_taken = True


class Jumper:

    def __init__(self):
        """ конструктор + создание прайсов, экрана и т.д."""

        self.flag_broken = True
        self.screen = pygame.display.set_mode((800, 600))

        self.platform = pygame.image.load("data/images/platform.png").convert_alpha()

        pygame.font.init()

        # заголовок игрового окна
        pygame.display.set_caption('Porcupine_Jmp')

        # счётчик очков
        self.score = 0

        # прайсы и их изображения
        self.font = pygame.font.SysFont("Arial", 25)
        self.platform = pygame.image.load("data/images/platform.png").convert_alpha()
        self.moving = pygame.image.load("data/images/moving.png").convert_alpha()
        self.broken = pygame.image.load("data/images/broken.png").convert_alpha()
        self.broken_1 = pygame.image.load("data/images/broken_1.png").convert_alpha()
        self.playerRight = pygame.image.load("data/images/Melissa_Jump2_R.png").convert_alpha()
        self.playerRight_1 = pygame.image.load("data/images/Melissa_Fall2_R.png").convert_alpha()
        self.playerLeft = pygame.image.load("data/images/Melissa_Jump2_L.png").convert_alpha()
        self.playerLeft_1 = pygame.image.load("data/images/Melissa_Fall2_L.png").convert_alpha()
        self.spring = pygame.image.load("data/images/spring.png").convert_alpha()
        self.spring_1 = pygame.image.load("data/images/spring_1.png").convert_alpha()
        self.image_orig = pygame.image.load("data/images/key.png").convert_alpha()

        # загрузка мелодий и звуков
        self.broken_sound = pygame.mixer.Sound("data/sounds/broken.wav")
        self.gameover_sound = pygame.mixer.Sound("data/sounds/game_over.wav")
        self.spring_sound = pygame.mixer.Sound("data/sounds/spring_melody.wav")
        self.theme_sound = pygame.mixer.Sound("data/sounds/theme.wav")

        # начальное положение главного героя
        self.playerx = 400
        self.playery = 400

        # основные параметры
        self.platforms = [[400, 500, 0, 0]]
        self.springs = []
        self.keys = []
        # параметр изменения камеры по оси oY
        self.cameray = 0
        # высота прыжка
        self.jump = 0
        # параметр направления
        self.direction = 0
        # параметр гравитации (силы тяжести)
        self.gravity = 0
        # параметр горизонтального движения
        self.xmovement = 0

        self.flag_key = 0

    def updatePlayer(self):
        """ движение главного героя, изменение его образа"""

        if not self.jump:
            self.playery += self.gravity
            self.gravity += 1
        elif self.jump:
            self.playery -= self.jump
            self.jump -= 1

        key = pygame.key.get_pressed()
        if key[K_RIGHT]:
            if self.xmovement < 10:
                self.xmovement += 1

            # направление "вправо" имеет значение "0"
            self.direction = 0

        elif key[K_LEFT]:
            if self.xmovement > -10:
                self.xmovement -= 1

            # направление "влево" имеет значение "1"
            self.direction = 1
        else:

            if self.xmovement > 0:
                self.xmovement -= 1
            elif self.xmovement < 0:
                self.xmovement += 1

        if self.playerx > 850:
            self.playerx = -50
        elif self.playerx < -50:
            self.playerx = 850
        self.playerx += self.xmovement
        if self.playery - self.cameray <= 200:
            self.cameray -= 10

        # изменение персонажа в зависимости от направления и расположения
        if not self.direction:
            if self.jump:
                self.screen.blit(self.playerRight_1, (self.playerx, self.playery - self.cameray))
            else:
                self.screen.blit(self.playerRight, (self.playerx, self.playery - self.cameray))
        else:
            if self.jump:
                self.screen.blit(self.playerLeft_1, (self.playerx, self.playery - self.cameray))
            else:
                self.screen.blit(self.playerLeft, (self.playerx, self.playery - self.cameray))

    def updatePlatforms(self):
        """ обновление платформ"""

        for p in self.platforms:
            rect = pygame.Rect(p[0], p[1], self.platform.get_width() - 10, self.platform.get_height())
            player = pygame.Rect(self.playerx, self.playery, self.playerRight.get_width() - 10,
                                 self.playerRight.get_height())
            if rect.colliderect(player) and self.gravity and self.playery < (p[1] - self.cameray):
                if p[2] != 2:
                    self.jump = 15
                    self.gravity = 0
                else:
                    p[-1] = 1
            if p[2] == 1:
                if p[-1] == 1:
                    p[0] += 5
                    if p[0] > 550:
                        p[-1] = 0
                else:
                    p[0] -= 5
                    if p[0] <= 0:
                        p[-1] = 1

    def drawPlatforms(self):
        """ отображение платформ"""

        global key
        for p in self.platforms:
            check = self.platforms[1][1] - self.cameray

            # разные вероятности появление того или иного объекта
            if check > 600:
                platform = random.randint(0, 1000)
                if platform < 800:
                    platform = 0
                elif platform < 900:
                    platform = 1
                else:
                    platform = 2
                self.platforms.append([random.randint(0, 700), self.platforms[-1][1] - 50, platform, 0])
                coords = self.platforms[-1]

                check = random.randint(0, 1000)
                if check > 900 and platform == 0:
                    self.springs.append([coords[0], coords[1] - 25, 0])
                self.platforms.pop(0)
                if check > 700 and (platform == 1 or platform == 2):
                    self.keys.append([coords[0], coords[1] - 10, 0])

                # увеличение показателя счётчика очков
                self.score += 7

            # отображение основной платформы
            if p[2] == 0:
                self.screen.blit(self.platform, (p[0], p[1] - self.cameray))

            # отображение движущейся платформы
            elif p[2] == 1:
                self.screen.blit(self.moving, (p[0], p[1] - self.cameray))

            # отображение "лжеплатформы"

            elif p[2] == 2:
                if not p[3]:
                    self.flag_broken = False

                    # целая и нетронутая платформа
                    self.screen.blit(self.broken, (p[0], p[1] - self.cameray))
                else:

                    # сломанная, тк на неё запрыгнули
                    self.screen.blit(self.broken_1, (p[0], p[1] - self.cameray))
                    if not self.flag_broken:
                        self.broken_sound.play()
                        self.flag_broken = True
        # монетки
        for money in self.keys:
            self.flag_key = 0
            if money[0]:
                # несобранная монетка
                self.key_form = Key()

            # изменение счётчика очков при касании ключа
            if pygame.Rect(money[0], money[1], self.image_orig.get_width(),
                           self.image_orig.get_height()).colliderect(
                pygame.Rect(self.playerx, self.playery, self.playerRight.get_width(),
                            self.playerRight.get_height())) and self.flag_key == 0:
                self.key_form.taken()
                self.flag_key = 1

        # работа с пружинами
        for spring in self.springs:
            if spring[-1]:

                # сжатая пружина
                self.screen.blit(self.spring_1, (spring[0], spring[1] - self.cameray))
            else:

                # сработавшая пружина
                self.screen.blit(self.spring, (spring[0], spring[1] - self.cameray))

            # изменение высоты прыжка при запрыгивании на пружину
            if pygame.Rect(spring[0], spring[1], self.spring.get_width(), self.spring.get_height()).colliderect(
                    pygame.Rect(self.playerx, self.playery, self.playerRight.get_width(),
                                self.playerRight.get_height())):
                self.spring_sound.play()
                self.jump = 50
                self.cameray -= 50

    def generatePlatforms(self):
        """ генерация платформ"""

        on = 600
        while on > -100:
            x = random.randint(0, 700)
            platform = random.randint(0, 1000)
            if platform < 800:

                # основная платформа
                platform = 0
            elif platform < 900:

                # "лжеплатформа"
                platform = 1
            else:

                # движущаяся платформа
                platform = 2

            # генерация на случайной координате случайной платформы
            self.platforms.append([x, on, platform, 0])
            on -= 50

    def drawGrid(self):
        """ фон в виде клетчатой бумаги"""

        for x in range(80):
            pygame.draw.line(self.screen, (222, 222, 222), (x * 12, 0), (x * 12, 600))
            pygame.draw.line(self.screen, (222, 222, 222), (0, x * 12), (800, x * 12))

    def run(self):
        """ запуск игры"""

        clock = pygame.time.Clock()
        self.generatePlatforms()

        while True:
            # отрисовка основного экрана

            self.screen.fill((255, 255, 255))
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()

            # проверка на падение игрока
            if self.playery - self.cameray > 700:
                self.gameover_sound.play()

                # сброс к начальным параметрам
                self.cameray = 0
                self.score = 0
                self.springs = []
                self.keys = []
                self.platforms = [[400, 500, 0, 0]]
                self.generatePlatforms()
                self.playerx = 400
                self.playery = 400

            # основные действия
            self.drawGrid()
            self.drawPlatforms()
            self.updatePlayer()
            self.updatePlatforms()
            self.screen.blit(self.font.render(str(self.score), -1, (0, 0, 0)), (25, 25))
            pygame.display.flip()


game_over = True
running = True
while running:
    if game_over:
        show_go_screen()
        game_over = False
        all_sprites = pygame.sprite.Group()
        score = 0

    # Держим цикл на правильной скорости
    clock.tick(FPS)
    # Ввод процесса (события)
    for event in pygame.event.get():
        # проверка для закрытия окна
        if event.type == pygame.QUIT:
            running = False

# запуск
Jumper().run()
