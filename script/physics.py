from random import randint
import pygame

class Entity:
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.type = e_type
        self.size = size
        
        self.pos = list(pos)
        self.mov = [0, 0]
        self.frame_mov = 0
        self.velocity = 0
        
        self.collision = {'up': False, 'down': False, 'left': False, 'right': False}

        self.flip = False
            
    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
    
    def going_right(self):
        return self.frame_mov > 0
    
    def going_left(self):
        return self.frame_mov < 0
    
    def going_up(self):
        return self.velocity < 0
    
    def going_down(self):
        return self.velocity > 0

    def update(self, tilemap):
        self.collision = {'up': False, 'down': False, 'left': False, 'right': False}
        
        self.frame_mov = (self.mov[0] - self.mov[1]) * 6
        self.velocity = min(self.velocity + 2, 14)

        self.pos[0] += self.frame_mov
        entity_rect = self.rect()
        for rect in tilemap:
            if entity_rect.colliderect(tilemap[rect]):
                if self.going_left():
                    entity_rect.left = tilemap[rect].right
                    self.collision['left'] = True
                if self.going_right():
                    entity_rect.right = tilemap[rect].left
                    self.collision['right'] = True
                self.pos[0] = entity_rect.x
        
        self.pos[1] += self.velocity
        entity_rect = self.rect()
        for rect in tilemap:
            if entity_rect.colliderect(tilemap[rect]):
                if self.going_up():
                    entity_rect.top = tilemap[rect].bottom
                    self.collision['up'] = True
                if self.going_down():
                    entity_rect.bottom = tilemap[rect].top
                    self.collision['down'] = True
                self.pos[1] = entity_rect.y
        
    def render(self, surf):
        surf.blit(pygame.transform.flip(self.game.assets[self.type], self.flip, False), self.pos)



class Player(Entity):
    def __init__(self, game, pos, size):
        super().__init__(game, "player", pos, size)

        self.jumps = 1
        self.alive = True
    
    def update(self, tilemap):
        super().update(tilemap)

        if self.collision['down']:
            self.jumps = 1
            self.velocity = 0

        if self.going_left():
            self.flip = True
        if self.going_right():
            self.flip = False
    
    def jump(self):
        if self.jumps > 0:
            self.velocity -= 30
            self.jumps -= 1
        


class Bomb(Entity):
    def __init__(self, game, pos, size, explosion_radius, min_velocity):
        super().__init__(game, "bomb", pos, size)
        
        self.velocity = min_velocity
        self.radius = explosion_radius
        self.exploding = False

    def collide(self):
        return self.collision['down'] or self.game.player.rect().colliderect(self.rect())
    
    def update(self, tilemap):
        super().update(tilemap)

        if self.collide():
            self.explode()
        else:
            self.exploding = False
    
    def explode(self):
        self.explosion_rect = pygame.Rect(self.pos[0] - self.radius, self.pos[1] - self.radius, self.size[0] + self.radius * 2, self.size[0] + self.radius * 2)
        
        self.exploding = True
        self.pos = [randint(2, 12) * 55, -99]
        self.velocity = randint(1, 5)

    def render(self, surf):
        if not self.exploding:
            super().render(surf)
        else:
            pygame.draw.rect(surf, (255, 0, 255), self.explosion_rect)