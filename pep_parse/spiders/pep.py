import scrapy

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://' + url + '/' for url in allowed_domains]

    def parse(self, response):
        tbody = response.css('section#numerical-index > table > tbody')
        all_links = tbody.css('a::attr(href)').getall()
        for pep_link in all_links:
            yield response.follow(pep_link, callback=self.parse_pep)

    def parse_pep(self, response):
        title = response.css('h1.page-title').xpath('string(.)').get()
        pep_number, pep_name = title.split(' – ', 1)
        data = {
            'number': pep_number.replace('PEP ', ''),
            'name': pep_name,
            'status': response.css(
                'dt:contains("Status") + dd > abbr::text'
            ).get(),
        }
        yield PepParseItem(data)
