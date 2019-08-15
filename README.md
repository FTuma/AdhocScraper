# Scraping adhoc-announcements for the German stock market (CDAX)

## Motivation
For my Masters thesis, which involved the construction of a stock market sentiment index,
the first step was to code 2 different scrapers to continuously get the latest data.
It was my first encounter of using the programming language R to do web scraping and it was a steep learning curve.
When I came across Scrapy, I wondered how much effort it would be to build the 2 scrapers with the same or even better
functionality in Python with Scrapy.

## Scrapers
For the thesis, I needed to collect adhoc announcements (which are compulsory press releases for events like
release of financial results, management changes, stock repurchases, M&A activities and many more)
for all CDAX companies, as well as stock price data and company metadata.

### Adhoc-announcement spider
This spider collects English adhoc-announcements from dgap.de, 
along with the some data about the publishing companies like the name, ISIN & WKN.


### Stock data spider
This spider downloads the price history for the stocks given by their ISIN,
as well as company metadata like the company sector & industry, country and more if available.

## Installation
Python 3 is required and it was only tested with Ubuntu, so it might need a few adaptions to run on Windows.

Clone the repo and install the required libraries.

`$ pip install -r requirements.txt`

## Quickstart

First, adapt the paths in adhocScraper/settings.py according to your local environment.

`$ python run.py`
### First execution
When executed the first time, this will download all the English adhoc announcements (as of 2019, ~25K) and store them into a CSV file.

After it finished the scraping of all announcements, it automatically starts to download the stock price data for all the companies based on the unique ISINs (as of 2019, ~1K), 
along with some company meta data.

### Consecutive executions
In consecutive runs, it will scrape all new announcements until it encounters the last announcement stored in the existing CSV file. The new announcements are appended to the CSV file.

After it finished scraping the new announcements, it downloads the stock price data for the new announcements and also for all announcements published up to 30 business days before the last announcement.

If there are not yet existing ISINs in the announcements, there meta data will be appended to the existing metadata CSV file.

This way you can easily execute the scraper every week with a cronjob.


