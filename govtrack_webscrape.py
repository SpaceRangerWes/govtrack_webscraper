#!/usr/bin/python

import urllib.request
from bs4 import BeautifulSoup
import re
import csv
import os


def get_section(section):
    nextNode = section
    title = nextNode.text
    regex = re.compile('[^a-zA-Z]')
    title = regex.sub('', nextNode.text).lower()
    text = ""
    while True:
        try:
            nextNode = nextNode.nextSibling
        except AttributeError:
            # end of page
            break
        try:
            tag_name = nextNode.name
        except AttributeError:
            tag_name = ""
        if tag_name == "p":
            text += str(nextNode.text)
        elif tag_name == "h3":
            # end of section
            break
    return (title, text)


def get_bill_page(url):
    sections = dict()
    with urllib.request.urlopen('https://policy.house.gov' + url) as response:
        info_page = response.read()
    soup_info = BeautifulSoup(info_page, "lxml")
    title = soup_info.find("h1", {"id": "page-title"}).text
    for section in soup_info.findAll('h3'):
        key, value = get_section(section)
        sections[key] = value
    print(title)
    return (title, sections)


def get_bill_summary(sections):
    if "summary" in sections:
        return (sections["summary"])
    else:
        return ("Error providing bill summary; keys available: {}".format(
            sections.keys()))


if __name__ == "__main__":
    #Query the website and return the html to the variable 'page'
    with urllib.request.urlopen(
            'https://policy.house.gov/legislative/bills') as response:
        page = response.read()

    #Parse the html in the 'page' variable, and store it in Beautiful Soup format
    soup = BeautifulSoup(page, "lxml")
    bills = soup.findAll('div',
                         {'class': lambda x: x and 'views-row' in x.split()})
    index = 1
    total = len(bills)

    #Remove previous data run
    try:
        os.remove('govtrack_old.csv')
    except OSError:
        if os.path.isfile('govtrack.csv'):
            os.rename('govtrack.csv', 'govtrack_old.csv')

    #Write by appending to csv file
    with open('govtrack.csv', 'w') as out:
        csv_out = csv.writer(out)
        csv_out.writerow(['title', 'summary', 'last_action_date'])
        for each in bills:
            time = each.span.span.span.text
            a = each.find('a', href=True)
            print("\n{0}/{1}".format(index, total))
            index += 1
            title, bill_sections = get_bill_page(a['href'])
            summary = get_bill_summary(bill_sections)
            csv_out.writerow([title, summary, time])
    print("Finished Scraping")
