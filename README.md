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
This spider collects all English adhoc-announcements from dgap.de, 
along with the some data about the publishing companies like the name, ISIN & WKN.


### Stock data spider
This spider downloads the price history for the stocks given by their ISIN,
as well as company metadata like the company sector & industry, country and more if available.

## Usage

Adhoc-announcements:  
`scrapy crawl adhocScraper -o adhoc.csv`  
Stocks:  
`scrapy crawl arivaStocks -o adhoc_stocks_metadata.csv`
