# govtrack web scraper

## How It Works
Each bill on https://policy.house.gov/legislative/bills is a hyperlink to a page that contains the specifics of that bill. This script stores the hyperlink as the bill's title and then reaches out to the linked page. Once it navigates to the bill's page, it retrieves each section on that page.

* Note: This means that the script's speed is reliant on the response time of navigating to a webpage.

As a pass is made to each bill page, a row is emitted to the CSV file. The script also maintains the previous run in case something goes wrong during the current processing run. I'd hate for you to lose any data if that were to happen! Two CSV files may be emitted to the local directory, *govtrack_old.csv* and *govtrack.csv*.

#### Rows currently emitted (can easily be changed; just ask):
* title
* summary
* last action date

## Requirements for Use
* python3 (built with Python 3.5.2)
* BeautifulSoup4
  * To install ```pip3 install bs4```

## How To Use
It is as simple as typing ```python3 govtrack_webscrape.py``` in your terminal emulator of choice.
