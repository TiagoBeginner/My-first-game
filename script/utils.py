import pygame as pg
import os

BASE_IMG_PATH = "assets/" 

def load_img(path):
    img = pg.image.load(BASE_IMG_PATH + path)
    img.set_colorkey((0, 0, 0))
    return img