from bs4 import BeautifulSoup
import requests
import time 

url = "https://www.amazon.com/gp/product/B078MC547V/ref=dbs_a_def_rwt_hsch_vapi_tkin_p1_i5"
r  = requests.get(url)
data = r.text
time.sleep(1)
soup = BeautifulSoup(data, "html.parser")
print(soup.contents)

#print(soup.contents)
#span = soup.find_all("h2")
#print(span)

""""
time.sleep(2)
span = soup.find("span",id="productTitle")
time.sleep(2)
print(span)
"""