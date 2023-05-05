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
        self.TYPE_DEATH = ''
        self.SPAWN = True
        self.DOG_ANIM = False
        self.TOUCHS = 0

        self.IMG_INDEX = 0
        self.IMG_DELAY_MAX = img_delay_max
        self.IMG_DELAY = 0

        self.WIDTH, self.HEIGHT = self.IMGS[self.IMG_INDEX].get_size()
        self.RECT = pygame.Rect(self.X, self.Y, self.WIDTH, self.HEIGHT)

    def draw(self, window, spawn_duck, ducks, ducks_count, duck_count):
        if not self.DOG_ANIM:
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
                if self.IMG_DELAY // (self.IMG_DELAY_MAX//2) <= 3 and not self.FALL:
                    self.IMG_INDEX = 3
                elif self.IMG_DELAY // (self.IMG_DELAY_MAX//2) >= 3 and not self.FALL:
                    self.FALL = True
                    self.IMG_DELAY = 0
                else:
                    self.IMG_INDEX = 4

            self.IMG_DELAY += 1
            if (not self.DEATH and not self.FALL) or self.FALL:
                if self.IMG_DELAY > self.IMG_DELAY_MAX:
                    self.IMG_DELAY = 0


            window.blit(self.IMGS[self.IMG_INDEX], (self.X, self.Y))
        else:
            self.dog_anim(window, spawn_duck, ducks, ducks_count, duck_count)

    def move(self, ducks):
        print(self.TOUCHS)
        if not self.DEATH:
            if self.RECT.bottom < 350 and not self.DOG_ANIM:
                self.FLY_UP = False
            if (self.RECT.bottom >= 400 and not self.FLY_UP):
                self.STEPY *= -1
            if self.RECT.top <= 0 and self.TOUCHS <= 6:
                self.STEPY *= -1
                self.TOUCHS += 1
            if (self.RECT.left <= 0 or self.RECT.right >= data.WINDOW['WIDTH']) and self.TOUCHS <= 6:
                self.STEPX *= -1
                self.TOUCHS += 1
                for i, img in enumerate(self.IMGS):
                    self.IMGS[i] = pygame.transform.flip(img, True, False)

            self.X += self.STEPX
            self.Y += self.STEPY
        else:
            if self.FALL and not self.DOG_ANIM:
                self.Y += 3

        self.RECT.topleft = (self.X, self.Y)

        if self.Y >= 700:
            self.DOG_ANIM = True
            self.Y = 500
            self.IMG_DELAY = 0

        if (self.RECT.bottom <= 0 or self.RECT.right <= 0 or self.RECT.left >= data.WINDOW['WIDTH']) and not self.DOG_ANIM:
            self.death('fly')

    def death(self, death_type='kill'):
        self.DEATH = True
        self.FLY_UP = True
        self.IMG_DELAY = 0
        self.TYPE_DEATH = death_type
        print(death_type)

    def dog_anim(self, window, spawn_duck, ducks, ducks_count, duck_count):
        if self.TYPE_DEATH == 'kill':
            window.blit(data.dogs_anim[7], (self.X, self.Y))
            if self.FLY_UP:
                self.Y = self.Y - 1
            else:
                self.Y += 1
                if self.Y >= 500:
                    spawn_duck(ducks)
                    ducks.remove(self)

            if self.Y <= 430:
                self.FLY_UP = False
            ducks_count[10-duck_count-1] = 1
        elif self.TYPE_DEATH == 'fly':
            window.blit(data.dogs_anim[-self.IMG_INDEX], (320, self.Y))
            if self.FLY_UP:
                self.Y = self.Y - 1
            else:
                self.Y += 1
                if self.Y >= 500:
                    spawn_duck(ducks)
                    ducks.remove(self)

            if self.Y <= 430:
                self.FLY_UP = False
            if self.IMG_DELAY <= self.IMG_DELAY_MAX//2:
                self.IMG_INDEX = 2
            elif self.IMG_DELAY >= self.IMG_DELAY_MAX//2:
                self.IMG_INDEX = 1
            if self.IMG_DELAY > self.IMG_DELAY_MAX:
                self.IMG_DELAY = 0
