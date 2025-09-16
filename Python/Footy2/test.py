from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

cols = [
    "#00ff00", 'red',
    'green', 'yellow',
    'blue', 'magenta',
    'cyan', 'white'
]


def monhtml(k):
    sess = requests.session()
    sess.headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
    }
    r = sess.get(k, allow_redirects=True)
    encoding = r.encoding if 'charset' in r.headers.get(
        'content-type', '').lower() else None
    parser = 'html.parser'
    return BeautifulSoup(r.content, parser, from_encoding=encoding)


u = "https://www.sendgb.com/9EZ5BO2fopY"

soup = monhtml(u)

us = [e["href"] for e in soup.findAll("a") if e.get(
    "href") and "one.php" in e.get("href")]

url = urljoin(u, us[0])

sess = requests.session()
sess.headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
}
r = sess.get(url, stream=True)

print(r.headers)
