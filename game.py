import sys
import json
import pygame
from random import randint

import pygame.event
from script.utils import load_img
from script.tilemap import Tilemap
from script.physics import Bomb, Player

class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        
        self.window = pygame.display.set_mode((55 * 14, 800))
        pygame.display.set_caption("Bomb runner")

        self.font = pygame.font.SysFont("Arial", 30)

        self.clock = pygame.time.Clock()
        
        self.assets = {
            'player': load_img("player.png"),
            'bomb': load_img("bomb.png"),
        }
        
        self.tilemap = Tilemap(self)
        
        self.player = Player(self, (self.window.get_width() // 2, self.window.get_height() - self.tilemap.tilemap['surface'].height - 78), (27, 78))
        self.bombs = {}
        bomb_cords = set()
        for i in range(4):
            x = randint(2, 12)
            while x in bomb_cords:
                x = randint(2, 12)
            bomb_cords.add(x)
            self.bombs['bomb' + str(i)] = Bomb(self, (x * 55, -99), (55, 99), 60, randint(1, 5))

        self.score = 0
        with open("score.json", 'r') as f:
            best_score = json.load(f)
        self.b_score = best_score['best_score']

    def check_score(self):
        with open("score.json", 'r') as f:
            last_score = json.load(f)
            if self.score // 30 > last_score["best_score"]:
                self.b_score = self.score // 30
                with open("score.json", 'w') as file:
                    json.dump({'best_score': self.score // 30}, file)
        
    def run(self):
        while True:
            self.window.fill((113, 203, 225))

            self.tilemap.render(self.window)

            for bomb_name in self.bombs:
                bomb = self.bombs[bomb_name]
                
                bomb.update(self.tilemap.tilemap)
                bomb.render(self.window)
                try:
                    if self.player.rect().colliderect(bomb.explosion_rect):
                        self.player.alive = False
                    del bomb.explosion_rect
                except AttributeError:
                    pass

            self.player.update(self.tilemap.tilemap)
            self.player.render(self.window)

            self.window.blit(self.font.render(f"Score: {self.score // 30}           Best score: {self.b_score}", False, (0, 0, 0)), (self.tilemap.tilemap['wall/left'].width + 30, 30))
            self.check_score()
            self.score += 1

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.player.mov[1] = 1
                    if event.key == pygame.K_RIGHT:
                        self.player.mov[0] = 1
                    if event.key == pygame.K_UP:
                        self.player.jump()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.player.mov[1] = 0
                    if event.key == pygame.K_RIGHT:
                        self.player.mov[0] = 0

            if not  self.player.alive:
                DeathScreen(self).show_screen()
                self.__init__()

            pygame.display.update()
            self.clock.tick(30)

class DeathScreen:        
    def __init__(self, game):
        self.font = pygame.font.SysFont("Arial", 30)
        self.game = game

        self.text = pygame.font.SysFont("Arial", 50).render("You lost!", False, (255, 255, 255))
        self.hint = self.font.render("Press Enter to continue", False, (255, 255, 255))
        self.score = self.font.render(f"Your score {self.game.score // 30}", False, (255, 255, 255))
        self.best_score = self.font.render(f"Best score: {self.game.b_score}", False, (255, 255, 255))

    def render(self, surf):
        surf.blit(self.text, (250, 200))
        surf.blit(self.hint, (230, 600))
        surf.blit(self.score, (250, 300))
        surf.blit(self.best_score, (250, 400))
        
    def show_screen(self):
        running = True
        while running:
            self.game.window.fill((0, 0, 0))
            self.render(self.game.window)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        running = False
                        pygame.time.delay(3000)
            
            pygame.display.update()
            self.game.clock.tick(30)
            

                    
if __name__ == "__main__":
    Game().run()