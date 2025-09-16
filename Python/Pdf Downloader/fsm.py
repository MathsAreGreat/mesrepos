import Livre2
from concurrent.futures import ThreadPoolExecutor


data = Livre2.fetch()
data += Livre2.fetch("f")
data += Livre2.fetch("e")

print(
    len(data),
    "items !"
)
print(data[:5], "items !")
with ThreadPoolExecutor(10) as executor:
    executor.map(Livre2.vid_download, data)
