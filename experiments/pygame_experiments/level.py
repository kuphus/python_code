import pygame
from tile import Tile
from player import Player
from settings import tile_size, screen_width

class Level():
    
    def __init__(self, level_data, surface):
        # level setup
        self.display_surface = surface
        self.setup_level(level_data)
        self.world_shift = 0
        
    
    def setup_level(self, layout):
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        
        for row_index, row in enumerate(layout):
            for column_index, cell in enumerate(row):
                x = column_index * tile_size
                y = row_index * tile_size
                if cell == 'X':
                    tile = Tile((x, y), tile_size)
                    self.tiles.add(tile)
                elif cell == 'P':
                    player = Player((x, y))
                    self.player.add(player)
                    
        
    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x
        
        if player_x < (screen_width*0.25) and direction_x < 0:
            self.world_shift = 7
            player.speed = 0
        elif player_x > (screen_width*0.75) and direction_x > 0:
            self.world_shift = -7
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 7


    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed
        
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    #player.direction.x = 0
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    
                    
                    
    def vertical_collision(self):
        player = self.player.sprite
        player.apply_gravity()
        
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                print("y speed: " + str(player.direction.y))
                if player.direction.y > 0:
                    print("and up...")
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                elif player.direction.y < 0:
                    print("and down...")
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    
    
    def draw(self):
        # level tiles
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)
        self.scroll_x()
        
        # player
        self.horizontal_movement_collision()
        self.vertical_collision()
        self.player.draw(self.display_surface)
        self.player.update()
        
    
