import requests
from bs4 import BeautifulSoup
import shelve
import csv
import re
import os

dirDb = "db"

with open(r"listURL.csv") as csvFile:
    csvForm = csv.reader(csvFile, delimiter=",")
    for row in csvForm:
        for url in row:
            pattern = re.compile(r'https?://(www\.)?(\w|-)+\.\w+')
            pattern = re.compile(r'https?://(www\.)?([a-zA-Z-0-9]+)(\.\w+/)')
            subbed_url = pattern.sub(r'\2', url)
            r = requests.get(url)
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