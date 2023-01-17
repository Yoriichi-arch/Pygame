import pygame


class Cube(pygame.sprite.Sprite):
    def __init__(self, x, y, filename):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename)
        self.rect = self.image.get_rect(left=x, top=y)
        event = False
        move = False

    def move(self, key, spisok, symbols):
        x = self.rect.x
        y = self.rect.y
        coords = f'({x}, {y})'
        if key == 'down':
            coords = f'({x}, {y + 70})'
            if (spisok[3].colliderect(self.rect) is False) and symbols[coords] != '#':
                self.rect.y += 70
        elif key == 'up':
            coords = f'({x}, {y - 70})'
            if (spisok[1].colliderect(self.rect) is False) and symbols[coords] != '#':
                self.rect.y -= 70
        elif key == 'left':
            coords = f'({x - 70}, {y})'
            if (spisok[0].colliderect(self.rect) is False) and symbols[coords] != '#':
                self.rect.x -= 70
        elif key == 'right':
            coords = f'({x + 70}, {y})'
            if (spisok[2].colliderect(self.rect) is False) and symbols[coords] != '#':
                self.rect.x += 70

    def get_coords_cube(self):
        x = self.rect.x
        y = self.rect.y
        return x, y
