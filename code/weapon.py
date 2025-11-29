import pygame
from player import Player
class Weapon(pygame.sprite.Sprite):

    def __init__(self, player: Player, groups: pygame.sprite.Group):
        super().__init__(groups)
        direction = player.status.split('_')[0]

        # graphic
        full_path = f'graphics/weapons/{player.weapon}/{direction}.png'
        self.image = pygame.image.load(full_path).convert_alpha()

        # placement
        if direction == 'right':
            self.rect = self.image.get_rect(midleft = player.rect.midright+pygame.Vector2(0, 16))
        elif direction == 'left':
            self.rect = self.image.get_rect(midright = player.rect.midleft+pygame.Vector2(0, 16))
        elif direction == 'up':
            self.rect = self.image.get_rect(midbottom = player.rect.midtop+pygame.Vector2(-10,0))
        else:
            self.rect = self.image.get_rect(midtop = player.rect.midbottom+pygame.Vector2(-10,0))
        