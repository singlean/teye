# -*- coding: utf-8 -*-
import scrapy
import pprint
from copy import deepcopy
from urllib.parse import urljoin
from scrapy_redis.spiders import RedisSpider

class DpingSpider(RedisSpider):
    name = 'dping'
    allowed_domains = ['maoyan.com']
    # start_urls = ['http://maoyan.com/board']
    redis_key = "dping"

    def parse(self, response):

        # 榜单列表
        li_list = response.xpath("//div[@class='subnav']/ul/li")
        for li in li_list:
            item = {}
            item["list_title"] = li.xpath("./a/text()").extract_first()
            item["list_href"] = li.xpath("./a/@href").extract_first()
            if item["list_href"]:
                if "board" in item["list_href"]:
                    item["list_href"] = "http://maoyan.com" + item["list_href"]
                else:
                    item["list_href"] = "http://maoyan.com/board/" + "7"

                yield scrapy.Request(
                    url=item["list_href"],
                    callback=self.parse_page_list,
                    meta={"item":item}
                )

    def parse_page_list(self,response):

        item = response.meta["item"]
        # 电影列表
        dd_list = response.xpath("//div[@class='main']/dl/dd")
        for dd in dd_list:
            item["movie_name"] = dd.xpath(".//div[@class='movie-item-info']/p[@class='name']/a/text()").extract_first()
            item["movie_url"] = dd.xpath(".//div[@class='movie-item-info']/p[@class='name']/a/@href").extract_first()
            if item["movie_url"]:
                item["movie_url"] = "http://maoyan.com" + item["movie_url"]
            item["movie_star"] = dd.xpath(".//div[@class='movie-item-info']/p[@class='star']/text()").extract()
            # 去除空白字符
            item["movie_star"] = [i.strip() for i in item["movie_star"] if i.strip()]
            item["movie_show_time"] = dd.xpath(".//div[@class='movie-item-info']/p[@class='releasetime']/text()").extract_first()

            if "board/7" in response.url or "board/4" in response.url:
                movie_score = dd.xpath(".//div[@class='movie-item-number score-num']/p/i/text()").extract()
                item["movie_score"] = ""
                for i in movie_score:
                    item["movie_score"] += i
            item["list_rank"] = dd.xpath("./i/text()").extract_first()
            item["movie_img"] = dd.xpath(".//img[@class='board-img']/@src").extract_first()

            yield scrapy.Request(
                url=item["movie_url"],
                callback=self.parse_detail,
                meta={"item":deepcopy(item)}
            )

        # 下一页
        next_url = response.xpath("//a[text()='下一页']/@href").extract_first()
        if next_url:
            next_url = urljoin(response.url,next_url)
            print("下一页地址",next_url)
            yield scrapy.Request(
                url=next_url,
                callback=self.parse_page_list,
                meta={"item":item}
            )

    def parse_detail(self,response):

        item = response.meta["item"]
        # 评论列表
        li_list = response.xpath("//li[@class='comment-container ']")

        item["comment_list"] = []
        for li in li_list:
            items = {}
            items["comment"] = li.xpath(".//div[@class='comment-content']/text()").extract()
            items["praise"] = li.xpath(".//span[@class='num']/text()").extract_first()
            items["author"] = li.xpath(".//div[@class='user']/span[@class='name']/text()").extract_first()
            items["time"] = li.xpath(".//div[@class='time']/span/@title").extract_first()
            items["zuthor_img"] = li.xpath(".//div[@class='portrait']/img/@src").extract_first()

            item["comment_list"].append(items)

        yield item















































