from bs4 import BeautifulSoup
import requests
import re
import json
from datetime import date, timedelta
import pandas
import os
import uuid 
import sys

# function to extract html document from given url
def getHTMLdocument(url):
    # request for HTML document of given url
    response = requests.get(url)
    # response will be provided in JSON format
    return response.content

def getAllDates(from_date,to_edate):
  sdate = date(int(from_date.split('/')[2]),int(from_date.split('/')[1]),int(from_date.split('/')[0]))
  edate = date(int(to_edate.split('/')[2]),int(to_edate.split('/')[1]),int(to_edate.split('/')[0]))
  all_dates = pandas.date_range(sdate,edate-timedelta(days=1),freq='d')
  return all_dates


def generatejpgURLS(from_date,to_date ,lang):
    alldates = getAllDates(from_date,to_date)
    for date in alldates:
        Final_urls =[]
        day = '{:02d}'.format(date.day)
        month = '{:02d}'.format(date.month)
        year = str(date.year)

        editions_url = "https://epaper.patrika.com/Home/GetEditionsForSearch"
        html_document = getHTMLdocument(editions_url)
        # create soap object
        soup = BeautifulSoup(html_document, 'html.parser')
        site_json=json.loads(soup.text)
        #printing for entrezgene, do the same for name and symbol
        edition_ids = [d.get('EditionId') for d in site_json if d.get('EditionId')]

        for edition_id in edition_ids:
            # assign required credentials
            # assign URL
            url_to_scrape = f"https://epaper.patrika.com/Home/GetAllpages?editionid={edition_id}&editiondate={day}%2F{month}%2F{year}"
            # create document
            html_document = getHTMLdocument(url_to_scrape)
            # create soap object
            soup = BeautifulSoup(html_document, 'html.parser')
            site_json=json.loads(soup.text)
            #printing for entrezgene, do the same for name and symbol
            jpg_urls = [d.get('XHighResolution') for d in site_json if d.get('XHighResolution')]
            Final_urls.extend(jpg_urls)        
        # print(Final_urls)
        with open(f'URLS/{lang}/Patrika_{year}_{month}_{day}.txt', 'w+') as f:
        # write elements of list
            for items in Final_urls:
                f.write('%s\n' %items)
        print("File written successfully")
        # close the file
        f.close()        
    return True 

def downloadImages(from_date,to_date,lang):
  alldates = getAllDates(from_date,to_date)
  for date in alldates:
    Final_urls =[]
    day = '{:02d}'.format(date.day)
    month = '{:02d}'.format(date.month)
    year = str(date.year)
    file = open(f'URLS/{lang}/Patrika_{year}_{month}_{day}.txt','r')
    url_list = file.readlines()
    for url in url_list:
      try:
        # print(url)
        url = url.replace('\n','')
        response = requests.get(url)
        with open(f"IMAGES/{lang}/Patrika_{year}_{month}_{day}_{uuid.uuid4()}.jpg", "wb") as f:
          f.write(response.content)
          f.close()
      except:
        pass

    file.close()
  return True


from_date = sys.argv[1]
to_date = sys.argv[2]
lang = 'Hindi'

urls_path = f"URLS/{lang}"
imgs_path = f"IMAGES/{lang}"
# Check whether the specified path exists or not
isExist = os.path.exists(urls_path)
if not isExist:
   os.makedirs(urls_path)

isExist = os.path.exists(imgs_path)
if not isExist:
   os.makedirs(imgs_path)

# scrape jpg  URLS into txt file
generatejpgURLS(from_date,to_date,lang)
# download  jpg files using stored  urls in txt files
downloadImages(from_date,to_date,lang)

    
    