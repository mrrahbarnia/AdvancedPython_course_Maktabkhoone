import mysql.connector

cnx = mysql.connector.connect(host = '127.0.0.1',
                              user = '****',
                              password = '****',
                              database = 'Project'
                              )

import requests
from bs4 import BeautifulSoup

for page in range(1,500):
    url = "https://www.truecar.com/used-cars-for-sale/listings/?buyOnline=true&page=%i" % page 
    response = requests.get(url)
    soup = BeautifulSoup(response.text , "html.parser")
    model = soup.find_all("span","truncate")[::2]
    year = soup.find_all("span",{"class":"vehicle-card-year text-xs"})
    miles = soup.find_all("div",{"data-test":"vehicleMileage"})
    price = soup.find_all("div" , "heading-3 my-1 font-bold")
    for m,y,mi,p in zip(model,year,miles,price):
        cursor = cnx.cursor(buffered=True)
        query = "INSERT IGNORE INTO cars (Model,Year,Miles,Price) VALUES(\'%s\',%i,%f,%f);" % ((m.text),(int(y.text)),(float(((mi.text).replace(',','.')).replace('miles',''))),(float(((p.text).replace(',','.')).replace('$',''))))
        cursor.execute(query)
        cnx.commit()

