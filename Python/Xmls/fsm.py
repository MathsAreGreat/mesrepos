from pathlib import Path
import requests
import xml.etree.ElementTree as ET

# # YouTube channel RSS feed URL
# url = "https://www.youtube.com/feeds/videos.xml?channel_id=UCXuqSBlHAE6Xw-yeJA0Tunw"

# # Fetch XML content
# response = requests.get(url)
# response.raise_for_status()
# xml_data = response.content

# with Path("content.xml").open("wb") as el:
#     el.write(xml_data)

with Path("content.xml").open("rb") as el:
    xml_data = el.read()

# Parse XML
root = ET.fromstring(xml_data)

# Namespaces used in YouTube RSS feeds
ns = {
    "atom": "http://www.w3.org/2005/Atom",
    "media": "http://search.yahoo.com/mrss/",
    "yt": "http://www.youtube.com/xml/schemas/2015",
}

# Extract feed title
title = root.find("atom:title", ns).text
print("Feed Title:", title)
print()

# Extract video entries
i = 1
for entry in root.findall("atom:entry", ns):
    video_title = ": " + entry.find("atom:title", ns).text
    video_link = ": " + entry.find("media:group/media:thumbnail", ns).attrib["url"]
    published = ": " + entry.find("atom:published", ns).text
    video_id = ": " + entry.find("yt:videoId", ns).text
    channelId = ": " + entry.find("yt:channelId", ns).text
    ds = 50
    print(f"Channel ID {channelId:<{ds}}")
    print(f"Video ID {video_id:<{ds}}")
    # print(f"Title {video_title:>{ds}}")
    # print(f"Link {video_link:>{ds}}")
    # print(f"Published {published:>{ds}}")
    print()
    i += 1
