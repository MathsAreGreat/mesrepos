from fnc import dwn, tolink


qs = []

us = [
    "https://www.faselhds.life/series/%d9%85%d8%b3%d9%84%d8%b3%d9%84-task-%d8%a7%d9%84%d9%85%d9%88%d8%b3%d9%85-%d8%a7%d9%84%d8%a7%d9%88%d9%84",
]

links = [
    "https://www.faselhds.life/hindi/%d9%81%d9%8a%d9%84%d9%85-mrs-chatterjee-vs-norway-2023-%d9%85%d8%aa%d8%b1%d8%ac%d9%85"
]

urls = tolink(us, links)

for link in urls:
    dwn(link, 1)
