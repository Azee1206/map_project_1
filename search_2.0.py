from geocoder import get_ll_span
from mapapi_PG import show_map


ADDRESS = 'Россия, Кириши, Ленинградская 6'


def main():
    ll, spn = get_ll_span(ADDRESS)
    ll_spn = f'll={ll}&spn={spn}'
    show_map(ll, spn, ll_spn, "map")


if __name__ == '__main__':
    main()