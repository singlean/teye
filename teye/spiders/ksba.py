# -*- coding: utf-8 -*-
import scrapy


class KsbaSpider(scrapy.Spider):
    name = 'ksba'
    allowed_domains = ['kaishiba.com']
    start_urls = ['https://m.kaishiba.com/api/advert/list?position=1&position=1&client=wap']
    cookies = "UM_distinctid=1649cb2db7954a-047116b083ebc1-5b163f13-100200-1649cb2db7a706; PHPSESSID=kbv4mo6auf2igpoq9mjtabqiq3; userinfo=U2FsdGVkX1%2BRbEeCzLWaewMElb8IGCUsCHp74AnJ4z3sPpUfUwYCUALKiIBhUOnh%2FDsLZUDOwdN00lbuur7FnkA9A%2FunOIF7TwrqltDHQ42qXLmx1cluQbMXll4gqEqsNMmPUtRJiqzAQpee6XUJn3WOFU%2B7qtg3oL%2Fmro%2Bg0SpU1zOX%2F7JrezcUuKGmFNL%2BwPeCDnpFQiM6WcvisRiHJ5tAbdvtRgMia6tdyhvnGu2HMis4Igy%2BYtpATjtkJsfcAsj644NQtb%2FFjXHn7s%2B4gG72n894blYhOaSQNY%2FxU2Q%3D; from=null; CNZZDATA1260467161=1500163830-1531742760-%7C1531746329; source=wxhd; channel_no=about_index; channel=wap; Hm_lvt_ea581b4eabd38795a7e47456ec643e31=1531748064,1531748072,1531748160,1531748691; client=wap; back_url=http%3A%2F%2Fm.kaishiba.com%2Fproject%2Fdetail%2Fid%2F703A2E0C730695C8E050190AFD012616%2Frefer%2Findex; _cnzz_CV1260467161=%E8%AE%BF%E5%AE%A2%E6%9D%A5%E6%BA%90%7Cnull%7C1532007901090; Hm_lpvt_ea581b4eabd38795a7e47456ec643e31=1531748784; SERVERID=5f5075e5ded2f2630e8f277d4c87cd20|1531748905|1531747304; backUrl=U2FsdGVkX1%2FNxa0ZPht5jZb2riRESLjaB61nGLp8fFfU47TmdeiKVQ5A3i5TJeZX"
    cookies = {i.split("=")[0]: i.split("=")[1] for i in cookies.split(";")}
    headers = {"referer": "https://m.kaishiba.com/"}

    def start_requests(self):


        yield scrapy.Request(
            url=self.start_urls[0],
            callback=self.parse,
            cookies=self.cookies,
            headers=self.headers
        )

    def parse(self, response):
        with open("te.txt","a") as f:
            f.write(response.body.decode())
            f.write("\n\n\n\n\n")




# import re
# str = r"<p class=\"total\">\n    <span>\u9605\u8bfb9.8\u4ebf<\/span>    <span>\u8ba8\u8bba313\u4e07<\/span>    <\/p>"
#
# ret = re.findall(r"<p class=\\\"total\\\">.*?<span>(.*?)<\\/span>.*?<span>(.*?)<\\/span>.*?<\\/p>",str,re.S)
#





























