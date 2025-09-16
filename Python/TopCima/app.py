import argparse

import redis

from fnc import refresh_database

r = redis.Redis(host="localhost", port=6379, decode_responses=True)

parser = argparse.ArgumentParser(
    description="YouTube media downloader with playlist support.",
)
parser.add_argument("-m", "--movies", type=str, nargs="+", help="Movie(s) to add !")
parser.add_argument("-s", "--series", type=str, nargs="+", help="Serie(s) to add !")

parser.add_argument("-r", "--removes", type=str, nargs="+", help="Serie(s) to remove !")

parser.add_argument(
    "-t",
    "--tvs",
    type=str,
    nargs="+",
    help="Filter playlist videos by title",
)

args = parser.parse_args()

if args.removes:
    for serie in r.smembers("topcima:series"):
        for q in args.removes:
            if q in serie:
                r.srem("topcima:series", serie)
                break

if args.tvs:
    r.sadd("topcima:tvs", *args.tvs)

if args.movies:
    r.sadd("topcima:links", *args.movies)

if args.series:
    r.sadd("topcima:series", *args.series)


refresh_database()
