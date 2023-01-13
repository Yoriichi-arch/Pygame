import pygame
import sys
import os
from src.module.cube import Cube

left = 1000 // 2 - 630 // 2
top = 700 // 2 - 630 // 2
all_sprites_rect = pygame.sprite.Group()

rect_left = pygame.Rect((left, top, 1, 630))
rect_top = pygame.Rect((left, top, 630, 1))
rect_right = pygame.Rect((left + 560, top, 1, 630))
rect_down = pygame.Rect((left, top + 560, 630, 1))


border_left = pygame.sprite.Sprite(all_sprites_rect)
border_left.image = pygame.Surface([1, 630])
border_left.image.fill(pygame.Color('red'))
border_left.rect = border_left.image.get_rect(left=left, top=top)

border_top = pygame.sprite.Sprite(all_sprites_rect)
border_top.image = pygame.Surface([630, 1])
border_top.image.fill(pygame.Color('red'))
border_top.rect = border_top.image.get_rect(left=left, top=top)

border_right = pygame.sprite.Sprite(all_sprites_rect)
border_right.image = pygame.Surface([1, 630])
border_right.image.fill(pygame.Color('red'))
border_right.rect = border_right.image.get_rect(left=left + 560, top=top)

border_down = pygame.sprite.Sprite(all_sprites_rect)
border_down.image = pygame.Surface([630, 1])
border_down.image.fill(pygame.Color('red'))
border_down.rect = border_down.image.get_rect(left=left, top=top + 560)

spisok = [border_left.rect, border_top.rect, border_right.rect, border_down.rect]

sp = [rect_left, rect_top, rect_right, rect_down]


class Board:
    # создание поля
    def __init__(self, left, top):
        self.left = left
        self.top = top

    def render(self, surface):
        pygame.draw.rect(surface, 'white', (left, top, 630, 630))


def load_image(name, colorkey=None):
    fullname = os.path.join('../resources', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def load_level(filename):
    filename = '../resources/' + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level, surface, left, top):
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                pygame.draw.rect(surface, 'white', (left + 70 * x, top + 70 * y, 70, 70))
            elif level[y][x] == '#':
                pygame.draw.rect(surface, 'black', (left + 70 * x, top + 70 * y, 70, 70))


def terminate():
    pygame.quit()
    sys.exit()


def check_click(x, y, width, height, position):
    if x <= position[0] <= x + width and y <= position[1] <= y + height:
        return True


# заставка
def start_screen(screen):
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
    pygame.draw.rect(screen, '#323232', (x1, y1, width + 10, height + 10))
    pygame.draw.rect(screen, '#14FFEC', (x, y, width, height))
    screen.blit(text, (x + (width - text.get_width()) // 2,
                       y + (height - text.get_height()) // 2))

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


if __name__ == '__main__':
    pygame.init()
    key = None
    clock = pygame.time.Clock()
    FPS = 60
    side = 70
    left = 1000 // 2 - 630 // 2
    top = 700 // 2 - 630 // 2
    width = 1000
    height = 70
    cube = Cube(left, top, '../resources/cube.png')
    screen = pygame.display.set_mode((1000, 700))
    pygame.display.set_caption('Paint Cube')
    pygame.display.set_icon(pygame.image.load('../resources/cube.png'))
    board = Board(left, top)
    start_screen(screen)
    screen.fill('#3FC1C9')
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    key = 'down'
                elif event.key == pygame.K_UP:
                    key = 'up'
                elif event.key == pygame.K_LEFT:
                    key = 'left'
                elif event.key == pygame.K_RIGHT:
                    key = 'right'
        if key:
            cube.move(key, spisok)
        screen.fill('#3FC1C9')
        generate_level(load_level('map.txt'), screen, left, top)
        screen.blit(cube.image, cube.rect)
        pygame.display.update()
        clock.tick(FPS)

