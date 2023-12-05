#!/usr/bin/env python
# coding: utf-8

# In[3]:


import csv
import pandas as pd
from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

row_list=[]
with open('pag_601_636.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    
    field = ["title", "date", "handle", "language", "download"]
    writer.writerow(field)
    
    for pag in range(601,637):
        page = str(pag)
        print("Processing page no. "+page)
        with urlopen("https://wedocs.unep.org/discover?rpp=10&etal=0&group_by=none&page="+page+"&filtertype_0=has_content_in_original_bundle&filtertype_1=author&filter_relational_operator_1=equals&filter_relational_operator_0=equals&filter_1=UNEP%2FMAP&filter_0=true") as fp:
            soup = BeautifulSoup(fp,"html.parser")
        titles=soup.find_all("h4")

        for ti in titles:
            ti.span.unwrap()
        
#       date=soup.find_all("span",class_="date")
        
        hand=soup.find_all("a",class_="image-link",href=True)

        for ha in hand:
            ha.img.unwrap()
        
        n=0
        
        for j in hand:
            
            #extract correct date passing for pandas
            with urlopen("https://wedocs.unep.org/"+j['href']+"?show=full") as meta_date:
                date_details = BeautifulSoup(meta_date,"html.parser")
 
            table=date_details.find("table",{"class":"table table-bordered table-striped table-hover"})
            rows=table.find_all("tr")
            data=[[td.text.strip() for td in row.find_all("td")] for row in rows[1:]]
            df=pd.DataFrame(data,columns=["namepar","valuepar","other"])
            if "dc.date.issued" in df["namepar"].unique():
                value=list(df.query('namepar == "dc.date.issued"')["valuepar"])[0]
            elif "dc.date" in df["namepar"].unique():
                value=list(df.query('namepar == "dc.date"')["valuepar"])[0]
            else:
                value=''
            #done--------
            
    
            with urlopen("https://wedocs.unep.org/"+j['href']) as details:
                soup_details = BeautifulSoup(details,"html.parser")
    
            down=soup_details.find_all("a",class_="btn btn-warning text-uppercase",href=True)
    
            for i in down:
                row=[titles[n].get_text(strip=True),value,"https://wedocs.unep.org/"+j['href'],i['href'].split('.pdf')[0][-3:],'https://wedocs.unep.org/'+i['href'].split('?')[0]]
                row_list.append(row)
            
            n=n+1

    writer.writerows(row_list)


# In[ ]:




