import pygame
import requests
import sys
import os
from button import Button
from search_address import search
from geocoder import get_ll_span


MAP_TYPES = ['map', 'sat', 'sat,skl']


MAP_MOVING_SPEED = 0.24
SPN_CHANGING_SPEED = 0.062
MAX_SPN = 10


def get_map(ll_spn=None, map_type="map", add_params=None, search=False):
    if ll_spn:
        map_request = f"http://static-maps.yandex.ru/1.x/?{ll_spn}&l={map_type}"
    else:
        map_request = f"http://static-maps.yandex.ru/1.x/?l={map_type}"

    if add_params:
        map_request += "&" + add_params
    response = requests.get(map_request)

    if not response:
        if search:
            return 'search_error'
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
    map_file = get_map(ll_spn, map_type, add_params)
    change_map_type_btn_img = pygame.image.load('buttons/change_map_type.png').convert_alpha()
    change_map_type_btn = Button(536, 386, change_map_type_btn_img, 2)
    search_btn_img = pygame.image.load('buttons/find_btn.png').convert_alpha()
    search_btn = Button(0, 386, search_btn_img, 2)
    num_of_points = 1
    run = True
    while run:
        screen.blit(pygame.image.load(map_file), (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        if change_map_type_btn.draw(screen):
            try:
                map_type = MAP_TYPES[MAP_TYPES.index(map_type) + 1]
                map_file = get_map(ll_spn, map_type, add_params)
            except IndexError:
                map_type = MAP_TYPES[0]
                map_file = get_map(ll_spn, map_type, add_params)

        if search_btn.draw(screen):
            new_address = search(screen, map_file)
            if new_address:
                spn = list(map(float, spn.split(',')))
                old_ll, old_spn = ll, spn
                spn = ','.join(map(str, spn))
                old_ll_spn = ll_spn
                ll, spn = get_ll_span(new_address)
                try:
                    spn = list(map(float, spn.split(',')))
                except AttributeError:
                    spn = [0, 0]
                    spn[0], spn[1] = old_spn[0], old_spn[1]
                if spn[0] > MAX_SPN or spn[1] > MAX_SPN:
                    spn[0], spn[1] = old_spn[0], old_spn[1]
                spn = ','.join(map(str, spn))
                ll_spn = f'll={ll}&spn={spn}'
                if ll:
                    if add_params:
                        add_params += f"~{ll},pm2wtl{num_of_points}"
                    else:
                        add_params = f"pt={ll},pm2wtl{num_of_points}"
                if num_of_points != 99:
                    num_of_points += 1
                old_map = map_file
                map_file = get_map(ll_spn, map_type, add_params, search=True)
                if map_file == 'search_error':
                    map_file = old_map
                    ll, spn = old_ll, old_spn
                    ll_spn = old_ll_spn
                    spn = ','.join(map(str, spn))

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
        elif keys[pygame.K_DOWN]:
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
        elif keys[pygame.K_RIGHT]:
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
        elif keys[pygame.K_LEFT]:
            ll = list(map(float, ll.split(',')))
            ll[0] -= MAP_MOVING_SPEED
            if ll[0] > -179:
                ll = ','.join(map(str, ll))
                ll_spn = f'll={ll}&spn={spn}'
                map_file = get_map(ll_spn, map_type, add_params)
            else:
                ll[0] += MAP_MOVING_SPEED
                ll = ','.join(map(str, ll))

        pygame.display.flip()

    pygame.quit()
    os.remove(map_file)
