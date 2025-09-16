import re
import xml.etree.ElementTree as ET

from pathlib import Path


# Parse the XML file (or string)
tree = ET.parse("/home/mohamed/stream.xspf")
root = tree.getroot()

# Define namespace mapping
ns = {
    "xspf": "http://xspf.org/ns/0/",
    "vlc": "http://www.videolan.org/vlc/playlist/ns/0/",
}

# Find all <track> elements
tracks = root.findall(".//xspf:track", ns)


ids = ["", "bein", "osn ", "art ", "mbc ", "ssc ", " movie", " sport", " news"]
# ids = ["", "bein"]

for ID in ids:
    tts = ["#EXTM3U"]
    ss = []
    name = "stream"
    if ID:
        name = f"{ID.strip()}_stream"
    fn = Path(f"/home/mohamed/Downloads/Files/M3Us/{name}.m3u")
    for t in tracks:
        location = t.find("xspf:location", ns)
        title = t.find("xspf:title", ns)
        if title is None:
            continue
        if location is None:
            continue
        tt = " ".join(e for e in title.text.split(" ") if e)
        if "---" in tt.lower():
            continue
        if ID not in tt.lower():
            continue
        url = location.text.strip()
        ss += [f"#EXTINF:-1,{tt}\n{url}"]
    tts += sorted(ss)
    with fn.open("w") as f:
        f.write("\n".join(tts))


# print([link for link in urls if link not in links])
