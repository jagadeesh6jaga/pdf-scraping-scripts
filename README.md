# pdf-scraping-scripts

## Follow the below steps to run the scripts:

-> pip install -r requirements.txt

#### 1) esakal :

-> python3 esakal.py from_date to_date  (EX : python3 esakal.py '24/12/2022' '30/12/2022')

#### 2) patrika :

-> python3 patrika.py from_date to_date  (EX : python3 patrika.py '24/12/2022' '30/12/2022')

#### 3) timesGroup :

-> python3 timesGroup.py from_date to_date  (EX : python3 timesGroup.py '24/12/2022' '30/12/2022')


#### 4) mathrubhumi

-> python3 mathrubhumi.py from_date to_date  (EX : python3 mathrubhumi.py '24/12/2022' '30/12/2022')

##### Note :
* Here  for above 4 files  date format should be in 'dd/mm/yyyy' 
* it will exclude the 'to_date'

  ( example if we provoid the from_date as  01/01/2023 and to_date as  15/01/2023  , it will process the date from  01/01/2023 to 14/01/2023  it will exclude the 15/01/2023)



#### 5) anandabazar

python newspaperScrapper.py anandabazar from_date to_date(EX:  python newspaperScrapper.py anandabazar 2023-08-24 2023-08-26)

#### 6) vijayvani

python newspaperScrapper.py vijayvani from_date to_date  (EX : python newspaperScrapper.py vijayvani 2023-08-24 2023-08-25)

##### Note

* in 5 and 6 we should pass the date format as 'yyyy-mm-dd'
