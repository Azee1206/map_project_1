import sys
import pygame
from button import Button
import os


def search(screen, map_file):
    TEXT_COLOR = (100, 100, 100)
    TEXT_FONT = pygame.font.Font(None, 30)
    text = ''

    search_btn_img = pygame.image.load('buttons/find_btn.png').convert_alpha()
    search_btn = Button(472, 386, search_btn_img, 2)

    run_search = True
    while run_search:
        text_on_screen = TEXT_FONT.render(text, True, pygame.color.Color('black'))
        screen.blit(pygame.image.load(map_file), (0, 0))
        pygame.draw.line(screen, TEXT_COLOR, (1, 440), (530, 440), 5)
        screen.blit(text_on_screen, (2, 422))
        if search_btn.draw(screen):
            return None

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_search = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return text
                elif event.key == pygame.K_BACKSPACE:
                    text = text[0:-1]
                else:
                    text += event.unicode
        pygame.display.flip()
    pygame.quit()
    os.remove(map_file)
    sys.exit()
