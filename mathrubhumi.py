# import necessary libraries
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

#get dates between given range
def getAllDates(from_date,to_edate):
  sdate = date(int(from_date.split('/')[2]),int(from_date.split('/')[1]),int(from_date.split('/')[0]))
  edate = date(int(to_edate.split('/')[2]),int(to_edate.split('/')[1]),int(to_edate.split('/')[0]))
  all_dates = pandas.date_range(sdate,edate-timedelta(days=1),freq='d')
  return all_dates

### get available editions for perticular date
# available_edition_ids =[]
# for i in range(0,120):
#   editionid_url = f"https://epaper.mathrubhumi.com/Home/GetAllSupplement?edid={i}&EditionDate=25%2F08%2F2023"
#   html_document = getHTMLdocument(editionid_url)
#   soup = BeautifulSoup(html_document, 'html.parser')
#   site_json=json.loads(soup.text)
#   if len(site_json)>0:
#     jpg_urls = [d.get('EditionId') for d in site_json if d.get('EditionId')]
#     available_edition_ids.extend(jpg_urls)



def generatejpgURLS(from_date,to_date ,lang):
    alldates = getAllDates(from_date,to_date)
    for date in alldates:
        Final_jpg_urls =[]
        day = '{:02d}'.format(date.day)
        month = '{:02d}'.format(date.month)
        year = str(date.year)


        #currently available editions
        available_edition_ids = [2, 5, 12, 4, 140, 119, 6, 23, 24, 22, 19, 9, 14, 11, 15, 8, 16, 13, 17, 18, 33, 31, 36, 34, 123, 39, 38, 42,\
        40, 49, 46, 50, 139, 48, 44, 47, 127, 55, 57, 52, 53, 56, 51, 128, 58, 59, 136, 137, 64, 61, 60, 62, 69, 65, 66,\
        67, 68, 130, 71, 72, 73, 74, 75, 76, 77, 78, 26, 30, 28, 29, 126, 96, 25]

        for edition in available_edition_ids:
            editions_url = f"https://epaper.mathrubhumi.com/Home/GetAllpages?editionid={edition}&editiondate={day}%2F{month}%2F{year}"
            html_document = getHTMLdocument(editions_url)
            # create soap object
            soup = BeautifulSoup(html_document, 'html.parser')
            site_json=json.loads(soup.text)
            #printing for entrezgene, do the same for name and symbol
            jpg_urls = [d.get('HighResolution') for d in site_json if d.get('HighResolution')]
            hight_res_imgs_urls = [url.replace('_mr','')for url in jpg_urls]
            Final_jpg_urls.extend(hight_res_imgs_urls)

        # print(Final_urls)
        with open(f'URLS/{lang}/mathrubhumi_{year}_{month}_{day}.txt', 'w+') as f:
        # write elements of list
            for items in Final_jpg_urls:
                f.write('%s\n' %items)
        print("File written successfully")
        # close the file
        f.close()        
    return True

def downloadImages(from_date,to_date,lang):
  alldates = getAllDates(from_date,to_date)
  for date in alldates:
    day = '{:02d}'.format(date.day)
    month = '{:02d}'.format(date.month)
    year = str(date.year)
    file = open(f'URLS/{lang}/mathrubhumi_{year}_{month}_{day}.txt','r')
    url_list = file.readlines()
    file.close()
    for url in url_list:
      try:
        # print(url)
        url = url.replace('\n','')
        response = requests.get(url)
        with open(f"IMAGES/{lang}/mathrubhumi_{year}_{month}_{day}_{uuid.uuid4()}.jpg", "wb") as f:
          f.write(response.content)
          f.close()
      except:
        pass

  return True


from_date = sys.argv[1]
to_date = sys.argv[2]
lang = 'Malayalam'

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


