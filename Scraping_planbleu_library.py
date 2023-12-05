# -*- coding: utf-8 -*-
"""
Created on Thu Aug 31 16:31:31 2023

@author: Alessandro
"""
import pandas as pd
from bs4 import BeautifulSoup
import requests

library = pd.DataFrame(columns=["title", "date", "handle", "language", "download", 'document_type'])

for tip in range(2, 48):
    page = str(tip)
    print("Processing page= " + page)
    link = "https://planbleu.org/en/publications/?wpv_view_count=3696&annee=all&wpv_aux_current_post_id=7419&wpv_aux_parent_post_id=7419&wpv_paged=" + page
    response = requests.get(link)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, "html.parser")

    # Trova tutti gli elementi 'col-sm-4'
    div_library = soup.find_all('div', class_='publi-droite')



    for element in div_library:
        a_handle = element.find('a')
        a_title = element.find('a')
        a_date = element.find('span', class_='meta')
       
        # Utilizza una lista per raccogliere i testi delle lingue

    

        # Estrai gli attributi solo se gli elementi esistono
        if a_handle:
            a_handle = a_handle['href']
        else:
            a_handle = 'no link'

        if a_title:
            a_title = a_title.text.strip()
        else:
            a_title = 'no title'

        if a_date:
            a_date = a_date.text.strip().split(',')[0]
        else:
            a_date = 'no date'

        # Aggiungi i dati al DataFrame
        library = library.append({'handle': a_handle, 'title': a_title, 'date': a_date, 'document_type': 'pubblication'}, ignore_index=True)


library.to_excel('Plan_bleau_library_scraping_draft.xlsx', index=False)

#sostituire il link con quello per il download

df_planbleau=pd.read_excel('Plan_bleau_library_scraping_draft.xlsx')

library_complete = pd.DataFrame(columns=["title", "date", "handle", "language", "download", 'document_type'])
for index,row in df_planbleau.iterrows():
    link_sub=row['handle']
    response_sub = requests.get(link_sub)
    response_sub.raise_for_status()
    soup_sub = BeautifulSoup(response_sub.content, "html.parser")
    
    div_links = soup_sub.find_all('div', class_='files-container')
    for element_sub in div_links:
        a_links=element_sub.find_all('a')
        for a_link in a_links:
            a_handle=link_sub
            a_title=row['title']
            a_date = row['date']
            if a_link:
                a_link=a_link['href']
            else:
                a_link='no_link'

        # Aggiungi i dati al DataFrame

            library_complete = library_complete.append({'handle': a_handle, 'title': a_title, 'date': a_date, 'document_type': 'pubblication','download': a_link}, ignore_index=True)

library_complete.to_excel('Plan_bleau_library_scraping_complete.xlsx', index=False)
        