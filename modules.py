import pygame
import data
pygame.init()

class Duck():
    def __init__(self, x, y, width, height, imgs, stepx, stepy):
        self.X, self.Y = x, y
        self.WIDTH, self.HEIGHT = width, height
        self.STEPX, self.STEPY = stepx, stepy

        self.IMGS = imgs

    def draw(self, window):
        window.blit
