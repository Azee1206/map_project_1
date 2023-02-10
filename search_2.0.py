import sys

from geocoder import get_coordinates, get_ll_span
from mapapi_PG import show_map


def main():
    toponym = ' '.join(sys.argv[1:])

    if not toponym:
        print('No data')
    else:
        # longitude, lattitude = get_coordinates(toponym)
        # ll_spn = f"ll={longitude},{lattitude}&spn=0.005,0.005"
        # show_map(ll_spn, 'map')

        ll, spn = get_ll_span(toponym)
        ll_spn = f'll={ll}&spn={spn}'
        point = f"pt={ll},pm2wtl"
        show_map(ll_spn, "map", add_params=point)


if __name__ == '__main__':
    main()