import requests
from deep_translator import GoogleTranslator
from bs4 import BeautifulSoup
import pandas as pd
import sys
from datetime import datetime
import time
import re

dateTimeObj = datetime.now()
filename = f'Duesseldrof_marketsegmentdata_{dateTimeObj.strftime("%d%m%Y-%H%M")}.xlsx'
Duesseldrofdata = []

headers = {
    "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"}
url = 'https://www.boerse-duesseldorf.de/anleihen/{}'
file = open("./Duesseldrof_allfields.txt")
lines = file.read().splitlines()
file.close()
wkn = str()
market_segment = str()
stammdaten = {}
for Identifier in lines:
    print(Identifier)

    htmlcontent = requests.get(url.format(Identifier), headers=headers, stream=True)
    soup = BeautifulSoup(htmlcontent.text, 'html.parser')

    header = soup.find('h4', class_='mt-50')
    if header:
        ul_element = header.find_next_sibling('ul', class_='list-group')
        if ul_element:
            for item in ul_element.find_all('li'):
                key = item.contents[0].strip()
                value = item.find('span').text.strip()
                stammdaten[key] = value

print(stammdaten)