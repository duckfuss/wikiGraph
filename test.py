import requests
from bs4 import BeautifulSoup
# remember pip3 install lxml
url = "https://en.wikipedia.org/wiki/Mycenaean_Greek"
r = requests.get(url)
soup = BeautifulSoup(r.text, "lxml")

for paragraph in soup.find_all("p"):
    for link in paragraph.find_all("a"): # type: ignore
        if link.get("href") is None: # type: ignore
            continue
        if link.find_parent("sup"):
            continue
        print(url.split("/wiki")[0] + link.get("href")) # type: ignore