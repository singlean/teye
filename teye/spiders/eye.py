# -*- coding: utf-8 -*-
import scrapy
from copy import deepcopy
from scrapy_redis.spiders import RedisSpider
from pprint import pprint

class EyeSpider(scrapy.Spider):

    name = 'eye'
    allowed_domains = ['tianyancha.com']
    start_urls = ['https://www.tianyancha.com/company500']
    # redis_key = "eye"

    # 自定义初始请求
    def start_requests(self):
        # 添加cookies
        cookies = "TYCID=7d47a050864d11e8af695dc8f69ac9f6; undefined=7d47a050864d11e8af695dc8f69ac9f6; _ga=GA1.2.327744665.1531452802; ssuid=6299852934; RTYCID=2c476a4786b34773895e4e68cbd477c3; aliyungf_tc=AQAAABLGZUvsMA8A8qc5cesAjoZfIflv; csrfToken=mBEobIPxWonxolUCSjgamglK; jsid=SEM-BD-GS-SY-08469; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1531481455,1531617072; tyc-user-info=%257B%2522token%2522%253A%2522eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxNTYyMzA1NjI1MCIsImlhdCI6MTUzMTYxNzE0NywiZXhwIjoxNTQ3MTY5MTQ3fQ.X9gjEB8YB8bqNY2JT_BCPm0moQvEzeh3eAJqrUDJC-Wdv5vxbnyx4qqvco2y29RxNbK_i_bbi0nAgO_-6s4Pmw%2522%252C%2522integrity%2522%253A%25220%2525%2522%252C%2522state%2522%253A%25220%2522%252C%2522redPoint%2522%253A%25220%2522%252C%2522vipManager%2522%253A%25220%2522%252C%2522vnum%2522%253A%25220%2522%252C%2522onum%2522%253A%25220%2522%252C%2522mobile%2522%253A%252215623056250%2522%257D; auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxNTYyMzA1NjI1MCIsImlhdCI6MTUzMTYxNzE0NywiZXhwIjoxNTQ3MTY5MTQ3fQ.X9gjEB8YB8bqNY2JT_BCPm0moQvEzeh3eAJqrUDJC-Wdv5vxbnyx4qqvco2y29RxNbK_i_bbi0nAgO_-6s4Pmw; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1531617151"
        cookies = {i.split("=")[0]:i.split("=")[1] for i in cookies.split(";")}

        yield scrapy.Request(
            url=self.start_urls[0],
            callback=self.parse,
            cookies=cookies
        )

    def parse(self, response):
        # 城市列表
        div_list = response.xpath("//div[@class='hotCompany pt30 pb30 new-border-bottom']/div")
        for div in div_list:
            item = {}
            item["city"] = div.xpath("./div[1]/text()").extract_first()
            di_list = div.xpath("./div[2]/a")
            for di in di_list:
                item["company_name"] = di.xpath("./text()").extract_first()
                item["company_href"] = di.xpath("./@href").extract_first()

                yield scrapy.Request(
                    url=item["company_href"],
                    callback=self.parse_company_detail,
                    meta={"item":deepcopy(item)}
                )

    def parse_company_detail(self,response):
        item = response.meta["item"]
        # 简介　地址
        item["desc"] = response.xpath("//div[@class='summary']//script/text()").extract()
        # 两层列表生成式去除空白字符
        item["desc"] = [ x for x in [i.split() for i in item["desc"] if i] if x]
        item["addr"] = response.xpath("//div[@class='detail ']/div[2]/div[2]/text()").extract_first()
        item["url"] = response.xpath("//div[@class='detail ']/div[2]/div[1]/a/@href").extract_first()
        item["phone"] = response.xpath("//div[@class='detail ']/div[1]/div[1]/span[2]/text()").extract_first()
        item["email"] = response.xpath("//div[@class='detail ']/div[1]/div[2]/span[2]/text()").extract_first()

        # 股东列表
        tr_list = response.xpath("//div[@id='_container_topTenNum']/table/tbody/tr")
        item["ten_shareholder"] = []
        for tr in tr_list:
            shares_name = tr.xpath(".//a[@class='link-click']/text()").extract_first()
            item["ten_shareholder"].append(shares_name)

        # 主要成员列表
        tr1_list = response.xpath("//div[@id='_container_staff']//table[@class='table']/tbody/tr")
        item["member_main"] = []
        for tr1 in tr1_list:
            member = {}
            member["member_name"] = tr1.xpath(".//img/@alt").extract_first()
            member["member_job"] = tr1.xpath("./td[3]/span/text()").extract()
            item["member_main"].append(member)

        yield item
























