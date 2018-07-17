# -*- coding: utf-8 -*-
import scrapy,re
import random
from selenium import webdriver
import time

from pprint import pprint

class XlangSpider(scrapy.Spider):
    name = 'xlang'
    allowed_domains = ['weibo.com']
    start_urls = ['https://d.weibo.com/100803?refer=index_hot_new']
    cookie = None


    def start_requests(self):
        cookies = random.choice(["SINAGLOBAL=1701840261058.1406.1528730867177; un=15623056250; wvr=6; login_sid_t=c61de11f028f945b0f57dd85f8f01723; cross_origin_proto=SSL; _s_tentry=passport.weibo.com; Apache=3078431802770.787.1531702696298; ULV=1531702696303:2:2:2:3078431802770.787.1531702696298:1531620297457; crossidccode=CODE-tc-1FERQu-3mcya0-13Oftf3TeiKi5x987f9ae; ALF=1563238731; SSOLoginState=1531702731; SCF=Apgtvkm-XeAJkJ3RqQ0lmRE0FFe36MC3XSq6Ylz96MMhg-g2U0ltOxopYSeUqdRB5JggIi59y2WXb8M3KX6WgWY.; SUB=_2A252T52cDeRhGeBL61MX-CrLyDSIHXVVPIhUrDV8PUNbmtAKLW34kW9NR3QRF0Y539UFbm5Zu2CUzTRr1_DKY2AY; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5hPnXre2HlWbJboqkVd8Z15JpX5KzhUgL.Foqfeh2c1hBNe0n2dJLoIp7LxKML1KBLBKnLxKqL1hnLBoMcSK5pSonXS0eR; SUHB=0mxEzId7nArx0U; UOR=,,graph.qq.com; YF-Page-G0=734c07cbfd1a4edf254d8b9173a162eb; wb_view_log_6501684738=1366*7681",
                   "UOR=cn.ui.vmall.com,widget.weibo.com,graph.qq.com; SINAGLOBAL=5092995624201.049.1527672178112; ULV=1531703865830:3:2:2:6345801572474.279.1531703865827:1531625587371; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhP5..wE.gRweHg982AQI2Z5JpX5K2hUgL.Foqceh2pShzEeh-2dJLoI7yRds8V9f8W-Btt; SUHB=0U1JbzdagCcIBE; wvr=6; YF-Ugrow-G0=169004153682ef91866609488943c77f; SUB=_2A252T4KVDeRhGeBI61MQ9CzOyzmIHXVVPPNdrDV8PUJbmtAKLRTGkW9NRqHOhVhz-xupeZyhTyHnh5aHS_p6KxRt; login_sid_t=294ca433a9f97596b81afb2d2945a809; cross_origin_proto=SSL; YF-V5-G0=731b77772529a1f49eac82a9d2c2957f; WBStorage=5548c0baa42e6f3d|undefined; wb_view_log=1366*7681; _s_tentry=passport.weibo.com; Apache=6345801572474.279.1531703865827; crossidccode=CODE-tc-1FES94-3mcya0-LKACDGRQJUXsGE56f8581; SSOLoginState=1531703884; YF-Page-G0=734c07cbfd1a4edf254d8b9173a162eb; wb_view_log_6501684738=1366*7681; SCF=Aq6ugZhc-Wbk1PidROiRrT5Ek1jCRiCx7cO7g7UVkj7BgcWkQgTse1PPPpbR_ONsZUZI1cw_u6BOBfrFDmbY3yE.; un=15623056250; wb_view_log_6601142205=1366*7681; WBtopGlobal_register_version=2018071609",
                    "SINAGLOBAL=2345532349201.569.1531624490995; WBStorage=5548c0baa42e6f3d|undefined; login_sid_t=a8157401c344060233b398ff31eca376; cross_origin_proto=SSL; YF-Ugrow-G0=8751d9166f7676afdce9885c6d31cd61; YF-V5-G0=f59276155f879836eb028d7dcd01d03c; _s_tentry=-; wb_view_log=1366*7681; Apache=2082738887400.83.1531703681467; ULV=1531703681478:2:2:2:2082738887400.83.1531703681467:1531624491016; SUB=_2A252T4HCDeRhGeVP6VsW9SzPyz-IHXVVPPQKrDV8PUNbmtAKLU3wkW9NTULdbGbROGNMb4FRSfRcdv9-uSDmoMm4; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhCaxvwAb97RmOi4IlwyY575JpX5KzhUgL.Foepeo.NSKz0ehe2dJLoIEBLxKML12zLB-eLxKqLB-BLBK-LxK-LB.-LB--LxK-L1hML1h.t; SUHB=0LcivReILYjpnr; ALF=1563239698; SSOLoginState=1531703698; wvr=6; YF-Page-G0=e1a5a1aae05361d646241e28c550f987; wb_view_log_3129752303=1366*7681"])

        self.cookie = {i.split("=")[0]:i.split("=")[1] for i in cookies.split(";")}

        yield scrapy.Request(
            url=self.start_urls[0],
            callback=self.parse,
            cookies=self.cookie
        )

    def parse(self, response):

        sub_top = r"DSC_topicon.*?\\\">(\w+?)<\\/span>.+?href=\\\"([http:]{0,5}\\\/\\\/[s\.]{0,2}weibo\.com\\/[weibo]{0,5}p?\\/.+?\?from=faxian_huati)\\\".+?#(.+?)[\.#]"
        top_list = re.findall("DSC_topicon.*?#.*?#",response.body.decode(),re.S)
        for top in top_list:
            item = {}
            ret = re.findall(sub_top,top,re.S)
            if ret:
                ret = ret[0]
                item["rank"] = ret[0]
                item["href"] = ret[1]
                if "http:" not in item["href"]:
                    item["href"] = "https:" + item["href"]
                item["href"] = re.sub(r"\\/\\/|\\/","//",item["href"])
                item["title"] = ret[2]

                headers = {"Upgrade-Insecure-Requests": 1,
                           "Referer":item["href"],
                           "Host": "weibo.com"
                           }

                yield scrapy.Request(
                    url=item["href"],
                    callback=self.parse_detail,
                    meta={"item":item},
                    cookies=self.cookie,
                    headers=headers
                )

        next_url = re.search(r"class=\\\"page next S_txt1 S_line1\\\" href=\\\"(.*?)\\\"><span>下一页<\\/span>",response.body.decode())
        if next_url:
            next_url = "https://d.weibo.com/100803?" + next_url.group(1)
            # print(next_url)
            yield scrapy.Request(
                url=next_url,
                callback=self.parse,
                cookies=self.cookie
            )

    def parse_detail(self,response):
        item = response.meta["item"]
        # TODO 未完成
        with open("te.txt","a") as f:
            f.write(response.body.decode())







