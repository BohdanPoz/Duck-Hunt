import pygame
import data
pygame.init()

WIDTH, HEIGHT = data.WINDOW['WIDTH'], data.WINDOW['HEIGHT']
FPS = data.WINDOW['FPS']

clock = pygame.time.Clock()

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Duck Hunt")

def run():
    game = True
    menu_regim = 1
    i_count_anim = 0
    index_anim = 0
    x_anim = 0
    y_anim = 500
    jump_anim = True

    while game:
        
        if menu_regim == 0:
            pass
        elif menu_regim == 1:
            pygame.mouse.set_visible(False)
            window.fill((0, 0, 250))
            window.blit(data.background, (0, 0))

            if i_count_anim//14//4 >= 16:
                if i_count_anim//14//4//10 <= 1:
                    window.blit(data.dogs_anim[4], (x_anim, y_anim-10))
                else:
                    if jump_anim:
                        if y_anim <= 420:
                            jump_anim = False
                        window.blit(data.dogs_anim[5], (x_anim, y_anim))
                        y_anim -= 1
                    else:
                        if y_anim >= 500:
                            menu_regim = 2
                        window.blit(data.dogs_anim[6], (x_anim, y_anim))
                        window.blit(data.background, (0, 0))
                        y_anim += 1
                #print(i_count_anim//14//4//10)

            else:
                if i_count_anim//14//4 % 4 == 0:
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
            pygame.mouse.set_visible(False)
            window.fill((0, 0, 250))
            window.blit(data.background, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game = False

            window.blit(data.cross, (pygame.mouse.get_pos()[0]+data.cross.get_width()//2, pygame.mouse.get_pos()[1]+data.cross.get_height()//2))
        pygame.display.flip()
        clock.tick(FPS)

run()
