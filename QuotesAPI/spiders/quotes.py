import scrapy
import json


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = ['https://quotes.toscrape.com/api/quotes?page=1']

    def parse(self, response):
        resp = json.loads(response.body)
        quotes = resp.get("quotes")
        has_next = resp.get("has_next")
        
        for quote in quotes:
            yield{
                "quotes" : quote.get("author").get("name"),
                "tags"  :   quote.get("tags"),
                "text"  :   quote.get("text")
            }

    
        if has_next:
            next_page_number = resp.get("page") + 1
            
            yield scrapy.Request(
                url = f'https://quotes.toscrape.com/api/quotes?page={next_page_number}',
                callback = self.parse
            )
