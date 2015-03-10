#!/usr/local/bin/python2.7
# -*- coding: utf-8 -*-

import lxml.html, requests, sqlite3, datetime

db = sqlite3.connect('/home/strongbo/NEWPROJECT/data.db')
db.text_factory = str
cursor = db.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS indices(stockindex TEXT, company TEXT, isin CHAR(12), DateAdded CHAR(10))''')
db.commit()

indices = ['Dax', 'TecDAX', 'Dow_Jones', 'MDAX', 'SDAX', 'S&P_500', 'Nasdaq_100', 'Euro_Stoxx_50', 'SMI', 'ATX', 'CAC_40', 'Nikkei_225']

count = 0
for item in indices:
    print item
    website = requests.get("http://www.finanzen.net/index/"+item+"/Werte")
    tree = lxml.html.fromstring(website.text)
    last_page = tree.xpath('//a[@class="last"]')
    content = tree.xpath('//div[@class="contentBox tableQuotes"]//tr/td')
    for i in xrange(0,len(content),11):
        cursor.execute('''INSERT INTO indices(stockindex, company, isin, DateAdded) VALUES (?,?,?,?) ''', (item, content[i][0].text, content[i][1].text, datetime.date.today()))
        count += 1
    if len(last_page) != 0:
        for x in range(2,int(last_page[0].text)+1):
            website = requests.get("http://www.finanzen.net/index/"+item+"/Werte@intpagenr_"+str(x))
            tree = lxml.html.fromstring(website.text)
            content = tree.xpath('//div[@class="contentBox tableQuotes"]//tr/td')
            for i in xrange(0,len(content),11):
                cursor.execute('''INSERT INTO indices(stockindex, company, isin, DateAdded) VALUES (?,?,?,?) ''',(item, content[i][0].text, content[i][1].text, datetime.date.today()))
                count += 1
    else:
        pass
    db.commit()

db.close()
print "Es wurden "+str(count)+" Einträge ausgelesen und in der Datenbank gespeichert!"


'''   FUNKTIONEN DIE NOCH HINZUGEFÜGT WERDEN MÜSSEN   '''
'''   - Überprüfen, ob Eintrag schon vorhanden ist, wenn nicht -> HINZUFÜGEN!   '''
'''   - Überprüfen, ob Eintrag noch Teil des Index ist, wenn nicht -> ENTFERNEN '''