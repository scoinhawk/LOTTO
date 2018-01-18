# PROMET V1.0
from bs4 import BeautifulSoup as Soup
from urllib.request import urlopen
from collections import Counter
import re
import csv

PAGENUMBER = 1
ARAWDATA = []
BRAWDATA = []
OFFICIALDATA = {}

while PAGENUMBER <= 83:  # Our way of filtering through pages
    COUNTER = 0  # We will need this later
    url = urlopen('https://www.usamega.com/mega-millions-history.asp?p={}'.format(PAGENUMBER))
    RAW = url.read()  # Reads data into variable
    url.close()  # Closes connection
    PARSED = Soup(RAW, 'html.parser')  # (DATA, Type of Parser)

    for line in PARSED.findAll('td', {'align': 'right'}):  # Finds all the 'td' tags with align:right
        if 'mega-millions-drawing.asp?d=' in str(line):  # Checks if tag has those char
            pRAW = re.findall('d=(.*?)\">', str(line))  # Gathers only the dates from that text
            for pline in pRAW:
                ARAWDATA.append(pline)  # Stores data in list for mutation later

    for line in PARSED.findAll('td', {'align': 'center'}):
        if '<strong>' in str(line) and 'nowrap' in str(line):  # Needs to be setup this long way
            pRAW = re.findall('<b>(.*?)</b>', str(line))
            for pline in pRAW:
                BRAWDATA.append(pline.replace(" · ", " "))

    for date in ARAWDATA:
        OFFICIALDATA[date] = BRAWDATA[COUNTER]  # For every date it will give it value of the numbers
        COUNTER += 1
    PAGENUMBER += 1

with open('lotto.csv', 'w') as data:
    file = csv.writer(data)
    file.writerows(OFFICIALDATA.items())
