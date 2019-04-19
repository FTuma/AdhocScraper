# -*- coding: utf-8 -*-
import scrapy


class AdhocScraperSpider(scrapy.Spider):
    name = 'adhoc_scraper'
    allowed_domains = ['www.dgap.de']
    start_urls = ['https://dgap.de/dgap/News/?newsType=ADHOC&page=1&limit=20']
    XPATH_SYMBOLS_ENG = '//a[(((count(preceding-sibling::*) + 1) = 4) and parent::*)]'

    def parse(self, response):
        # Print what the spider is doing
        print(response.url)

        #eng_links = Selector(response=page).xpath(XPATH_SYMBOLS_ENG)
        #headlines_links_eng = [href.xpath('@href').extract()[0] for href in eng_links if
        #                       'newsID' in href.xpath('@href').extract()[0]]

        href_selectors = response.xpath(self.XPATH_SYMBOLS_ENG)
        # Loop on each tag
        for selector in href_selectors:
            # Extract the link text
            text = selector.xpath("text()").extract_first()
            # Extract the link href
            link = selector.xpath('@href').extract()[0] if 'newsID' in selector.xpath('@href').extract()[0] else False
            if link:
                # Create a new Request object
                request = response.follow(link, callback=self.parse)
                # Return it thanks to a generator
                yield request
            else:
                continue
