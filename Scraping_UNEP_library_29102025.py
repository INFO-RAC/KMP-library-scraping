from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import time
import random
from urllib.parse import urljoin
import pandas as pd
import csv


row_list=[]
with open('pag_691_719.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    
    field = ["title", "date", "handle", "language", "download"]
    writer.writerow(field)
    
    for pag in range(691,720):
        page = str(pag)
        print("Processing page no. "+page)
        req = Request(
            url='https://wedocs.unep.org/discover?rpp=10&etal=0&group_by=none&page='+page+'&filtertype_0=has_content_in_original_bundle&filtertype_1=author&filter_relational_operator_1=equals&filter_relational_operator_0=equals&filter_1=UNEP%2FMAP&filter_0=true', 
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        
        with urlopen(req) as details:
            soup_details = BeautifulSoup(details,"html.parser")
        titles = soup_details.find_all("h4")
        
        for ti in titles:
            if ti.span:  # Check if span exists before unwrapping
                ti.span.unwrap()

        hand = soup_details.find_all("a", class_="image-link", href=True)
        for ha in hand:
            if ha.img:  # Check if img exists before unwrapping
                ha.img.unwrap()
        
        n = 0
        base_url = "https://wedocs.unep.org/"
        row_list = []

        for j in hand:
            try:
                # Add delay between requests to avoid being blocked
                time.sleep(random.uniform(1, 3))
        
                # Extract correct date passing for pandas
                meta_url = urljoin(base_url, j['href'] + "?show=full")
        
                req_meta = Request(
                    url=meta_url, 
                    headers={'User-Agent': 'Mozilla/5.0'}
                )
        
                meta_response = urlopen(req_meta)
        
                date_details = BeautifulSoup(meta_response, "html.parser")
            
                table = date_details.find("table", {"class": "table table-bordered table-striped table-hover"})
                if table:
                    rows = table.find_all("tr")
                    data = [[td.text.strip() for td in row.find_all("td")] for row in rows[1:]]
                    df = pd.DataFrame(data, columns=["namepar", "valuepar", "other"])
                
                    if "dc.date.issued" in df["namepar"].unique():
                        value = list(df.query('namepar == "dc.date.issued"')["valuepar"])[0]
                    elif "dc.date" in df["namepar"].unique():
                        value = list(df.query('namepar == "dc.date"')["valuepar"])[0]
                    else:
                        value = ''
                else:
                    value = ''
            
                # Get details page
                details_url = urljoin(base_url, j['href'])
        
                req_details = Request(
                    url=details_url, 
                    headers={'User-Agent': 'Mozilla/5.0'}
                )
        
                details_response = urlopen(req_details)
            
                soup_details = BeautifulSoup(details_response, "html.parser")
                down = soup_details.find_all("a", class_="btn btn-warning text-uppercase", href=True)
                
                for i in down:
                    pdf_url = i['href'].split('?')[0]
                    pdf_lang = i['href'].split('.pdf')[0][-3:]
                    row = [
                        titles[n].get_text(strip=True),
                        value,
                        urljoin(base_url, j['href']),
                        pdf_lang,
                        urljoin(base_url, pdf_url)
                    ]
                    row_list.append(row)
            
                n = n + 1
            
            except Exception as e:
                print(f"Error processing {j['href']}: {str(e)}")
                continue
        
        writer.writerows(row_list)
