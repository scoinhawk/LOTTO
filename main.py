# Christopher M. Bradley
# Version 1.0
from bs4 import BeautifulSoup as Soup
from urllib.request import urlopen
from collections import Counter
import re
import csv

pageNumber = 1
rawDataA = []
rawDataB = []
DATA = {}

while pageNumber <= 1:  # Change value based on how far back you want to go in (pages)
    counter = 0
    url = urlopen('https://www.usamega.com/mega-millions-history.asp?p={}'.format(pageNumber))
    uRaw = url.read()
    url.close()
    uSoup = Soup(uRaw, "html.parser")

    for line in uSoup.findAll('td', {'align': 'right'}):
        if 'mega-millions-drawing.asp?d=' in str(line):
            raw = re.findall("d=(.*?)\">", str(line))
            for u in raw:
                rawDataA.append(u)

    for line in uSoup.findAll('td', {'align': 'center'}):
        if '<strong>' in str(line) and 'nowrap' in str(line):
            raw = re.findall("<b>(.*?)</b>", str(line))
            for u in raw:
                rawDataB.append(u.replace(" · ", " "))

    for value in rawDataA:
        DATA[value] = rawDataB[counter]
        counter += 1

    pageNumber += 1

with open('lotto.csv', 'w') as data:
    file = csv.writer(data)
    file.writerows(DATA.items())


def probability(list):
    BUFFED = []
    for i in list:
        buffer = i.split()
        for b in buffer:
            BUFFED.append(b)
    STORE = Counter(BUFFED)
# Uncomment if you want to see DATA in terminal
#    for key, value in STORE.items():
#        print('NUMBER: {0} | OCCURRED: {1} times'.format(key, value))
    with open('occurrence.csv', 'w') as data:
        file = csv.writer(data)
        file.writerows(STORE.items())


probability(rawDataB)

# Uncomment if you want to see DATA in terminal
# for key, value in DATA.items():
#   print('DATE: {0} | TICKET#: {1}'.format(key, value))
