# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os.path
import json
import datetime
from collections import defaultdict
from scrapy import log
import hackerrank_crawler.settings as settings
from hackerrank_crawler.items import SubDomainItem
from hackerrank_crawler.items import DomainItem
from hackerrank_crawler.items import ChallengeItem
from jinja2 import Template

class ItemEncoder(json.JSONEncoder):
    def default(self, item):
        if isinstance(item, DomainItem) or \
            isinstance(item, SubDomainItem) or  \
            isinstance(item, ChallengeItem):
            return dict(item)
        return json.JSONEncoder.default(self, item)

class HackerrankCrawlerPipeline(object):
    def __init__(self):
        now = datetime.datetime.now().strftime("%Y%m%d")
        self.now = now
        data_folder = settings.DATA_FOLDER
        self.domain_file = open(os.path.join(data_folder, "domain_%s.js" % now), "w");
        self.sub_domain_file = open(os.path.join(data_folder,"sub_domain_%s.js" % now), "w");
        self.challenge_file = open(os.path.join(data_folder,"challenge_%s.js" % now), "w");
        self.report_file = open(os.path.join(data_folder,"report_%s.html" % now), "w");
        self.domains = []
        self.sub_domains = []
        self.challenges = []

    def process_item(self, item, spider):
        if isinstance(item, DomainItem):
            self.domains.append(item)
            self.domain_file.write(json.dumps(dict(item), cls=ItemEncoder) + "\n")

        if isinstance(item, SubDomainItem):
            self.sub_domains.append(item)
            self.sub_domain_file.write(json.dumps(dict(item), cls=ItemEncoder) + "\n")

        if isinstance(item, ChallengeItem):
            self.challenges.append(item)
            self.challenge_file.write(json.dumps(dict(item), cls=ItemEncoder) + "\n")
        return item

    def close_spider(self, spider):
        total = defaultdict(lambda: defaultdict(lambda:0))
        solved = defaultdict(lambda: defaultdict(lambda:0))
        for challenge in self.challenges:
            total[challenge["domain_slug"]][challenge["sub_domain_slug"]] += 1
            if challenge["solved"]:
                solved[challenge["domain_slug"]][challenge["sub_domain_slug"]] += 1

        
        template_text = """
        <html>
        <head>
        <head>
        <style>
        table, tr, th, td {
        border:1px solid black;
        }
        table {
            border-spacing: 0;
        }
        </style>
        </head>
        </head>
        <body>
        <table>
        <tr>
            <td rowspan="2"></td>
            {% for domain in domains %}
            <th colspan="{{domain['children']|length}}">{{domain['name']}}</th>
            {% endfor %}
            <th rowspan="2">Total</th>
        </tr>
        <tr>
            {% for domain in domains %}
                {% for sub_domain in domain["children"] %}
                <td>{{sub_domain["name"]}}</td>
                {% endfor %}
            {% endfor %}
        </tr>
        <tr>
            <td>Total</td>
            {% set count=[] %}
            {% for domain in domains %}
                {% for sub_domain in domain["children"] %}
                    {% if count.append(total[domain['slug']][sub_domain['slug']]) %}
                    {% endif %}
                    <td>{{total[domain['slug']][sub_domain['slug']]}}</td>
                {% endfor %}
            {% endfor %}
            <td>{{count|sum}}</td>

        </tr>
        <tr>
            <td>Solved until {{now}}</td>
            {% set count=[] %}
            {% for domain in domains %}
                {% for sub_domain in domain["children"] %}
                    {% if count.append(solved[domain['slug']][sub_domain['slug']]) %}
                    {% endif %}
                    <td>{{solved[domain['slug']][sub_domain['slug']]}}</td>
                {% endfor %}
            {% endfor %}
            <td>{{count|sum}}</td>
        </tr>
        </table>
        </body>
        </html>
        """
        template = Template(template_text)
        result = template.render(domains = self.domains, total=total, solved=solved, now=self.now)
        self.report_file.write(result)


            

