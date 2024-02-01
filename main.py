import requests
from bs4 import BeautifulSoup
import shelve
import csv
import re
import os

headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://www.google.com/',
            'Alt-Used': 'www.scraperapi.com',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'cross-site',
            'Sec-Fetch-User': '?1',
}


dirDb = "db"

with open(r"listURL.csv") as csvFile:
    csvForm = csv.reader(csvFile, delimiter=",")
    for row in csvForm:
        for url in row:
            pattern = re.compile(r'https?://(www\.)?(\w|-)+\.\w+')
            pattern = re.compile(r'https?://(www\.)?([a-zA-Z-0-9]+)(\.\w+/)')
            subbed_url = pattern.sub(r'\2', url)
            r = requests.get(url,headers=headers)
            soup = BeautifulSoup(r.content, "html.parser")
            isExist = os.path.exists(dirDb)

            if not isExist:
                os.makedirs(dirDb)
            else:
                db = shelve.open(dirDb + "/" + subbed_url + ".db")

                if r.status_code == 200:
                    print(soup.title.string)
                    linkObject = {}
                    for link in soup.find_all("a"):
                        linkObject[link.text] = link.get("href")
                    db["link"] = linkObject
                else:
                    exit(0)
