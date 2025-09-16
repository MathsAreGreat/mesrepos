# import pyfiglet module
import pyfiglet


def sprint(t):
    result = pyfiglet.figlet_format(t)
    print()
    print(result)
    print()


if __name__ == "__main__":
    from pathlib import Path
    import pickle

    p = Path("/home/mohamed/Documents/datas/Spotify")
    t = Path("/home/mohamed/Music/Spotify/Finals/Premp3")
    for f in p.glob("*.albsptf"):
        with open(f, "rb") as fl:
            dt = pickle.load(fl)
        for k, v in dt.items():
            doc = t / k
            if doc.exists():
                print(k)
                print(v)
                print()

    # f = p / "2HZLJwBLZN8etpz2ZvHqlL.arsptf"
    # with open(f, "rb") as fl:
    #     dt = pickle.load(fl)
    # print(dt)
