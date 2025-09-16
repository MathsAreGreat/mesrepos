

from bs4 import BeautifulSoup
import requests


r = requests.get("https://www.footarchives.com")
soup = BeautifulSoup(r.text, 'html.parser')

articles = soup.select(".Posts-byCategory > article")

for article in articles:
    link = article.a
    u = link.get('href')
    imgSrc = article.select_one("img.post-thumb").get('data-src')
    tt = link.get('title')
    print(tt)
    print(imgSrc)
    print()
