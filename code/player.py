import pygame
from os import walk
from support import import_folder
class Player(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[int, int], groups: pygame.sprite.Group, obstacle_sprites:pygame.Surface):
        super().__init__(groups)
        self.image = pygame.image.load("graphics/test/player.png").convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.import_character_assets()

        self.direction = pygame.math.Vector2()
        self.speed = 10
        self.status = 'down'
        self.frame_index = 0
        self.animation_speed = 0.15

        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None

        self.hitbox = self.rect.inflate(0, -26)
        self.obstacle_sprites = obstacle_sprites

    def import_character_assets(self):
        character_path = 'graphics/player'
        self.animations = {
            'up':[], 'down':[], 'left':[], 'right':[],
            'up_idle':[], 'down_idle':[], 'left_idle':[], 'right_idle':[],
            'up_attack':[], 'down_attack':[], 'left_attack':[], 'right_attack':[]
        }
        for animation in self.animations.keys():
            current_path = character_path+'/'+animation
            self.animations[animation] = import_folder(current_path)

    def input(self):
        keys = pygame.key.get_pressed()
        if not self.attacking:
            # Movement input
            if keys[pygame.K_UP]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_DOWN]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0
            
            if keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.status = 'left'
            elif keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.status = 'right'
            else:
                self.direction.x = 0

            if keys[pygame.K_d]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
            if keys[pygame.K_s]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        # Move the hitbox accordingly
        self.hitbox.x += self.direction.x*speed
        self.collide("horizontal")
        self.hitbox.y += self.direction.y*speed
        self.collide("vertical")

        # Set the rect box to hitbox
        self.rect.center = self.hitbox.center

    def get_status(self):
        # idle status
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status:
                self.status = self.status.removesuffix('_attack') +'_idle'

        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if not 'attack' in self.status:
                self.status = self.status.removesuffix('_idle') +  '_attack'
            
    def cooldowns(self):
        if self.attacking:
            current_time = pygame.time.get_ticks()
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False

    def collide(self, direction):
        if direction == "horizontal":
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right

        if direction == "vertical":
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom

    def animate(self):
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]

        self.rect = self.image.get_rect(center = self.hitbox.center)

    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.speed)