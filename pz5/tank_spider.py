import scrapy
from tank_crawler.items import TankItem


class TankSpider(scrapy.Spider):
    name = 'tank_spider'
    start_urls = [
        'https://wiki.warthunder.ru/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%9D%D0%B0%D0%B7%D0%B5%D0%BC%D0%BD%D0%B0%D1%8F_%D1%82%D0%B5%D1%85%D0%BD%D0%B8%D0%BA%D0%B0_%D0%A1%D0%A1%D0%A1%D0%A0']

    def parse(self, response):
        # Получаем все ссылки на танки на странице
        tank_links = response.xpath('//div[@class="mw-category-group"]//a/@href').extract()
        for link in tank_links:
            yield response.follow(link, callback=self.parse_tank)

    def parse_tank(self, response):
        item = TankItem()
        item['name'] = response.xpath('//h1/text()').get()
        item['description'] = response.xpath('//div[@class="mw-parser-output"]/p[1]/text()').get()
        item['research_points'] = response.xpath(
            '//table[contains(@class, "wikitable")]//tr[th[contains(text(),"Опыт для исследования")]]/td/text()').get()
        item['silver_lions'] = response.xpath(
            '//table[contains(@class, "wikitable")]//tr[th[contains(text(),"Стоимость покупки")]]/td/text()').get()

        yield item
