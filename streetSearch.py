#!/usr/bin/env python

#import BeautifulSoup
from bs4 import BeautifulSoup 
import urllib
import pandas as pd
import pandas as np
import re
import time
from random import randint

#URL Generated in street easy by setting desired filters
FILTER_URL='http://streeteasy.com/for-rent/nyc/price:2600-3200%7Carea:115,158,113,119,139,135,%7Cbeds%3E=1?page='
PREV_RESULT_FOLDER= 'results/'
NUM_PAGES=50

aptsAll={}
aptsSel={}

def package_url_rent(page):
    return FILTER_URL + page

def load_prev_results():
    with open(PREV_RESULT_FOLDER + '/aptsAll', 'r') as f,  open(PREV_RESULT_FOLDER + '/aptsSel', 'r') as f1:
        for line in f1:
            line = line.strip("http://streeteasy.com/").strip()
            aptsSel[line] = 1
        for line in f:
            line = line.strip("http://streeteasy.com/").strip()
            aptsAll[line] = 1
            
def find_new_results():
    found_new = 0
    skipped = 0
    total = 0
    for x in range(1,NUM_PAGES): #loop through pages
        url=package_url_rent(str(x))
        r = urllib.urlopen(url).read()
        soup = BeautifulSoup(r,'html.parser')
        for a in soup.find_all('a', href=True):
            link = a['href']
            found = re.match(r'/building', link)
            link = link.strip()
            total = total + 1
            if found:
                if link.strip() in aptsAll.keys():
                    skipped = skipped + 1
                else:
                    found_new = found_new + 1
                    apts[link] = 1
                    aptsAll[link] = 1
        # Adding delay
        time.sleep(randint(1,3))

    with open('aptsAll', 'w') as f,  open('aptsSel', 'w') as f1:
        for link in apts:
            link = "http://streeteasy.com/" + link
            f.write(link+ '\n')  

            r = urllib.urlopen(link).read()
            soup = BeautifulSoup(r,'html.parser')
            mydivs = soup.findAll("div", { "class" : "details_info" })
            for div in mydivs:
                # Put all desired move in date relevent strings here 
                found1 = ('May' in str(div))
                found2 = ('05/01/' in str(div))
                found3 = ('5/1/' in str(div))
                found4 = ('04/15' in str(div))
                found5 = ('4/2' in str(div))
                found6 = ("04/1" in str(div))
                if found1 or found2 or found3 or found4 or found5 or found6:
                    f1.write(link+'\n')
                    break
            # Adding delay 
            time.sleep(1)

if __name__ == '__main__':
    load_prev_results()
    find_new_results()
    print 'done'
