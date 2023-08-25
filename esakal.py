
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

        loc_urls = "https://epaper.esakal.com/smartepaper/Admin/dpadmin/Controller.aspx?a=getlocations"
        html_document = getHTMLdocument(loc_urls)
        soup = BeautifulSoup(html_document, 'html.parser')
        site_json=json.loads(soup.text)
        all_cities_names = [d.get('name') for d in site_json if d.get('name')]

        for city in all_cities_names:
            edition_url = f"https://epaper.esakal.com/smartepaper/Admin/dpadmin/Controller.aspx?a=geteditionsforlocation&locationcode={city}&dt={day}/{month}/{year}"
            html_document = getHTMLdocument(edition_url)
            soup = BeautifulSoup(html_document, 'html.parser')
            site_json=json.loads(soup.text)
            all_edition_names = [d.get('value') for d in site_json if d.get('value')]

            for edition in all_edition_names:
                page_url = f"https://epaper.esakal.com/smartepaper/Admin/dpadmin/Controller.aspx?a=getjson3&pub={city}${edition}&dt={year}-{month}-{day}"
                page_html_document = getHTMLdocument(page_url)
                soup1 = BeautifulSoup(page_html_document, 'html.parser')
                site_json1=json.loads(soup1.text)
                jpg_thumnail_urls = [d.get('thumnailurl') for d in site_json1 if d.get('thumnailurl')]
                # print(jpg_thumnail_urls)

                for url in jpg_thumnail_urls:
                    replace_str1 = '_'.join(url.split('_')[:-1])+'_PR.jpg'
                    replace_str2 = replace_str1.split('//')
                    replace_str3 = '//'.join(replace_str2[:2])
                    replace_str4 = replace_str3+'/'+replace_str2[-1]
                    replace_str4
                    Final_urls.append(replace_str4)

        with open(f'URLS/{lang}/Esakal_{year}_{month}_{day}.txt', 'w+') as f:
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

    file = open(f'URLS/{lang}/Esakal_{year}_{month}_{day}.txt','r')
    url_list = file.readlines()
    for url in url_list:
      try:
        # print(url)
        url = url.replace('\n','')
        response = requests.get(url)

        with open(f"IMAGES/{lang}/Esakal_{year}_{month}_{day}_{uuid.uuid4()}.jpg", "wb") as f:
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


