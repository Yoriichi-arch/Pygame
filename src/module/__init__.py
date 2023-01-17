import pygame
import sys
import os
from src.module.cube import Cube


left = 1000 // 2 - 630 // 2
top = 700 // 2 - 630 // 2
all_sprites_rect = pygame.sprite.Group()


def load_image(name, colorkey=None):
    fullname = os.path.join('../resources', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Barrier(pygame.sprite.Sprite):
    image = load_image('barrier.png')

    def __init__(self, x, y):
        super().__init__(all_sprites_rect)
        self.image = Barrier.image
        self.image = pygame.transform.scale(self.image, (70, 70))
        self.rect = self.image.get_rect(left=x, top=y)
        self.mask = pygame.mask.from_surface(self.image)

    def get_coords_cube(self):
        x = self.rect.x
        y = self.rect.y
        coords = (x, y)
        return coords


border_left = pygame.sprite.Sprite()
border_left.image = pygame.Surface([1, 630])
border_left.image.fill(pygame.Color('white'))
border_left.rect = border_left.image.get_rect(left=left, top=top)
border_left.mask = pygame.mask.from_surface(border_left.image)

border_top = pygame.sprite.Sprite()
border_top.image = pygame.Surface([630, 1])
border_top.image.fill(pygame.Color('white'))
border_top.rect = border_top.image.get_rect(left=left, top=top)
border_top.mask = pygame.mask.from_surface(border_left.image)

border_right = pygame.sprite.Sprite()
border_right.image = pygame.Surface([1, 630])
border_right.image.fill(pygame.Color('white'))
border_right.rect = border_right.image.get_rect(left=left + 560, top=top)
border_right.mask = pygame.mask.from_surface(border_left.image)

border_down = pygame.sprite.Sprite()
border_down.image = pygame.Surface([630, 1])
border_down.image.fill(pygame.Color('white'))
border_down.rect = border_down.image.get_rect(left=left, top=top + 560)
border_down.mask = pygame.mask.from_surface(border_left.image)

spisok = [border_left.rect, border_top.rect, border_right.rect, border_down.rect]


class Board:
    # создание поля
    def __init__(self, filename):
        x, y = 70, 70
        self.list_coordinates = []
        for i in range(10):
            s = []
            for j in range(10):
                s.append((x * j + 185, y * i + 35))
            self.list_coordinates.append(s)
        self.slovar = {}
        self.filename = filename
        # читаем уровень, убирая символы перевода строки
        with open(filename, 'r') as mapFile:
            level_map = [line.strip() for line in mapFile]
        # и подсчитываем максимальную длину
        max_width = max(map(len, level_map))
        # дополняем каждую строку пустыми клетками ('.')
        self.level = list(level_map)
        n = 0
        # создаём словарь с символами и их координатами
        for (i, j) in zip(self.list_coordinates, level_map):
            for (g, h) in zip(i, j):
                self.slovar[str(g)] = h

    def generate_level(self, surface, left, top):
        for y in range(len(self.level)):
            for x in range(len(self.level[y])):
                if self.level[y][x] == '#':
                    barrier = Barrier(left + 70 * x, top + 70 * y)
                    screen.blit(barrier.image, barrier.rect)

    def slov(self):
        return self.slovar


def terminate():
    pygame.quit()
    sys.exit()


def check_click(x, y, width, height, position):
    if x <= position[0] <= x + width and y <= position[1] <= y + height:
        return True


# заставка
def start_screen(screen, width1, height1):
    mem = load_image('meme.png')
    mem = pygame.transform.scale(mem, (300, 300))
    flag = False
    screen.fill('#3FC1C9')
    font = pygame.font.Font('../resources/Montserrat-Light.ttf', 30)
    text = font.render('Раскраска головоломка', False, '#323232')
    screen.blit(text, (1000 // 2 - text.get_width() // 2, 100))
    text = font.render('Старт', False, '#323232')
    width = 200
    height = 60
    x = 1000 // 2 - width // 2
    y = 700 // 2 - height // 2
    x1 = 1000 // 2 - 210 // 2
    y1 = 700 // 2 - 70 // 2
    pygame.draw.rect(screen, '#323232', (x1, y1 - 90, width + 10, height + 10))
    pygame.draw.rect(screen, '#14FFEC', (x, y - 90, width, height))
    screen.blit(mem, ((width1 // 2) - (300 // 2), 350))
    screen.blit(text, (x + (width - text.get_width()) // 2, (y + (height - text.get_height()) // 2) - 90))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                flag = True
                if flag and check_click(x, y, width, height, event.pos):
                    pygame.draw.rect(screen, '#323232', (x1, y1, width + 10, height + 10))
                    pygame.draw.rect(screen, '#0D7377', (x, y, width, height))
                    screen.blit(text, (x + (width - text.get_width()) // 2,
                                       y + (height - text.get_height()) // 2))
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                flag = False
                pygame.draw.rect(screen, '#323232', (x1, y1, width + 10, height + 10))
                pygame.draw.rect(screen, '#14FFEC', (x, y, width, height))
                screen.blit(text, (x + (width - text.get_width()) // 2,
                                   y + (height - text.get_height()) // 2))
                return
        pygame.display.flip()
        clock.tick(FPS)


def score(count):
    font = pygame.font.Font('../resources/Montserrat-Light.ttf', 16)
    text = font.render(f'Ходы: {count}', False, 'white')
    screen.blit(text, (40, 40))


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((1000, 700))
    pygame.display.set_caption('Paint Cube')
    pygame.display.set_icon(pygame.image.load('../resources/cube.png'))
    key = None
    clock = pygame.time.Clock()
    FPS = 60
    side = 70
    width = 1000
    height = 700
    board = Board('../resources/map.txt')
    board.generate_level(screen, left, top)
    cube = Cube(left, top, '../resources/cube.png')
    # start_screen(screen, width, height)
    screen.fill('#3FC1C9')
    pygame.draw.rect(screen, 'white', (left, top, 630, 630))
    count = 0
    flag = False
    pygame.draw.rect(screen, 'white', (left, top, 630, 630))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    count += 1
                    key = 'down'
                elif event.key == pygame.K_UP:
                    count += 1
                    key = 'up'
                elif event.key == pygame.K_LEFT:
                    count += 1
                    key = 'left'
                elif event.key == pygame.K_RIGHT:
                    count += 1
                    key = 'right'
        if key:
            cube.move(key, spisok, board.slov())
        all_sprites_rect.draw(screen)
        score(count)
        screen.blit(cube.image, cube.rect)
        pygame.draw.rect(screen, 'yellow', (cube.rect[0], cube.rect[1], 70, 70))
        pygame.display.update()
        clock.tick(FPS)
