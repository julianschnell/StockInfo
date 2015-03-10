#!/usr/local/bin/python2.7
# -*- coding: utf-8 -*-

import lxml.html, requests, json, sqlite3

def GetISIN (str):
    dict = {}
    website = requests.get('http://json.finanzen100.de/v1/search/instrument_list?QUERY='+str+'&_LOCALE=de_DE')
    data = json.loads(website.text)
    i=0
    if data.has_key("INSTRUMENT_LIST"):
        for item in data["INSTRUMENT_LIST"]:
            i += 1
            dict[i] = item["NAME"].encode('utf-8'), item["ISIN"].encode('utf-8')
            print i, item["ISIN"], item["NAME"]
    else:
        print "No entries found for this query!"
        return 1

    s1 = raw_input('Please select a stock: ')
    while True:
        try:
            if int(s1) in dict:
                break
            else:
                s1 = raw_input('Wrong query! Please repeat: ')
        except ValueError:
            s1 = raw_input('Wrong query! Please repeat: ')
    return dict[int(s1)] ##returns tuple with two values: ('NameofStock', 'ISIN')

def GetAnalysis (q): ## q is a tuple like ('NameofStock', 'ISIN')
    count = 0
    a = 1
    page = 3 ##page can actually be any value higher than a!
    cursor.execute("SELECT * FROM news WHERE isin=? ORDER BY date desc", (q[1],)) ##load most current entry from database!
    currententry = cursor.fetchone()
    while a < page+1:
        link = 'http://www.onvista.de/news/alle-news?assetId='+str(q[1])+'&assetType=Stock&searchTerm=&dateRange=&orderBy=datetime&newsType%5B%5D=analysis&page='+str(a)
        website = requests.get(link)
        tree = lxml.html.fromstring(website.text)
        a_news = tree.xpath('//div[@class="SPALTE_1"]')
        if a == 1:
            page = website
            try:
                page = len(a_news[0][-1][1])-1 ##number of webpages to scrape!
            except IndexError:
                print "Unfortunately there is no analysis for this stock!"
                break
            print page
        newsbox = tree.find_class("NEWS_TEASERBOX ARTIKEL")
        for x in newsbox:
            try:
                date = x[1][0].attrib['datetime'].encode('utf-8')
                trend = x[0][0].attrib['class'].split(" ")[-1].encode('utf-8')
                link = 'http://www.onvista.de'+x[0][1].attrib['href'].encode('utf-8')
                title = x[0][1].text.encode('utf-8')
                analyst = x[1][0].tail.encode('utf-8')
                teaser = x[2][0].text.encode('utf-8')
            except IndexError:
                continue
            if currententry == (q[0], q[1], date, trend, title, teaser, link, analyst): ##check whether scraped content is identical with most current content in database! if this is the case -> exit!
                return "Es wurden "+str(count)+" neue Einträge angelegt!"
            cursor.execute('''INSERT INTO news(name, isin, date, trend, title, teaser, link, analyst) VALUES (?,?,?,?,?,?,?,?) ''', (q[0], q[1], date, trend, title, teaser, link, analyst))
            count += 1
        print
        a += 1
        db.commit()
    return str(count)+" entries added!"



''' LOADING DATABASE news '''
db = sqlite3.connect('data.db')
db.text_factory = str
cursor = db.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS news(name TEXT, isin CHAR(12), date CHAR(22), trend TEXT, title TEXT, teaser TEXT, link TEXT, analyst TEXT)
''')
db.commit()

''' START DB-QUERY '''
while True:
    s = raw_input('Search stock: ')
    Aktie = GetISIN(s)
    if Aktie != 1:
        break

Liste = GetAnalysis(Aktie)
print Liste
db.close()
