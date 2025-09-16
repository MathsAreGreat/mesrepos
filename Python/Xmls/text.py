from Mido.variables import monhtml, print


u = "https://www.alloschool.com/course/mathematiques-1ere-annee-college"

soup = monhtml(u)

links = [
    link.get("href")
    for link in soup.select("a")
    if link.get("href") and "/element/" in link.get("href")
]

pdfs = [link.rsplit("/", 1)[0] for link in links if link.endswith("pdf")]
hts = [link for link in links if not link.endswith("pdf") and link not in pdfs]

for link in hts:
    soup = monhtml(link)
    pdfs += [
        link.get("href")
        for link in soup.select("a")
        if link.get("href") and link.get("href").endswith("pdf")
    ]


print(set(pdfs))
