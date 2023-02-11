import pygame
import requests
import sys
import os


def get_map(ll_spn=None, map_type="map", add_params=None):
    if ll_spn:
        map_request = f"http://static-maps.yandex.ru/1.x/?{ll_spn}&l={map_type}"
    else:
        map_request = f"http://static-maps.yandex.ru/1.x/?l={map_type}"

    if add_params:
        map_request += "&" + add_params
    response = requests.get(map_request)

    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    # Запишем полученное изображение в файл.
    map_file = "map.png"
    try:
        with open(map_file, "wb") as file:
            file.write(response.content)
    except IOError as ex:
        print("Ошибка записи временного файла:", ex)
        sys.exit(2)
    return map_file


def show_map(ll, spn, ll_spn=None, map_type="map", add_params=None):
    pygame.init()
    screen = pygame.display.set_mode((600, 450))
    run = True
    map_file = get_map(ll_spn, map_type, add_params)
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_PAGEUP] or keys[pygame.K_w]:
            spn = list(map(float, spn.split(',')))
            spn[0] += 0.062
            spn[1] += 0.062
            if spn[0] < 2.5 and spn[1] < 2.5:
                spn = ','.join(map(str, spn))
                ll_spn = f'll={ll}&spn={spn}'
                map_file = get_map(ll_spn, map_type, add_params)
            else:
                spn[0] -= 0.062
                spn[1] -= 0.062
                spn = ','.join(map(str, spn))

        elif keys[pygame.K_PAGEDOWN] or keys[pygame.K_s]:
            spn = list(map(float, spn.split(',')))
            spn[0] -= 0.062
            spn[1] -= 0.062
            if spn[0] > 0 and spn[1] > 0:
                spn = ','.join(map(str, spn))
                ll_spn = f'll={ll}&spn={spn}'
                map_file = get_map(ll_spn, map_type, add_params)
            else:
                spn[0] += 0.062
                spn[1] += 0.062
                spn = ','.join(map(str, spn))

        screen.blit(pygame.image.load(map_file), (0, 0))
        pygame.display.flip()

    pygame.quit()
    os.remove(map_file)
