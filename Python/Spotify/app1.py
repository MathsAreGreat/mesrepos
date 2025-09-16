import os

# dpath = "/home/mohamed/Music/Spotify/Finals"

# for c, _, files in os.walk(f"{dpath}/Gadhom"):
#     for f in files:
#         if ").mp3" in f:
#             nbr = f.split("(")[-1].split(')')[0]
#             o = f"PreMp3/{nbr}"
#             to = f"{dpath}/{o}"
#             os.makedirs(to, exist_ok=True)
#             os.rename(
#                 f"{c}/{f}",
#                 f"{to}/{f}"
#             )


def audio(nbr):
    u = f"https://open.spotify.com/track/{nbr}"
    o = f"/home/mohamed/Music/PreMp3/{nbr}"
    cmd = f'spotify_dl -ml {u} -o "{o}"'
    os.system(cmd)


audio("1lGBN8yd5qodDJ8Q1NTWqT")
