import time
from bs4 import BeautifulSoup
import requests, csv
import pandas as pd
from fake_useragent import UserAgent
import proxyLister

def vacationScraper(checkin, checkout, group_adults, group_children, no_rooms):

    start = time.time()

    proxyList = proxyLister.mainList
    print(f'Proxies list updated after {int(time.time() - start)} seconds!\n{len(proxyList)} proxies availables')

    urlParis = 'https://www.booking.com/searchresults.es.html'\
        '&lang=en'\
        '&sb=1'\
        '&src_elem=sb'\
        '&src=searchresults'\
        '&dest_id=-1456928'\
        '&dest_type=city'\
        '&ac_position=0'\
        '&ac_click_type=b'\
        '&ac_langcode=en'\
        '&ac_suggestion_list_length=5'\
        '&search_selected=true'\
        f'&checkin={checkin}'\
        f'&checkout={checkout}'\
        f'&group_adults={group_adults}'\
        f'&no_rooms={no_rooms}'\
        f'&group_children={group_children}'\
        '&sb_travel_purpose=leisure'\
        '&order=bayesian_review_score'\
        '&top_currency=1'\
        '&nflt=ht_id%3D204'
    
    urlLondon = 'https://www.booking.com/searchresults.es.html?'\
        '&lang=en'\
        '&sb=1'\
        '&src_elem=sb'\
        '&src=searchresults'\
        '&dest_id=-2601889'\
        '&dest_type=city'\
        '&ac_click_type=b'\
        '&ac_langcode=en'\
        '&ac_suggestion_list_length=5'\
        '&search_selected=true'\
        f'&checkin={checkin}'\
        f'&checkout={checkout}'\
        f'&group_adults={group_adults}'\
        f'&no_rooms={no_rooms}'\
        f'&group_children={group_children}'\
        '&sb_travel_purpose=leisure'\
        '&order=bayesian_review_score'\
        '&top_currency=1'\
        '&nflt=ht_id%3D204'

    urlRome = 'https://www.booking.com/searchresults.es.html?'\
        '&lang=en'\
        '&sb=1'\
        '&src_elem=sb'\
        '&src=searchresults'\
        '&dest_id=-126693'\
        '&dest_type=city'\
        '&ac_click_type=b'\
        '&ac_langcode=en'\
        '&ac_suggestion_list_length=5'\
        '&search_selected=true'\
        f'&checkin={checkin}'\
        f'&checkout={checkout}'\
        f'&group_adults={group_adults}'\
        f'&no_rooms={no_rooms}'\
        f'&group_children={group_children}'\
        '&sb_travel_purpose=leisure'\
        '&order=bayesian_review_score'\
        '&top_currency=1'\
        '&nflt=ht_id%3D204'

    ua = UserAgent()
    
    for proxy in proxyList:
        
        try:
            parisR = requests.get(urlParis, headers={'User-Agent': str(ua.chrome)}, proxies={'http': proxy, 'https': proxy}, timeout=2)
        except:
            proxyList.remove(proxy)
            print(f'Proxy iteration failed, {len(proxyList)} proxies left')
            continue
        
        if parisR.status_code == 200:
            print(f'Paris scrapped after {int(time.time() - start)} seconds!')
            break
        proxyList.remove(proxy)
        print(f'Proxy with no response, {len(proxyList)} proxies left')
        continue


    for proxy in proxyList:
        
        try:
            londonR = requests.get(urlLondon, headers={'User-Agent': str(ua.chrome)}, proxies={'http': proxy, 'https': proxy}, timeout=2)
        except:
            proxyList.remove(proxy)
            print(f'Proxy iteration failed, {len(proxyList)} proxies left')
            continue
        
        if londonR.status_code == 200:
            print(f'London scrapped after {int(time.time() - start)} seconds!')
            break
        proxyList.remove(proxy)
        print(f'Proxy with no response, {len(proxyList)} proxies left')
        continue

    for proxy in proxyList:
        
        try:
            romeR = requests.get(urlRome, headers={'User-Agent': str(ua.chrome)}, proxies={'http': proxy, 'https': proxy}, timeout=2)
        except:
            proxyList.remove(proxy)
            print(f'Proxy iteration failed, {len(proxyList)} proxies left')
            continue
        
        if romeR.status_code == 200:
            print(f'Rome scrapped after {int(time.time() - start)} seconds!')
            break
        proxyList.remove(proxy)
        print(f'Proxy with no response, {len(proxyList)} proxies left')
        continue


    destinationList = [parisR, londonR, romeR]

    parisDf = pd.DataFrame()
    londonDf = pd.DataFrame()
    romeDf = pd.DataFrame()

    for r in destinationList:

        soup = BeautifulSoup(r.content, 'html.parser')

        names = soup.find_all(attrs={'class': 'a23c043802'})
        names = [name.text for name in names]

        prices = soup.find_all(attrs={'class': 'bd73d13072'})
        prices = [price.text for price in prices]

        scores = soup.find_all(attrs={'class': 'd10a6220b4'})
        scores = [score.text for score in scores]

        places = soup.find_all(attrs={'data-testid': 'address'})
        places = [place.text for place in places]

        if r == parisR:
            parisDf['name'] = names
            parisDf['price'] = prices
            parisDf['score'] = scores
            parisDf['place'] = places
            parisDf['city'] = 'Paris'

        if r == londonR:
            londonDf['name'] = names
            londonDf['price'] = prices
            londonDf['score'] = scores
            londonDf['place'] = places
            londonDf['city'] = 'London'

        if r == romeR:
            romeDf['name'] = names
            romeDf['price'] = prices
            romeDf['score'] = scores
            romeDf['place'] = places
            romeDf['city'] = 'Rome'

        
        print(f'Iteration over destination after {int(time.time() - start)} seconds!')

        df = pd.concat([londonDf, parisDf, romeDf], ignore_index=True)
        df = df.sort_values(by=['score'], ascending=False)
        df = df.reset_index(drop=True)
        

    return df