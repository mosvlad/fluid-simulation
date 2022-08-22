import pygame
import random

import Parameters

import World

pygame.init()

screen = pygame.display.set_mode([Parameters.DOMAIN_WIDTH, Parameters.DOMAIN_HEIGHT])

running = True

w = World.Wold()

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEWHEEL:
            mousex, mousey = pygame.mouse.get_pos()
            w.add_particle([[mousex, mousey]])
        # if event.type == pygame.MOUSEBUTTONDOWN:
        #     click = pygame.mouse.get_pressed()
        #     mousex, mousey = pygame.mouse.get_pos()
        #
        #     if click[0]:
        #         w.add_particle([[mousex, mousey]])

    screen.fill((255, 255, 255))
    w.update()
    w.draw(screen)
    pygame.display.flip()

pygame.quit()
