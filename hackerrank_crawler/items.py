# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class ChallengeItem(scrapy.Item):
    name = scrapy.Field()
    domain = scrapy.Field()
    domain_slug = scrapy.Field()
    sub_domain = scrapy.Field()
    sub_domain_slug = scrapy.Field()
    updated_at = scrapy.Field()
    created_at = scrapy.Field()
    solved_count = scrapy.Field()
    success_ratio = scrapy.Field()
    id = scrapy.Field()
    preview = scrapy.Field()
    max_score = scrapy.Field()
    solved = scrapy.Field()

class SubDomainItem(scrapy.Item):
    name = scrapy.Field()
    domain = scrapy.Field()
    priority = scrapy.Field()
    challenges_count = scrapy.Field()
    slug = scrapy.Field()

class DomainItem(scrapy.Item):
    name = scrapy.Field()
    categories_count = scrapy.Field()
    children = scrapy.Field()
    challenges_count = scrapy.Field()
    slug = scrapy.Field()

class HackerrankCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
