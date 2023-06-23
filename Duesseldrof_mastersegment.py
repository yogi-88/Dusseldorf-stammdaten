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
file = open("./Duesseldrof.txt")
lines = file.read().splitlines()
file.close()
wkn = str()
market_segment = str()

for Identifier in lines:
    print(Identifier)

    content = requests.get(url.format(Identifier), headers=headers, stream=True)
    soup = BeautifulSoup(content.text, 'html.parser')
    spans = soup.find_all('div', "row-isin-wkn isin-wkn")
    if len(spans) <= 0:
        data_status = 'No'
    else:
        data_status = 'Yes'
    wkn = ""
    market_segment = ""

    for span in spans:
        req_data = span.text
        wkn = (req_data.split("WKN: ",1)[1]).split()[0]
        market_segment = GoogleTranslator(source='auto', target='en').translate(text=(req_data.split("Marktsegment: ",1)[1]))

    tempdata = {'ISIN': Identifier,
                'Security Available': data_status,
                'WKN': wkn,
                'Market Segment': market_segment,
                }
    Duesseldrofdata.append(tempdata)
    df = pd.DataFrame.from_dict(Duesseldrofdata)
    df.to_excel(filename, index=False)









