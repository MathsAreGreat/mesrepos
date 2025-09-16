from fnc import db_update, get_links

nb = 1

ks = [
    "9-ruler-s-crown",
    "dandadan",
    "futari-solo-camp",
    "guimi-zhi-zhu-xiaochou-pian",
    "hibike-euphonium",
    "hikaru-ga-shinda-natsu",
    "kakkou-no-iinazuke",
    "kanojo-okarishimasu",
    "kaoru-hana-wa-rin-to-saku",
    "long-zu",
    "mattaku-saikin",
    "mikadono-sanshimai",
    "muchuu-sa-kimi-ni",
    "sakamoto-days",
    "seishun-buta-yarou",
    "silent-witch-chinmoku",
    "sono-bisque-doll",
    "summer-pockets",
    "tate-no-yuusha",
    "tsuihousha-shokudou",
    "turkey",
    "ruri-no-houseki",
    "gachiakuta",
    "zutaboro-reijou-wa",
    "witch-watch",
    "yofukashi-no-uta",
    "your-forma",
    "yuusha-party",
    "hotel-inhumans",
    "bullet-bullet",
    "grand-blue",
    "jidou-hanbaiki",
    "hundred-memories",
    "astro-note",
]


fs = [e for e in ks if e.strip()]

db_update(5)

get_links(*fs)
db_update()
