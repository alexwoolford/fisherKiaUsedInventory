#!/usr/bin/env python

import urllib2
from bs4 import BeautifulSoup
import time
import json
import pickle

def inventorySnapshot():

    try:
        with open('fisherkia.pickle', 'rb') as fp:
            records = pickle.load(fp)
            fp.close()
    except:
        records = []

    html = urllib2.urlopen('http://www.fisherkia.net/used-inventory-sheet/').read()
    soup = BeautifulSoup(html)
    table = soup.find('table', {'class':'table'})
    header = [header.text for header in table.findAll('th')]

    for tr in table.findAll('tr'):
        record = dict(zip(header, [td.text for td in tr.findAll('td')]))
        record['ts'] = int(time.time())
        if len(record) > 1:
            records.append(record)

    with open('fisherkia.pickle', 'wb') as fp:
        pickle.dump(records, fp)
        fp.close()

if __name__ == "__main__":
    inventorySnapshot()
