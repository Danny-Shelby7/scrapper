import requests
from bs4 import BeautifulSoup
import re
import os
import shelve
import json

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

# Ouvre le fichier json
with open(r"urls.json") as f:
	file = f.read()

data = json.loads(file)

for name, url in data["urls"].items():
	r = requests.get(url,headers=headers)
	soup = BeautifulSoup(r.content, "html.parser")
	isExist = os.path.exists(dirDb)

	# Créer le dossier s'il n'existe pas
	if not isExist:
		os.makedirs(dirDb)
		
	db_location = os.path.join(dirDb, name)
	db = shelve.open(db_location)

	# Si la requête HTTP retourne une réponse OK,
	# retourner tous les liens contenu sur la page
	if r.status_code == 200:
		print(f"\n{soup.title.string}")
		print(url)
		linkObject = {}
		for link in soup.find_all("a"):
			linkObject[link.text] = link.get("href")
		db["link"] = linkObject
	else:
		exit(0)
