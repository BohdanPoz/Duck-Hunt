import pygame
import data
pygame.init()

class Duck():
    def __init__(self, x, y, imgs, stepx, stepy, img_delay_max=30):
        self.X, self.Y = x, y
        self.STEPX, self.STEPY = stepx, stepy
        self.FALL = False
        self.FLY_UP = True

        self.IMGS = imgs
        self.DEATH = False

        self.IMG_INDEX = 0
        self.IMG_DELAY_MAX = img_delay_max
        self.IMG_DELAY = 0

        self.WIDTH, self.HEIGHT = self.IMGS[self.IMG_INDEX].get_size()
        self.RECT = pygame.Rect(self.X, self.Y, self.WIDTH, self.HEIGHT)

    def draw(self, window):
        if not self.DEATH:

            if self.IMG_DELAY <= self.IMG_DELAY_MAX // 3:
                self.IMG_INDEX = 0
                self.WIDTH, self.HEIGHT = self.IMGS[self.IMG_INDEX].get_size()
                self.RECT.size = (self.WIDTH, self.HEIGHT)
            elif self.IMG_DELAY <= self.IMG_DELAY_MAX-self.IMG_DELAY_MAX // 3:
                self.IMG_INDEX = 1
                self.WIDTH, self.HEIGHT = self.IMGS[self.IMG_INDEX].get_size()
                self.RECT.size = (self.WIDTH, self.HEIGHT)
            elif self.IMG_DELAY <= self.IMG_DELAY_MAX:
                self.IMG_INDEX = 2
                self.WIDTH, self.HEIGHT = self.IMGS[self.IMG_INDEX].get_size()
                self.RECT.size = (self.WIDTH, self.HEIGHT)

        else:
            if self.IMG_DELAY // self.IMG_DELAY_MAX <= 3 and not self.FALL:
                self.IMG_INDEX = 3
            elif self.IMG_DELAY // self.IMG_DELAY_MAX >= 3 and not self.FALL:
                self.FALL = True
                self.IMG_DELAY = 0
            else:
                self.IMG_INDEX = 4

        self.IMG_DELAY += 1
        if (not self.DEATH and not self.FALL) or self.FALL:
            if self.IMG_DELAY > self.IMG_DELAY_MAX:
                self.IMG_DELAY = 0
    

        window.blit(self.IMGS[self.IMG_INDEX], (self.X, self.Y))

    def move(self, ducks):
        if not self.DEATH:
            if self.RECT.bottom < 380:
                self.FLY_UP = False
            if self.RECT.top <= 0 or (self.RECT.bottom >= 400 and not self.FLY_UP):
                self.STEPY *= -1
            if self.RECT.left <= 0 or self.RECT.right >= data.WINDOW['WIDTH']:
                self.STEPX *= -1
                for i, img in enumerate(self.IMGS):
                    self.IMGS[i] = pygame.transform.flip(img, True, False)

            self.X += self.STEPX
            self.Y += self.STEPY
        else:
            if self.FALL:
                self.Y += 3

        self.RECT.topleft = (self.X, self.Y)

        if self.Y >= data.WINDOW['HEIGHT']:
            ducks.remove(self)

    def death(self):
        self.DEATH = True
        self.IMG_DELAY = 0
