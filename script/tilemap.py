import pygame as pg

class Tilemap:
    def __init__(self, game):
        self.game = game

        self.tilemap = {
            'surface': pg.Rect(0, self.game.window.get_height() - 50, self.game.window.get_width(), 50),
            'wall/left': pg.Rect(0, 0, 40, self.game.window.get_height()),
            'wall/right': pg.Rect(self.game.window.get_width() - 40, 0, 40, self.game.window.get_height()),
        }

    def render(self, surf):
        for rect in self.tilemap:
            pg.draw.rect(surf, (209, 123, 46), self.tilemap[rect])