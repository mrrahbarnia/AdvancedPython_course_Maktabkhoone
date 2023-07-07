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

from sklearn import tree
from sklearn.preprocessing import LabelEncoder

car = input("Model: ")

cursor = cnx.cursor(buffered=True)
query = "SELECT Model,Year,Miles,Price FROM cars WHERE Model = \'%s\'" % car
cursor.execute(query)
x = []
y = []
for i in cursor:
    x.append(((i[1]),int(i[2])))
    y.append(int(i[3]))

cursor = cnx.cursor(buffered=True)
query = "SELECT Model,Year,Miles,Price FROM cars WHERE Model = \'%s\'" % car
cursor.execute(query)

clf = tree.DecisionTreeClassifier()
clf = clf.fit(x,y)

for i in cursor:
    new_data = [[i[1],int(i[2])]]
    fair_price = clf.predict(new_data)
    print("Model: {}|Year: {}|Miles: {}|Price: {}|Fair price: {}".format(i[0],i[1],i[2],i[3],fair_price[0]))


cnx.commit()
cnx.close()



