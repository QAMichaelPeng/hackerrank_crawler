# -*- coding: utf-8 -*-

# Scrapy settings for hackerrank_crawler project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#
import os.path
BOT_NAME = 'hackerrank_crawler'

SPIDER_MODULES = ['hackerrank_crawler.spiders']
NEWSPIDER_MODULE = 'hackerrank_crawler.spiders'

# Not use LOG_FILE here to let the log output to stdout,
# see __init__.py to see the use of LOG_OBSERVE_FILE

LOG_FOLDER="log"
if not os.path.exists(LOG_FOLDER):
    os.makedirs(LOG_FOLDER)
LOG_FILE=os.path.join(LOG_FOLDER, "crawl.log")
LOG_OBSERVE_FILE = os.path.join(LOG_FOLDER, "crawl.log")


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'hackerrank_crawler (+http://www.yourdomain.com)'

DATA_FOLDER = "crawl_results"
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)


ITEM_PIPELINES = {
    'hackerrank_crawler.pipelines.HackerrankCrawlerPipeline': 300,
}

