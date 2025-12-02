from player import Player
from settings import *
import pygame

class UI():
    def __init__(self):
        # General
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        # Bar setup
        self.health_bar_rect = pygame.Rect(10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.energy_bar_rect = pygame.Rect(10, 40, ENERGY_BAR_WIDTH, BAR_HEIGHT)

        # Weapon list
        self.weapons_graphics = []
        for weapon in weapon_data.values():
            path = weapon['graphic']
            weapon = pygame.image.load(path).convert_alpha()
            self.weapons_graphics.append(weapon)

    def show_bar(self, current: int, max: int, bg_rect: pygame.Rect, color: str):
        # Draw the bg bar
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)

        ratio = current/max
        fg_rect = bg_rect.copy()
        fg_rect.width = bg_rect.width * ratio
        
        # Draw the bg bar
        pygame.draw.rect(self.display_surface, color, fg_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)

    def show_exp(self, exp):
        text_surface = self.font.render(str(int(exp)),False, TEXT_COLOR)

        x_pos, y_pos = self.display_surface.get_size()
        text_rect = text_surface.get_rect(bottomright = (x_pos-20, y_pos-20))

        pygame.draw.rect(self.display_surface, UI_BG_COLOR, text_rect.inflate(20,20))
        self.display_surface.blit(text_surface, text_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, text_rect.inflate(20,20), 3)

    def show_selection(self, x, y, has_switched) -> pygame.Rect:
        bg_rect = pygame.Rect(x, y, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)
        if has_switched:
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR_ACTIVE, bg_rect, 3)
        else:
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)
        return bg_rect

    def show_weapon(self, weapon_index, has_switched):
        bg_rect = self.show_selection(10, 630, has_switched)
        weapon_surf = self.weapons_graphics[weapon_index]
        weapon_rect = weapon_surf.get_rect(center = bg_rect.center)

        self.display_surface.blit(weapon_surf, weapon_rect)

    def display(self, player: Player):
        self.show_bar(player.health, player.stats['health'], self.health_bar_rect, HEALTH_COLOR)
        self.show_bar(player.energy, player.stats['energy'], self.energy_bar_rect, ENERGY_COLOR)
        self.show_exp(player.experience)
        self.show_weapon(player.weapon_index, not player.can_switch_weapon)