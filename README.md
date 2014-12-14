#A project to scrape hacker rank and generate report for progress on hacker rank.#

##Dependency##

1. [Python 2.7](https://www.python.org/download/releases/2.7/)
2. [Scrapy 0.24.4, Python scraper framework](http://scrapy.org/)
3. [Jinja2: Python template engine](http://jinja.pocoo.org/)


##Usage##
```
scrapy crawl DomainCategory -a username=<hackerranker username> -a password=<hackerranker password>
```

[sample results](http://htmlpreview.github.io/?https://github.com/QAMichaelPeng/hackerrank_crawler/blob/master/crawl_results/report_20141213.html)