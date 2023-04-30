import pygame
import os

WINDOW = {
    'WIDTH' : 750,
    'HEIGHT' : 720,
    'FPS' : 60
}

def load_imgs(folder: str, name: str, count_imgs: int, format_img='png') -> list:
    list = []
    for i in range(count_imgs):
        list.append(pygame.image.load(f'{img_path+folder}\\{name}{i}.{format_img}'))

    return list

path = os.path.abspath(__file__+'/..')
img_path = path+'\\img\\'

background = pygame.image.load(img_path+'background.png')
cross = pygame.image.load(img_path+'cross.png')

dogs_anim = load_imgs('dog', 'dog_anim', 11)
duck_anim = load_imgs('duck', 'duck_anim', 8)

ducks_count = [pygame.image.load(img_path+'duck\\white_duck.png'), pygame.image.load(img_path+'duck\\red_duck.png')]

bullet_img = pygame.image.load(img_path+'bullet.png')
