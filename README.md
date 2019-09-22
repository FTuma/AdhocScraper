# Scraping adhoc-announcements for the German stock market

## Motivation
For my Masters thesis, which involved the construction of a stock market sentiment index,
the first step was to code 2 different scrapers to continuously get the latest data.
It was my first encounter of using the programming language R to do web scraping and it was a steep learning curve.
When I came across Scrapy, I wondered how much effort it would be to build the 2 scrapers with the same or even better
functionality in Python with Scrapy.

## Description - Scrapers
For the thesis, I needed to collect adhoc announcements (which are compulsory press releases for events like
release of financial results, management changes, stock repurchases, M&A activities and many more)
for all CDAX companies, as well as stock price data and company metadata.

### Adhoc-announcement spider
This spider collects English adhoc-announcements from dgap.de, 
along with the some data about the publishing companies like the name, ISIN & WKN.


### Stock data spider
This spider downloads the price history for the stocks given by their ISIN,
as well as company metadata like the company sector & industry, country and more if available.

## Install
Python>=3.4 is required and it was only tested with Ubuntu.

Clone the repo and install the required libraries with:

`$ pip install -r requirements.txt`


## Quickstart

To run the full scraping process (announcements, stock prices & metadata), just navigate to the project root directory and run the following command:

`$ python run.py`
### First execution
When executed the first time, this will download all the English adhoc announcements (as of 2019, ~25K) and store them into a file, adhoc.csv, in the data folder.

After it finished the scraping of all announcements, it automatically starts to download the stock price data for all the companies based on the unique ISINs (as of 2019, ~1K) and write one file for each ISIN into the stocks subfolder of the data directory.
 
The corresponding company meta data for each ISIN is written into adhoc_stocks_metadata.csv in the data folder.

### Consecutive executions
In consecutive runs, all new announcements are scraped until the last announcement stored in adhoc.csv is encountered. The new announcements are appended to the existing CSV file.

After finishing scraping the new announcements, the stock price data for them is downloaded, as well as for all announcements published up to 30 business days before the timestamp of the previously last announcement.

If there are not yet existing ISINs in the announcements, their company meta data will be appended to the existing metadata CSV file, adhoc_stocks_metadata.csv.

This way you can easily execute the scraper every day or week with a cronjob.

## Output

**adhoc.csv**: 

timestamp, newsID, headline, text, isin, companyID, company_name, country, url, wkn

**adhoc_stocks_metadata.csv**: 

arivaID, country, exchangeID, file_urls, files, foundingyear, industry, isin, listingdate, sector, security_name, stocktype, ticker

**isin_XXXXXXX.csv**: German header & format - delimited by semicolon & decimal comma

Datum (date), Eröffnung (open), Höchstkurs (high), Tiefstkurs (low), Schlusskurs (close),Stücke (shares), Volumen (volume) 
## Conclusion
After getting used to inner workings and all the possible extensions of Scrapy, you'll always want to do your web scraping with it. 

Especially, compared to writing a scraper in R, because it took less time and the resulting scrapers are faster, more robust and easily extensible.

Replacing the CSV and Parquet pipelines with a database pipeline would require only a few small adjustments, 
but for my current needs it's sufficient to store the data locally as CSV and Parquet files.





