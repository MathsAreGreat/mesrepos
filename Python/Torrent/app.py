import re
import time
from pathlib import Path

import libtorrent as lt
from Mido.variables import monhtml, run_tasks, upclear


uns = [
    f.stem.rsplit(".", 1)[0]
    for f in Path("/home/mohamed/Downloads/Files/Torrents").rglob("*.torrent")
]


def dwn_torrent(magnet_link, titre):
    # Start session
    ses = lt.session({"listen_interfaces": "0.0.0.0:6881"})

    # Create add_torrent_params
    params = lt.add_torrent_params()
    params.save_path = "."
    params.storage_mode = lt.storage_mode_t.storage_mode_sparse
    params.url = magnet_link

    handle = ses.add_torrent(params)

    print("Fetching metadata...")
    tries = 0
    stop = 1
    while tries < 10:
        if torrent_info := handle.torrent_file():
            stop = 0
            break
        time.sleep(1)
        tries += 1

    if stop:
        return 0

    sz = torrent_info.total_size()
    filename = Path(f"Files/{titre}.[{sz:010}].torrent")
    # Save .torrent file
    input_file = torrent_info.name()
    thefile = Path(input_file)
    if not filename.exists():
        with filename.open("wb") as f:
            f.write(lt.bencode(lt.create_torrent(torrent_info).generate()))

    print(f"Torrent metadata saved to {filename}")
    thefile.unlink(missing_ok=True)
    return 1


def dwn_torrent2(magnet_link, titre):
    ses = lt.session()
    output_path = "/home/mohamed/Downloads/Files/Torrents"
    # New way to add magnet URI (non-deprecated)
    print("Adding magnet link ...")
    atp = lt.add_torrent_params()
    atp = lt.parse_magnet_uri(magnet_link)
    atp.save_path = output_path
    handle = ses.add_torrent(atp)
    nb = 1
    while not handle.torrent_file() and nb < 30:
        print(f"{upclear}Fetching", "." * (nb % 10))
        nb += 1
        time.sleep(0.3)
        continue
    # Get torrent info
    torrent_info = handle.torrent_file()  # Updated method

    # Generate and save the torrent file
    torrent_data = lt.create_torrent(torrent_info)

    sz = torrent_info.total_size()

    filename = Path(f"{output_path}/{titre}.[{sz:010}].torrent")

    with open(filename, "wb") as f:
        f.write(lt.bencode(torrent_data.generate()))


url = "https://en.yts-official.org/episodes/landman-2024-season-1-episode-1"
url = "https://en.yts-official.org/episodes/shameless-2011-season-11-episode-1"
soup = monhtml(url)
t = soup.find(id="movie-info").h1.text
ts = re.findall(r"[0-9a-z]+", t, flags=re.IGNORECASE)
titre = ".".join(ts)
trs = soup.select_one(".table").select("tr")
links = [
    (magnet_link, f"[{nb:03}].{titre}.{tr.find('td').text.strip()}")
    for nb, tr in enumerate(trs)
    if (link := tr.a)
    if tr.find("td")
    if (magnet_link := link.get("href"))
    if f"[{nb:03}].{titre}.{tr.find('td').text.strip()}" not in uns
]

run_tasks(dwn_torrent, links, 1)
