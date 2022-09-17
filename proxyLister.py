import requests
from bs4 import BeautifulSoup
import pandas as pd

r = requests.get('https://free-proxy-list.net/')
soup = BeautifulSoup(r.content, 'html.parser')
table = soup.find_all('table')
df = pd.read_html(str(table))[0]
df = df[df['Https'] == 'yes']
proxyList = df['IP Address'] + ':' + df['Port'].astype('str')

mainList = proxyList

mainList = mainList.drop_duplicates()
mainList = mainList.reset_index(drop=True)
toDrop = []

for i in range(len(mainList)):
    try:
        r = requests.get('https://httpbin.org/ip', proxies={'http': mainList.iloc[i], 'https': mainList.iloc[i]}, timeout=2)
        break
    except:
        toDrop.append(i)
        continue

mainList = mainList.drop(toDrop)
mainList = list(mainList)