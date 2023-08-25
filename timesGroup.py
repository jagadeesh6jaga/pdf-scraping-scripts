# import necessary libraries
from bs4 import BeautifulSoup
import requests
import re
import json
import pandas
from datetime import date, timedelta
import os
import requests
from PIL import Image
from io import BytesIO
import uuid
import sys



#get all dates between given range excluding end date
#dates should be in dd/mm/yyyy format
def getAllDates(from_date,to_edate):
  sdate = date(int(from_date.split('/')[2]),int(from_date.split('/')[1]),int(from_date.split('/')[0]))
  edate = date(int(to_edate.split('/')[2]),int(to_edate.split('/')[1]),int(to_edate.split('/')[0]))
  all_dates = pandas.date_range(sdate,edate-timedelta(days=1),freq='d')
  return all_dates
    
# function to extract html document from given url
def getHTMLdocument(url):
    # request for HTML document of given url
    response = requests.get(url)
    # response will be provided in JSON format
    return response.content

def generatejpgURLS(from_date,to_date ,lang):
  alldates = getAllDates(from_date,to_date)
  for date in alldates:
    Final_urls =[]
    day = '{:02d}'.format(date.day)
    month = '{:02d}'.format(date.month)
    year = str(date.year)
    #city codeds
    #mtnag (Nagpur) , mtm (mumbai) , mtag (Aurangabad) , mtnk (nasik)  ,mtpe (pune) 
    city_codes = ['mtnag','mtm','mtag','mtnk','mtpe'] 

    for city_code in city_codes:
        # assign URL
        url_to_scrape = f"https://asset.harnscloud.com/PublicationData/MT/{city_code}/{year}/{month}/{day}/DayIndex/{day}_{month}_{year}_{city_code}.json"
        # print(url_to_scrape)
        # create document
        html_document = getHTMLdocument(url_to_scrape)
        # create soap object
        soup = BeautifulSoup(html_document, 'html.parser')
        try:
          site_json=json.loads(soup.text)
          # printing for entrezgene, do the same for name and symbol
          page_names = [d.get('PageName') for d in site_json["DayIndex"] if d.get('PageName')]

          for page in page_names:
            replace_str1 = '/'.join(url_to_scrape.split('/')[:-2])
            replace_str2 = replace_str1+'/Page/'+page+'.jpg'
            Final_urls.append(replace_str2)
        except Exception as exc:
          pass
          # print(replace_str2)

    with open(f'URLS/{lang}/TimesGroup_{year}_{month}_{day}.txt', 'w+') as f:
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
    file = open(f'URLS/{lang}/TimesGroup_{year}_{month}_{day}.txt','r')
    url_list = file.readlines()
    for url in url_list:
      try:
        # print(url)
        url = url.replace('\n','')
        response = requests.get(url)

        with open(f"IMAGES/{lang}/TimesGroup_{year}_{month}_{day}_{uuid.uuid4()}.jpg", "wb") as f:
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
