import pygame


class Cube(pygame.sprite.Sprite):
    def __init__(self, x, y, filename):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename)
        self.rect = self.image.get_rect(left=x, top=y)

    def move(self, key, spisok):
        if key == 'down':
            if not spisok[3].colliderect(self.rect):
                self.rect.y += 70
        elif key == 'up':
            if not spisok[1].colliderect(self.rect):
                self.rect.y -= 70
        elif key == 'left':
            if not spisok[0].colliderect(self.rect):
                self.rect.x -= 70
        elif key == 'right':
            if not spisok[2].colliderect(self.rect):
                self.rect.x += 70

    def get_coords_cube(self):
        x = self.rect.x
        y = self.rect.y
        coords = (x, y)
        return coords