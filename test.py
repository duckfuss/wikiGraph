import requests
from bs4 import BeautifulSoup
# remember pip3 install lxml
url = "https://en.wikipedia.org/wiki/Vertebra"
url2 = "https://en.wikipedia.org/wiki/Ulf_L%C3%A5ngbacka"

r = requests.get(url)
soup = BeautifulSoup(r.text, "lxml")

ignoreList = [
            "Old French", "Latin", "Greek", "Ancient Greek", "Grec ancien",
            "Simplified Chinese characters", "Chinese characters", "Traditional Chinese characters",
            "Pinyin", "Help:Pronunciation respelling key", "American English", "Espagnol",
            "Grec (langue)", "language", "langue", "lengua", "言語", "語言", "wikt", "Help:"
        ]

for paragraph in soup.find_all("p"):
    for link in paragraph.find_all("a"):  # type: ignore
        print("\n")
        if link.get("href") is None or link.find_parent("sup") or link.find_parent("tr"): # type: ignore
            # ignore None and superscript (citations)
            continue
        if link.get("class") and "external" in link.get("class"): # type: ignore
            # ignore external links
            continue
        if link.get("title") and any(ig in link.get("title") for ig in ignoreList): # type: ignore
            continue
        print(link.get("class"))  # type: ignore
        print(url.split("/wiki")[0] + link.get("href"))  # type: ignore