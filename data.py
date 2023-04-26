import pygame
import os

WINDOW = {
    'WIDTH' : 750,
    'HEIGHT' : 720,
    'FPS' : 60
}

path = os.path.abspath(__file__+'/..')
img_path = path+'\\img\\'

dogs = pygame.image.load(img_path+'dog.png')
background = pygame.image.load(img_path+'background.png')

dogs_anim = []
x = 0
y = 0
for i in range(4):
    dogs_anim.append(pygame.transform.scale(dogs.subsurface((x, y, 52, 42)), (104, 84)))
    x += 53

dogs_anim.append(pygame.transform.scale(dogs.subsurface((0, 43, 52, 47)), (104, 94)))
dogs_anim.append(pygame.transform.scale(dogs.subsurface((53, 43, 34, 47)), (68, 94)))
dogs_anim.append(pygame.transform.scale(dogs.subsurface((88, 43, 32, 47)), (64, 94)))

cross = pygame.image.load(img_path+'cross.png')
