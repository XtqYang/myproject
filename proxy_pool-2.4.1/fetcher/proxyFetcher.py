# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     proxyFetcher
   Description :
   Author :        JHao
   date：          2016/11/25
-------------------------------------------------
   Change Activity:
                   2016/11/25: proxyFetcher
-------------------------------------------------
"""
__author__ = 'JHao'

import re
import json
import base64

from time import sleep

from util.webRequest import WebRequest


class ProxyFetcher(object):
    """
    proxy getter
    """

    @staticmethod
    def freeProxy01():
        """
        站大爷 https://www.zdaye.com/dayProxy.html
        """
        start_url = "https://www.zdaye.com/dayProxy.html"
        html_tree = WebRequest().get(start_url).tree
        latest_page_time = html_tree.xpath("//span[@class='thread_time_info']/text()")[0].strip()
        from datetime import datetime
        interval = datetime.now() - datetime.strptime(latest_page_time, "%Y/%m/%d %H:%M:%S")
        if interval.seconds < 300:  # 只采集5分钟内的更新
            target_url = "https://www.zdaye.com/" + html_tree.xpath("//h3[@class='thread_title']/a/@href")[0].strip()
            while target_url:
                _tree = WebRequest().get(target_url).tree
                for tr in _tree.xpath("//table//tr"):
                    ip = "".join(tr.xpath("./td[1]/text()")).strip()
                    port = "".join(tr.xpath("./td[2]/text()")).strip()
                    yield "%s:%s" % (ip, port)
                next_page = _tree.xpath("//div[@class='page']/a[@title='下一页']/@href")
                target_url = "https://www.zdaye.com/" + next_page[0].strip() if next_page else False
                sleep(5)

    @staticmethod
    def freeProxy02():
        """ 云代理 """
        urls = ['http://www.ip3366.net/free/?stype=1', "http://www.ip3366.net/free/?stype=2"]
        for url in urls:
            r = WebRequest().get(url, timeout=10)
            proxies = re.findall(r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>[\s\S]*?<td>(\d+)</td>', r.text)
            for proxy in proxies:
                yield ":".join(proxy)

    @staticmethod
    def freeProxy3():
        """ 89免费代理 """
        r = WebRequest().get("https://www.89ip.cn/index_1.html", timeout=10)
        proxies = re.findall(
            r'<td.*?>[\s\S]*?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})[\s\S]*?</td>[\s\S]*?<td.*?>[\s\S]*?(\d+)[\s\S]*?</td>',
            r.text)
        for proxy in proxies:
            yield ':'.join(proxy)

    @staticmethod
    def freeProxy4():
        """ free免费代理 """
        urls = ['https://freeproxyupdate.com/']
        request = WebRequest()
        for url in urls:
            r = request.get(url, timeout=10)
            proxies = re.findall(r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>[\s\S]*?<td>(\d+)</td>', r.text)
            for proxy in proxies:
                print(proxy)
                yield ':'.join(proxy)

    @staticmethod
    def freeProxy5():
        """ best-proxy免费代理 """
        urls = ['https://best-proxy.com/english/index.php?p=1', 'https://best-proxy.com/english/index.php?p=2',
                'https://best-proxy.com/english/index.php?p=3']
        request = WebRequest()
        for url in urls:
            r = request.get(url, timeout=10)
            pattern = r"Proxy\('([^']+)'\)"
            proxies = re.findall(pattern, r.text)
            # 对匹配到的 base64 进行解码
            decoded_proxies = [base64.b64decode(proxy).decode('utf-8') for proxy in proxies]
            for proxy in decoded_proxies:
                yield proxy

    @staticmethod
    def freeProxy6():
        """ ProxyLister免费代理 """
        r = WebRequest().get("https://proxylister.com/", timeout=10)
        pattern = r'<td class="table-ip"><strong>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</strong></td>\s*<td>(\d+)</td>'
        proxies = re.findall(pattern, r.text)
        for proxy in proxies:
            yield ':'.join(proxy)

#
# if __name__ == '__main__':
#     p = ProxyFetcher()
#     for _ in p.freeProxy6():
#         print(_)
#
