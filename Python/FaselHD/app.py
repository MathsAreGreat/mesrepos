from fnc import dwn, tolink


qs = []

us = [
    "https://www.faselhds.life/series/%d9%85%d8%b3%d9%84%d8%b3%d9%84-task-%d8%a7%d9%84%d9%85%d9%88%d8%b3%d9%85-%d8%a7%d9%84%d8%a7%d9%88%d9%84",
]

links = []

urls = tolink(us, links)

for link in urls:
    dwn(link, 1)
