# -*- coding: utf-8 -*-
"""
Created on Thu Aug 31 16:31:31 2023

@author: Alessandro
"""
import pandas as pd
from bs4 import BeautifulSoup
import requests

library = pd.DataFrame(columns=["title", "date", "handle", "language", "download"])

for tip in range(1, 6):
    tipology = str(tip)
    print("Processing document type " + tipology)
    link = "https://iczmplatform.org/search?format=" + tipology
    response = requests.get(link)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, "html.parser")

    # Trova tutti gli elementi 'col-sm-4'
    div_library = soup.find_all('div', class_='col-sm-4')

    for element in div_library:
        a_link = element.find('a')
        a_title = element.find('p')
        a_date = element.find('div', class_='text-muted')
        language_elements = element.find_all('span')
    
        # Utilizza una lista per raccogliere i testi delle lingue

    

        # Estrai gli attributi solo se gli elementi esistono
        if a_link:
            a_link = a_link['href']
        else:
            a_link = 'no link'

        if a_title:
            a_title = a_title.text.strip()
        else:
            a_title = 'no title'

        if a_date:
            a_date = a_date.text.strip().split(',')[0]
        else:
            a_date = 'no date'

        if language_elements:
            language_texts = [element.text.strip() for element in language_elements]
            languages = ', '.join(language_texts)
        else:
            languages = 'no language'

        # Aggiungi i dati al DataFrame
        library = library.append({'download': a_link, 'title': a_title, 'date': a_date, 'language': languages}, ignore_index=True)


library.to_excel('PAP_RAC_plan_strategies.xlsx', index=False)