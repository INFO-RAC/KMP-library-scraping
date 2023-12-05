#!/usr/bin/env python
# coding: utf-8

# In[29]:


import csv
import pandas as pd
from urllib.request import Request,urlopen
from bs4 import BeautifulSoup
import ssl
import requests
ssl._create_default_https_context = ssl._create_unverified_context


# In[72]:


with open('pag_0.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    
    field = ["title", "handle", "download", "language", "date"]
    writer.writerow(field)
    
    url="https://www.unep.org/unepmap/resources/publications?/resources/publications=&/resources/page=0&combine=&field_type_category_target_id=All&field_library_series_target_id=All&field_year_value=&page=0"
    request_site = Request(url, headers={"User-Agent": "Chrome/117.0.0.0"})

    webpage = urlopen(request_site)

    with webpage as fp:
        soup = BeautifulSoup(fp,"html.parser")

    row_list=[]
    title=[]
    date=[]
    handle=[]
    langs=[]
    download=[]
    n=0

    for i in range (0,20):
        title_row=soup.find_all('div', class_='result_item_title')[n].get_text().strip('\n')
        date_row=soup.find_all("div",class_="result_item_meta")[n].get_text().strip('\n')
    
        title.append(title_row)
        date.append(date_row)
    
        if soup.find_all('div', class_='result_item_summary')[n].find('a').attrs['href'].__contains__('bitstream'):
            download_row=soup.find_all('div', class_='result_item_summary')[n].find('a').attrs['href']
            langs_row=soup.find_all('div', class_='result_item_summary')[n].get_text().strip('\n')
        
            download.append(download_row)
            handle.append('None')
            langs.append(langs_row)
        
            row=[title_row,'None',download_row,langs_row,date_row]
        
            print(row)
        
            row_list.append(row)
        
        else:
            handle_row=soup.find_all('div', class_='result_item_summary')[n].find('a').attrs['href'].replace('wedoc.','wedocs.')
        
            handle.append(handle_row)

            try:
                with urlopen(handle_row) as details:
                        soup_details = BeautifulSoup(details,"html.parser")
                all_downloads = soup_details.find_all("a",class_="btn btn-warning text-uppercase",href=True)
                for j in all_downloads:
                    langs_row=j.get_text(strip=True).split(' ')[0]
                    download_row="https://wedocs.unep.org"+j['href'].split('?')[0]
                
                    langs.append(langs_row)
                    download.append(download_row)
                
                    row=[title_row,handle_row,download_row,langs_row,date_row]
                
                    print(row)
                
                    row_list.append(row)
                
            except:
            
                langs_row=langs.append(soup.find_all('div', class_='result_item_summary')[n].get_text().strip('\n'))
            
                langs.append(langs_row)
                download.append("None")
            
                row=[title_row,handle_row,'None',langs_row,date_row]
                
                print(row)
            
                row_list.append(row)     
    
        n=n+1

    writer.writerows(row_list)


# In[ ]:




