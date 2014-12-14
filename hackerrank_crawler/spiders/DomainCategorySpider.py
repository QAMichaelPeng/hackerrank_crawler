import scrapy
from scrapy import log
from scrapy.http import Request
import json
from hackerrank_crawler.items import SubDomainItem
from hackerrank_crawler.items import DomainItem
from hackerrank_crawler.items import ChallengeItem
import hackerrank_crawler.settings as settings
from urllib import quote_plus


class DomainCategorySpider(scrapy.Spider):
    name = "DomainCategory"
    allowed_domains = ["hackerrank.com"]
    start_urls = [
        "https://www.hackerrank.com/auth/login/master"
    ]
    domain_homepage = "https://www.hackerrank.com/domains"

    def __init__(self, username=None, password=None):
        self.username = username
        self.password = password
        
    def create_subcategory_request(self, response, domain, sub_domain, count, item):
        url_base = response.url
        if not url_base.endswith("/"):
            url_base = url_base + "/"
        url_base = "https://www.hackerrank.com/rest/contests/master/categories/%s%%7C%s/challenges?offset=%d&limit=10&filter=" 

        page = 1
        itemPerPage = 10
        requests = [Request(url= url_base % (quote_plus(domain), quote_plus(sub_domain), page*10) , callback = self.parse_sub_category, meta={"item":item, "page":page}) \
                    for page in range(0, (count+itemPerPage-1)/itemPerPage)]
        return requests
        
    def parse_sub_category(self, response):
        item = response.meta["item"]
        content = json.loads(response.body)
        for model in content["models"]:
            challenge = ChallengeItem()
            challenge["name"] = model["name"]
            challenge["domain"] = model["track"]["track_name"]
            challenge["domain_slug"] = model["track"]["track_slug"]
            challenge["sub_domain"] = model["track"]["name"]
            challenge["sub_domain_slug"] = model["track"]["slug"]
            challenge["max_score"] = model["max_score"]
            challenge["updated_at"] = model["updated_at"]
            challenge["created_at"] = model["created_at"]
            challenge["solved_count"] = model["solved_count"]
            challenge["success_ratio"] = model["success_ratio"]
            challenge["id"] = model["id"]
            challenge["preview"] = model["preview"]
            challenge["solved"] = model["solved"]
            yield challenge


    def parse(self, response):
        while not self.username:
            self.username = raw_input("Enter username:")
        while not self.password:
            self.password = raw_input("Enter password:")
        return scrapy.FormRequest.from_response(
            response,
            formname="legacy-login",
            formdata={'login': self.username, 'password': self.password},
            callback=self.after_login
        )

    def after_login(self, response):
        result = json.loads(response.body)
        if not result["status"]:
            log.msg("Login failed, %s" % result["errors"], level=log.CRITICAL)
            return
        return Request(url=DomainCategorySpider.domain_homepage, callback=self.parse_domain)

    def parse_domain(self, response):
        lines = response.body.splitlines()
        lines = filter(lambda x:x.strip().startswith("HR.PREFETCH_DATA ="), lines)
        if len(lines) != 1:
            log.msg("Can't find category info", level=log.CRITICAL)
            return
        else:
            line = lines[0]
            l = line.find("{")
            r = line.rfind("}")
            line = line[l:r+1]
            js = json.loads(line)
            line = json.dumps(js, indent=4)
            result =[] 
            requests=[]
            for category in js["contest"]["categories"]:
                total_challenges_count = 0
                domain = DomainItem()
                domain["name"] = category["name"]
                domain["slug"] = category["slug"]
                domain["categories_count"] = category["categories_count"]
                domain["children"] = []
                for child in category["children"]:
                    sub_domain = SubDomainItem()
                    sub_domain["name"] = child["name"]
                    sub_domain["slug"] = child["slug"]
                    sub_domain["priority"] = child["priority"]
                    sub_domain["challenges_count"] = child["challenges_count"]["total"]
                    sub_domain["domain"] = domain["name"]
                    total_challenges_count += sub_domain["challenges_count"]
                    domain["children"].append(sub_domain)
                    for request in self.create_subcategory_request(response, domain["slug"], sub_domain["slug"], sub_domain["challenges_count"], sub_domain):
                        yield request
                domain["challenges_count"] = total_challenges_count
                yield domain
