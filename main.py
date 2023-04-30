import pygame
import data
import modules
import random, time
pygame.init()

WIDTH, HEIGHT = data.WINDOW['WIDTH'], data.WINDOW['HEIGHT']
FPS = data.WINDOW['FPS']

def spawn_duck(ducks):
    if random.random() <= 0.5:
        ducks.append(modules.Duck(random.randint(0, data.WINDOW['WIDTH']-70), 510, data.duck_anim[:3]+data.duck_anim[-2:], 3, -1))
    else:
        ducks.append(modules.Duck(random.randint(0, data.WINDOW['WIDTH']-70), 510, data.duck_anim[3:], 4, -1))

clock = pygame.time.Clock()

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Duck Hunt")

FONT = pygame.font.SysFont('duckhunt.ttf', 28, True)

def run():
    game = True
    menu_regim = 1
    ROUND = 1
    DUCK_COUNT = 10
    BULLETS = 3
    shot_time = -1
    i_count_anim = 0
    index_anim = 0
    x_anim = 0
    y_anim = 500
    jump_anim = True

    ducks = []
    spawn_duck(ducks)

    while game:
        
        if menu_regim == 0:
            pass
        elif menu_regim == 1:
            pygame.mouse.set_visible(False)
            window.fill((0, 0, 250))
            window.blit(data.background, (0, 0))

            if i_count_anim//14//4 >= 16:
                if i_count_anim//14//40 <= 1:
                    window.blit(data.dogs_anim[4], (x_anim, y_anim-10))
                else:
                    if jump_anim:
                        if y_anim <= 400:
                            jump_anim = False
                        window.blit(data.dogs_anim[5], (x_anim, y_anim))
                        y_anim -= 2
                    else:
                        if y_anim >= 500:
                            menu_regim = 2
                        window.blit(data.dogs_anim[6], (x_anim, y_anim))
                        window.blit(data.background, (0, 0))
                        y_anim += 2
                #print(i_count_anim//14//4//10)

            else:
                if i_count_anim//14//8 % 4 == 0:
                    if index_anim == 3:
                        index_anim = 0

                    x_anim += 1
                    window.blit(data.dogs_anim[:3][index_anim], (x_anim, y_anim))

                    if i_count_anim % 14 == 0:
                        index_anim += 1
                else:
                    if i_count_anim % 10 == 0:
                        index_anim = -1
                    if i_count_anim % 20 == 0:
                        index_anim = 0

                    window.blit(data.dogs_anim[:4][index_anim], (x_anim, y_anim))

                    #index_anim = 0

            i_count_anim += 1

            #print(i_count_anim//14//4 == 17)

            #x = 0
            #for i in range(7):
            #    window.blit(data.dogs_anim[i], (x, 0))
            #    x += 106

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game = False

        elif menu_regim == 2:
            #print(ducks)
            pygame.mouse.set_visible(False)
            window.fill((0, 0, 250))
            if len(ducks) <= 0:
                spawn_duck(ducks)
                DUCK_COUNT -= 1
            for duck in ducks:
                duck.draw(window)
                duck.move(ducks)

            window.blit(data.background, (0, 0))

            if BULLETS < 3:
                if time.time() - shot_time >= 3:
                    #print(0)
                    BULLETS += 1
                    if BULLETS >= 3:
                        shot_time = -1
                    else:
                        shot_time = time.time()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0] and BULLETS > 0:
                        for duck in ducks:
                            if duck.RECT.collidepoint(pygame.mouse.get_pos()):
                                duck.death()
                        window.fill((0, 0, 0))
                        BULLETS -= 1
                        if shot_time < 0:
                            shot_time = time.time()

            window.blit(data.cross, (pygame.mouse.get_pos()[0]-data.cross.get_width()//2, pygame.mouse.get_pos()[1]-data.cross.get_height()//2))
        
        #x = 0
        #for i in range(len(data.duck_anim[:3]+data.duck_anim[-2:])):
        #    l = data.duck_anim[:3]+data.duck_anim[-2:]
        #    #print(l)
        #    window.blit(l[i], (x, 5))
        #    x += l[i].get_width()+2

        round_count = FONT.render(f'R={ROUND}', False, (90, 180, 20))
        window.blit(round_count, (55, 601))
        x = 500-26
        for i in range(DUCK_COUNT):
            window.blit(data.ducks_count[0], (x, 645))
            x-=26
        for i in range(10-DUCK_COUNT):
            window.blit(data.ducks_count[1], (x, 645))
            x-=26
        x = 51
        for i in range(BULLETS):
            window.blit(data.bullet_img, (x, 635))
            x+=24
        pygame.display.flip()
        clock.tick(FPS)

run()
