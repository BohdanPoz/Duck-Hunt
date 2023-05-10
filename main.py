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
FONT_SCORE = pygame.font.SysFont('duckhunt.ttf', 50, False)
SHOT_TEXT = FONT.render('SHOT', False, (90, 90, 250))

def run():
    game = True
    menu_regim = 1
    ROUND = 1
    DUCK_COUNT = 10
    BULLETS = 3
    SCORE = 0
    shot_time = -1
    i_count_anim = 0
    index_anim = 0
    x_anim = 0
    y_anim = 500
    jump_anim = True
    ducks_count = [0 for i in range(DUCK_COUNT)]

    ducks = []

    while game:
        pygame.display.set_caption(f'Duck Hunt FPS: {round(clock.get_fps(), 2)}')
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
                            spawn_duck(ducks)
                            ducks_count = [0 for i in range(DUCK_COUNT)]
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

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game = False
                if event.type == pygame.KEYDOWN:
                    print(1)
                    if event.key == pygame.K_ESCAPE:
                        menu_regim = 2
                        spawn_duck(ducks)
                        ducks_count = [0 for i in range(DUCK_COUNT)]

        elif menu_regim == 2:
            #print(ducks)
            pygame.mouse.set_visible(False)
            window.fill((0, 0, 250))
            for duck in ducks:
                duck.draw(window, spawn_duck, ducks, ducks_count, DUCK_COUNT)
                duck.move(ducks)
                if duck.DEATH and duck.SPAWN:
                    DUCK_COUNT -= 1
                    duck.SPAWN = False
                #    spawn_duck(ducks)

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
                                change_score = duck.death()
                                SCORE += change_score if type(change_score) == type(1) else 0
                        window.fill((0, 0, 0))
                        BULLETS -= 1
                        if shot_time < 0:
                            shot_time = time.time()

            window.blit(data.cross, (pygame.mouse.get_pos()[0]-data.cross.get_width()//2, pygame.mouse.get_pos()[1]-data.cross.get_height()//2))

            if DUCK_COUNT <= 0 and ducks == []:
                ROUND += 1
                DUCK_COUNT = 10
                i_count_anim = 0
                index_anim = 0
                x_anim = 0
                y_anim = 500
                jump_anim = True
                ducks_count.sort(reverse=True)
                menu_regim = 1

        round_count = FONT.render(f'R={ROUND}', False, (90, 180, 20))
        window.blit(round_count, (55, 601))
        x = 500-260
        for i in ducks_count:
            window.blit(data.ducks_count[i], (x, 645))

            x+=26
        x = 51
        for i in range(BULLETS):
            window.blit(data.bullet_img, (x, 635))
            x+=24
        window.blit(SHOT_TEXT, (55, 664))
        SCORE_STR = ''
        for i in range(6-len(str(SCORE))): SCORE_STR += '0'
        SCORE_STR += str(SCORE)
        SCORE_SURF = FONT_SCORE.render(SCORE_STR, False, (255, 255, 255))
        window.blit(SCORE_SURF, (555, 630))

        pygame.display.flip()
        clock.tick(FPS)

run()
