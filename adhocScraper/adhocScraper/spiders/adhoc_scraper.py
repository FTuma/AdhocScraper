# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from adhocScraper.items import AdhocNewsItem
from w3lib.html import remove_tags
import re



class AdhocScraperSpider(scrapy.Spider):
    name = 'adhoc_scraper'
    allowed_domains = ['dgap.de']
    #start_urls = ['https://dgap.de/dgap/News/?newsType=ADHOC&page=1&limit=20']
    XPATH_SYMBOLS_ENG = '//a[(((count(preceding-sibling::*) + 1) = 4) and parent::*)]'
    XPATH_SECOND_PAGE = '//*[@id="content"]/div[1]/div/div[2]/a'
    XPATH_NEXT_PAGE = '//*[@id="content"]/div[1]/div/div[2]/div[2]/a'

    XPATH_COMPANY_NAME = '//*[contains(concat( " ", @class, " " ), concat( " ", "company_header", " " ))]//*[contains(concat( " ", @class, " " ), concat( " ", "darkblue", " " ))]'
    XPATH_COMPANY_WKN_ISIN_COUNTRY = '//*[@id="content"]/div[1]/div[1]/ul/li'  # '//*[contains(concat( " ", @class, " " ), concat( " ", "company_header", " " ))]//ul'

    XPATH_COMPANY_DATETIME = '/html/body/div[2]/div[2]/div[1]/div[2]/div/h2'
    XPATH_COMPANY_HEADLINE = '//*[@id="content"]/div[1]/div[2]/div/div/h1'
    XPATH_COMPANY_MAINTEXT = '//*[contains(concat( " ", @class, " " ), concat( " ", "news_main", " " ))]'
    XPATH_COMPANY_MAINTEXT_PRE = '//pre'
    RE_DATETIME = r'.+ (\d\d\.\d\d\.\d\d\d\d \| \d\d:\d\d)'


    def __init__(self, url='https://dgap.de/dgap/News/?newsType=ADHOC&page=1&limit=20', *args, **kwargs):
        # Don't forget to call parent constructor
        super(AdhocScraperSpider, self).__init__(*args, **kwargs)
        # Set the start_urls to be the one given in url parameters
        self.start_urls = [url]

    def parse(self, response):
        # Print what the spider is doing
        print(response.url)
        href_selectors = response.xpath(self.XPATH_SYMBOLS_ENG)
        # Loop on each tag
        for selector in href_selectors:
            # Extract the link text
            # text = selector.xpath("text()").extract_first()
            # Extract the link href
            link = selector.xpath('@href').extract()[0] if 'newsID' in selector.xpath('@href').extract()[0] else False
            if link:
                # Create a new Request object
                # print(link)
                request = response.follow(link, callback=self.parse_adhoc_page)
                # Return it thanks to a generator
                yield request
            else:
                continue
        if response.url != self.start_urls[0]:
            next_page_selector = response.xpath(self.XPATH_NEXT_PAGE)
        else:
            next_page_selector = response.xpath(self.XPATH_SECOND_PAGE)

        link_next_page = next_page_selector.xpath('@href').extract_first()
        print(link_next_page)
        request = response.follow(link_next_page, callback=self.parse)
        yield request

    def parse_adhoc_page(self, response):
        # Print what the spider is doing
        print(response.url)

        l = ItemLoader(item=AdhocNewsItem(), response=response)
        l.add_value('url', response.url)
        l.add_xpath('company_name', self.XPATH_COMPANY_NAME)

        company_meta = [' '.join(remove_tags(x).split()) for x in response.xpath(self.XPATH_COMPANY_WKN_ISIN_COUNTRY).extract()]
        if 'WKN' in company_meta[0]:
            l.add_value('wkn', re.search(r'WKN: (.+)', company_meta[0]).group(1))
            l.add_value('isin', re.search(r'ISIN: (.+)', company_meta[1]).group(1))
            l.add_value('country', re.search(r'Land: (.+)', company_meta[2]).group(1))
        else:
            l.add_value('wkn', '')
            l.add_value('isin', re.search(r'ISIN: (.+)', company_meta[0]).group(1))
            l.add_value('country', re.search(r'Land: (.+)', company_meta[1]).group(1))
        l.add_value('timestamp', response.xpath(self.XPATH_COMPANY_DATETIME).re(self.RE_DATETIME))
        l.add_xpath('headline', self.XPATH_COMPANY_HEADLINE)
        l.add_xpath('text', self.XPATH_COMPANY_MAINTEXT)
        l.add_xpath('text', self.XPATH_COMPANY_MAINTEXT_PRE)


        return l.load_item()

    # rules = (
    #     # Extract link from this path only
    #     Rule(
    #         LxmlLinkExtractor(restrict_xpaths=[
    #             "//ol[@id=repo-list]//h3/a/@href"], allow_domains=['https://github.com/trending']),
    #         callback='parse'
    #     ),
    #     # link should match this pattern and create new requests
    #     Rule(
    #         LxmlLinkExtractor(allow='https://github.com/[\w-]+/[\w-]+$', allow_domains=['github.com']),
    #         callback='parse_product_page'
    #     ),
    # )


XPATH_COMPANY_META = '//*[contains(concat( " ", @class, " " ), concat( " ", "darkblue", " " ))] | //*[(@id = "content")]//ul'
XPATH_COMPANY_WKN = '//*[contains(concat( " ", @class, " " ), concat( " ", "company_header", " " ))]//li[(((count(preceding-sibling::*) + 1) = 1) and parent::*)]'
XPATH_COMPANY_ISIN = '//*[contains(concat( " ", @class, " " ), concat( " ", "company_header", " " ))]//li[(((count(preceding-sibling::*) + 1) = 2) and parent::*)]'
XPATH_COMPANY_COUNTRY = '//*[contains(concat( " ", @class, " " ), concat( " ", "company_header", " " ))]//li[(((count(preceding-sibling::*) + 1) = 3) and parent::*)]'
