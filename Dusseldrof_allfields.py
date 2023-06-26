import requests
from deep_translator import GoogleTranslator
from bs4 import BeautifulSoup
import pandas as pd
import sys
from random import randint
from time import sleep
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


for Identifier in lines:
    print(Identifier)

    htmlcontent = requests.get(url.format(Identifier), headers=headers, stream=True)
    sleep(randint(1,5))
    soup = BeautifulSoup(htmlcontent.text, 'html.parser')
    stammdaten = {}
    header = soup.find('h4', class_='mt-50')
    if header:
        ul_element = header.find_next_sibling('ul', class_='list-group')
        if ul_element:
            for item in ul_element.find_all('li'):
                key = item.contents[0].strip()
                value = item.find('span').text.strip()
                stammdaten[key] = value

    translated_stammdaten = {}
    for key, value in stammdaten.items():
        translated_value = GoogleTranslator(source='auto', target='en').translate(value)
        translated_stammdaten[key] = translated_value
    print(translated_stammdaten)
    tempdata = {'ISIN': Identifier,
                'Security Type': translated_stammdaten.get('Wertpapiertyp', 'n/a'),
                'WKN': translated_stammdaten.get('WKN', 'n/a'),
                'Currency': translated_stammdaten.get('Währung', 'n/a'),
                'Notation Unit': translated_stammdaten.get('Notierungseinheit', 'n/a'),
                'Initial Listing': translated_stammdaten.get('Erstnotierung', 'n/a'),
                'Origin': translated_stammdaten.get('Herkunft', 'n/a'),
                'Denomination': translated_stammdaten.get('Stückelung', 'n/a'),
                'Coupon': translated_stammdaten.get('Kupon', 'n/a'),
                'Coupon Type': translated_stammdaten.get('Kupontyp', 'n/a'),
                'Due Date': translated_stammdaten['Fälligkeit'],
                'Previous Coupon': translated_stammdaten.get('Vorheriger Kupon', 'n/a'),
                'Next Coupon': translated_stammdaten.get('Nächster Kupon', 'n/a'),
                'Interest Date': translated_stammdaten.get('Zinstermin', 'n/a')
                }
    Duesseldrofdata.append(tempdata)
df = pd.DataFrame.from_dict(Duesseldrofdata)
print(df)

