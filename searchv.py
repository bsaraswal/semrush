#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import csv
import urllib.parse
from time import sleep

# Constant
SEMRUSH_APIKEY = ''
SEMRUSH_DB = 'fr'

keywords = csv.reader(open("keywords.csv"))
for keyword in keywords:
    try:
        result = requests.get(
            'http://api.semrush.com/'
            '?type=phrase_this'
            '&key=' + SEMRUSH_APIKEY + 
            '&export_columns=Ph,Nq,Cp,Co,Nr'
            '&phrase=' + urllib.parse.quote_plus(keyword[0]) + 
            '&database=' + SEMRUSH_DB
        )
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        print(e)
        sys.exit(1)

    volume = None 
    writer = csv.writer(open("volumes.csv", "a", newline=''), delimiter=';')
     
    if result.text == 'ERROR 50 :: NOTHING FOUND':
        volume = ""
        writer.writerow([keyword[0], volume])  
    else:
        cr = csv.reader(result.text.splitlines(), delimiter=';')
        next(cr, None)  # skip the headers
        for row in cr:
            volume = row[1]
            writer.writerow([keyword[0], volume]) 

    print(keyword[0] + " : " + volume)

    sleep(0.2) # No more 10 SEMRUSH API Requests / second (see : https://fr.semrush.com/api-terms/)
