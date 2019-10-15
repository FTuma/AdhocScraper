# Scraping adhoc-announcements for the German stock market

## Motivation
For my Masters thesis, which involved the construction of a stock market sentiment index,
the first step was to code 2 different scrapers for getting the latest data continuously.
It was my first encounter of using the programming language R to do web scraping and it was a steep learning curve.
When I came across Scrapy, I wondered how much effort it would be to build the 2 scrapers with the same or even better
functionality.

## Description - Scrapers
For the thesis, I needed to collect adhoc announcements for companies traded on German exchanges. 
These are compulsory press releases for events such as a release of financial results, management changes, stock repurchases, M&A activities, etc.
In addition, stock price data and company metadata is collected as well.

### Adhoc-announcement spider
This spider collects English adhoc-announcements from dgap.de 
along with some data about the publishing companies such as the name, ISIN & WKN.


### Stock data spider
This spider downloads the price history for the stocks given by their ISIN,
as well as company metadata, e.g. company sector & industry, country, etc.

## Install
Python>=3.4 is required. 

Clone the repo and install the required libraries with:

`$ pip install -r requirements.txt`

Note: It was only tested with Ubuntu.

## Quickstart

In order to run the full scraping process (announcements, stock prices & metadata), navigate to the project root directory and run the following command:

`$ python run.py`
### First execution
When executed for the first time, this will download all the English adhoc announcements (as of 2019, ~25K) and store them into a file, adhoc.csv, in the data folder.

As soon as the scraping of all announcements is finished, it automatically starts to download the stock price data for all the companies based on the unique ISINs (as of 2019, ~1K). 
For each ISIN one file is written into the stocks or stocks_xetra subfolder of the data directory.
 
The corresponding company meta data for each ISIN is written into adhoc_stocks_metadata.csv in the data folder.

### Consecutive executions
In consecutive runs, all new announcements are scraped until the last announcement stored in adhoc.csv is encountered. The new announcements are appended to the existing CSV file.

After finishing scraping the new announcements, the stock price data for them is downloaded, as well as for all announcements published up to 30 business days before the timestamp of the previously last announcement.

If there are not yet existing ISINs in the announcements, their company meta data will be appended to the existing metadata CSV file, adhoc_stocks_metadata.csv.

This way you can easily execute the scraper every day or week with a cronjob.

## Output

**adhoc.csv**: 


|   companyID | company_name   | country     | headline                                          | isin         |   newsID | text                                               | timestamp           | url        | wkn    |
|-------------|----------------|-------------|---------------------------------------------------|--------------|----------|----------------------------------------------------|---------------------|------------|--------|
|      372698 | OSRAM Licht AG | Deutschland | OSRAM Licht AG: OSRAM clears way for ams takeover | DE000LED4000 |  1186915 | The Managing Board of Osram Licht AG (Osram) has ... | 2019-08-21 20:30:00 | https://dg... | LED400 |
**adhoc_stocks_metadata.csv**: 

arivaID, country, exchangeID, file_urls, files, foundingyear, industry, isin, listingdate, sector, security_name, stocktype, ticker

**isin_XXXXXXX.parquet**: German header & format - delimited by semicolon & decimal comma

Datum (date), Eröffnung (open), Höchstkurs (high), Tiefstkurs (low), Schlusskurs (close),Stücke (shares), Volumen (volume) 
## Conclusion
After getting used to inner workings and all the possible extensions of Scrapy, you'll always want to do your web scraping with it. 

Compared to writing a scraper in R, it took less time and the resulting scrapers are faster, more robust and easily extensible.

Replacing the CSV and Parquet pipelines with a database pipeline would require only a few small adjustments. For my current needs it's sufficient to store the data locally as CSV and Parquet files.





