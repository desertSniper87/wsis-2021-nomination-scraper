import re

import scrapy

class LawsSpider(scrapy.Spider):
    BASE_URL = 'https://www.itu.int/'
    name = "nominations2"

    def start_requests(self):
        urls = [ self.BASE_URL + f'net4/wsis/stocktaking/Prizes/2021/Nominated?jts=8S9QLL&idx=11&page={p}' for p in range(1, 19)]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        category_name = response.xpath('/html/body/div[2]/section/div/div[2]/div/h4/text()').get().strip()
        nominations = response.css('body > div:nth-child(2) > section > div > div:nth-child(2) > div > div')
        for nomination in nominations:
            nomination_title = nomination.css('h6').xpath('text()').get().strip()
            nomination_desc = nomination.xpath("div/div/p/text()").get().strip()
            nomination_link = nomination.xpath('div/div/p/a/@href').get().strip()

            # print(self.BASE_URL+nomination_link)

            n = {
                'cat': category_name,
                'title': nomination_title,
                'desc': nomination_desc,
                'link': nomination_link,
            }


            yield scrapy.Request(url=self.BASE_URL+nomination_link,
                                 callback=self.parse_subpage,
                                 meta={'nomination': n})

            # print("=======")
            # print(nomination_title, nomination_desc, nomination_link, )
            # print("=======")

            # law_url = self.BASE_URL + law_link
            # law_description = self.parse_subpage(law_url)


    def parse_subpage(self, response):
        new_nom = response.request.meta['nomination']
        country = response.css('fieldset > ul > li > span').xpath('text()').get().strip()
        new_nom['country'] = country
        # print(country)
        yield new_nom



