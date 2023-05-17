import pygame
import data
import time
pygame.init()

TOP_RECORD = 0

with open('record.txt') as record:
    TOP_RECORD = record.read()

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

    def move(self, ROUND):
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
            if ROUND > 1:
                stepx, stepy = self.STEPX, self.STEPY
            else:
                stepx, stepy = self.STEPX, self.STEPY
            
            self.X += stepx
            self.Y += stepy
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
            self.DOG_ANIM = True
            self.Y = 500

    def death(self, death_type='kill'):
        self.DEATH = True
        self.FLY_UP = True
        self.IMG_DELAY = 0
        self.TYPE_DEATH = death_type
        if death_type == 'kill':
            if self.TOUCHS < 2:
                return 1000
            elif self.TOUCHS >= 2 and self.TOUCHS <= 4:
                return 750
            elif self.TOUCHS > 4:
                return 500

    def dog_anim(self, window, spawn_duck, ducks, ducks_count, duck_count):
        if self.TYPE_DEATH == 'kill':
            window.blit(data.dogs_anim[7], (self.X, self.Y))
            if self.FLY_UP:
                self.Y = self.Y - 1
            else:
                self.Y += 1
                if self.Y >= 490:
                    if duck_count >= 0:
                        spawn_duck(ducks)
                    ducks.remove(self)

            if self.Y <= 420:
                self.FLY_UP = False
            if duck_count >= 1:
                ducks_count[10-duck_count-1] = 1
        elif self.TYPE_DEATH == 'fly':
            window.blit(data.dogs_anim[-self.IMG_INDEX], (320, self.Y))
            if self.FLY_UP:
                self.Y = self.Y - 0.5
            else:
                self.Y += 0.5
                if self.Y >= 490:
                    if duck_count >= 1:
                        spawn_duck(ducks)
                    ducks.remove(self)

            if self.Y <= 420:
                self.FLY_UP = False
            if self.IMG_DELAY <= self.IMG_DELAY_MAX//2:
                self.IMG_INDEX = 2
            elif self.IMG_DELAY >= self.IMG_DELAY_MAX//2:
                self.IMG_INDEX = 1
            self.IMG_DELAY += 1
            if self.IMG_DELAY > self.IMG_DELAY_MAX:
                self.IMG_DELAY = 0

class TEXT_SCORE:
    def __init__(self, x, y, score, font, scores):
        scores.append(self)
        self.X, self.Y = x, y

        self.SCORES = scores
        self.TEXT_SCORE = font.render(str(score), False, (255, 255, 255))
        self.TIME = time.time()

    def draw(self, window):
        if abs(time.time() - self.TIME) <= 1.5:
            window.blit(self.TEXT_SCORE, (self.X, self.Y))
        else:
            self.SCORES

class Menu:
    def __init__(self, window, color_background, img_title, color_buttons, font_button, size_fontb):
        self.WINDOW = window

        self.FONT_BUTTON = pygame.font.SysFont(font_button, size_fontb, True)
        self.BUTTONS = []

        self.COLOR_BACKGOUND = color_background
        self.TITLE = pygame.image.load(data.img_path+img_title)
        self.COLOR_BUTTONS = color_buttons

        self.CURENT_BUTTON = None
    
    def add_button(self, text, func=None):
        self.BUTTONS.append((self.FONT_BUTTON.render(text, False, self.COLOR_BUTTONS), self.FONT_BUTTON.render(text, False, self.COLOR_BACKGOUND, self.COLOR_BUTTONS), func))
        with open('record.txt', 'w') as f:
            f.write(str(self.BUTTONS))

    def draw(self):
        self.WINDOW.fill(self.COLOR_BACKGOUND)
        self.WINDOW.blit(self.TITLE, (data.WINDOW['WIDTH']//2-self.TITLE.get_width()//2, 20))

        y = 100 + self.TITLE.get_height()

        for i, button in enumerate(self.BUTTONS):
            if self.CURENT_BUTTON != i:
                self.WINDOW.blit(button[0], (data.WINDOW['WIDTH']//2-button[1].get_width()//2, y))
            else:
                self.WINDOW.blit(button[1], (data.WINDOW['WIDTH']//2-button[1].get_width()//2, y))
            y += button[1].get_height() + 10

    def event_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    if self.CURENT_BUTTON != None:
                        self.CURENT_BUTTON += 1
                    elif self.CURENT_BUTTON == None:
                        self.CURENT_BUTTON = 0
                elif event.key == pygame.K_UP:
                    if self.CURENT_BUTTON != None:
                        self.CURENT_BUTTON -= 1
                    elif self.CURENT_BUTTON == None:
                        self.CURENT_BUTTON = len(self.BUTTONS)-1

                if self.CURENT_BUTTON != None:
                    if self.CURENT_BUTTON <= -1:
                        self.CURENT_BUTTON = len(self.BUTTONS)-1
                    elif self.CURENT_BUTTON >= len(self.BUTTONS):
                        self.CURENT_BUTTON = 0

                if event.key == pygame.K_RETURN and self.CURENT_BUTTON != None:
                    if self.BUTTONS[self.CURENT_BUTTON][-1] != None:
                        self.BUTTONS[self.CURENT_BUTTON][-1]()
