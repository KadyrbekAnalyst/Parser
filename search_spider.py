import scrapy


class MechtaSpider(scrapy.Spider):
    name = 'mechta'
    start_urls = ['https://www.mechta.kz/search/?q=iphone&page=1']
    
    def parse(self,response):
        for a in response.xpath('//a'):
            yield {'a_links':a.xpath('.//@href').get()}