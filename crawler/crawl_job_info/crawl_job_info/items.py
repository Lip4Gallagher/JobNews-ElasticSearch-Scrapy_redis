# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JobInfoItem(scrapy.Item):
    name = scrapy.Field()
    salary_max = scrapy.Field()
    salary_min = scrapy.Field()
    pubdate = scrapy.Field()
    update = scrapy.Field()
    education = scrapy.Field()
    experience = scrapy.Field()
    company = scrapy.Field()
    com_logo = scrapy.Field()
    com_logo_url = scrapy.Field()
    location = scrapy.Field()
    description = scrapy.Field()
    main_cate = scrapy.Field()
    sub_cate = scrapy.Field()
    pub_url = scrapy.Field()
