import pygame
import requests
import sys
import os


MAP_MOVING_SPEED = 0.24
SPN_CHANGING_SPEED = 0.062
MAX_SPN = 5


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
        # Изменение масштаба карты (spn)
        # Приближение
        if keys[pygame.K_PAGEUP] or keys[pygame.K_w]:
            spn = list(map(float, spn.split(',')))
            spn[0] += SPN_CHANGING_SPEED
            spn[1] += SPN_CHANGING_SPEED
            if spn[0] < MAX_SPN and spn[1] < MAX_SPN:
                spn = ','.join(map(str, spn))
                ll_spn = f'll={ll}&spn={spn}'
                map_file = get_map(ll_spn, map_type, add_params)
            else:
                spn[0] -= SPN_CHANGING_SPEED
                spn[1] -= SPN_CHANGING_SPEED
                spn = ','.join(map(str, spn))

        # Отдаление
        elif keys[pygame.K_PAGEDOWN] or keys[pygame.K_s]:
            spn = list(map(float, spn.split(',')))
            spn[0] -= SPN_CHANGING_SPEED
            spn[1] -= SPN_CHANGING_SPEED
            if spn[0] > 0 and spn[1] > 0:
                spn = ','.join(map(str, spn))
                ll_spn = f'll={ll}&spn={spn}'
                map_file = get_map(ll_spn, map_type, add_params)
            else:
                spn[0] += SPN_CHANGING_SPEED
                spn[1] += SPN_CHANGING_SPEED
                spn = ','.join(map(str, spn))

        # Изменение положения карты (ll)
        # Движение в северном направлении
        if keys[pygame.K_UP]:
            ll = list(map(float, ll.split(',')))
            ll[1] += MAP_MOVING_SPEED
            if ll[1] < 80:
                ll = ','.join(map(str, ll))
                ll_spn = f'll={ll}&spn={spn}'
                map_file = get_map(ll_spn, map_type, add_params)
            else:
                ll[1] -= MAP_MOVING_SPEED
                ll = ','.join(map(str, ll))

        # Движение в южном направлении
        if keys[pygame.K_DOWN]:
            ll = list(map(float, ll.split(',')))
            ll[1] -= MAP_MOVING_SPEED
            if ll[1] > -80:
                ll = ','.join(map(str, ll))
                ll_spn = f'll={ll}&spn={spn}'
                map_file = get_map(ll_spn, map_type, add_params)
            else:
                ll[1] += MAP_MOVING_SPEED
                ll = ','.join(map(str, ll))

        # Движение в восточном направлении
        if keys[pygame.K_RIGHT]:
            ll = list(map(float, ll.split(',')))
            ll[0] += MAP_MOVING_SPEED
            if ll[0] < 179:
                ll = ','.join(map(str, ll))
                ll_spn = f'll={ll}&spn={spn}'
                map_file = get_map(ll_spn, map_type, add_params)
            else:
                ll[0] -= MAP_MOVING_SPEED
                ll = ','.join(map(str, ll))

        # Движение в западном направлении
        if keys[pygame.K_LEFT]:
            ll = list(map(float, ll.split(',')))
            ll[0] -= MAP_MOVING_SPEED
            if ll[0] > -179:
                ll = ','.join(map(str, ll))
                ll_spn = f'll={ll}&spn={spn}'
                map_file = get_map(ll_spn, map_type, add_params)
            else:
                ll[0] += MAP_MOVING_SPEED
                ll = ','.join(map(str, ll))

        screen.blit(pygame.image.load(map_file), (0, 0))
        pygame.display.flip()

    pygame.quit()
    os.remove(map_file)
