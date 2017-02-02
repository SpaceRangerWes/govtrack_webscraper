#!/usr/bin/python

import urllib.request
from bs4 import BeautifulSoup
import re
import csv

#Query the website and return the html to the variable 'page'
with urllib.request.urlopen('https://policy.house.gov/legislative/bills') as response:
    page = response.read()

def get_bill_page(url):
    texts = ""
    with urllib.request.urlopen('https://policy.house.gov' + url) as response:
        info_page = response.read()
    soup_info = BeautifulSoup(info_page, "lxml")
    title = soup_info.find("h1", {"id": "page-title"}).text
    m = re.search(r'\<h3\>\s*\<strong\>\s*Summary\s*\<\/strong\>\s*\<\/h3\>\s*((.|\s)*?)\<hr\/\>',str(soup_info))
    n = re.sub('<[^<]+?>', '', m.group(1))
    n = n.replace(u'\xa0', u'')
    n = n.replace(u'\n', u'')
    return (n, title)

#Parse the html in the 'page' variable, and store it in Beautiful Soup format
soup = BeautifulSoup(page, "lxml")
tuple_list = []
for each in soup.findAll('div',{'class': lambda x: x and 'views-row' in x.split()}):
    time = each.span.span.span.text
    a = each.find('a', href=True)
    summary, title = get_bill_page(a['href'])
    tuple_list.append((title, summary, time))

with open('govtrack.csv','wb') as out:
    csv_out=csv.writer(out)
    csv_out.writerow(['title','Summary', 'last_action'])
    for row in tuple_list:
        csv_out.writerow(row)
