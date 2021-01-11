import scrapy
import re
from issuecrawl.items import IssuecrawlItem
from datetime import datetime, timedelta
from scrapy.http import HtmlResponse
import requests
from bs4 import BeautifulSoup

class IssueSpider(scrapy.Spider):
    name = 'issue'
    # start_urls = ['https://theqoo.net/index.php?mid=hot']
    
    def start_requests(self):
        self.chk=0
        print('request')
        start_url = 'https://theqoo.net/index.php?mid=hot'
        i=0
        yesDate = (datetime.now()-timedelta(days=1)).strftime('%m.%d')
        while self.chk==0 and i<8:
            i+=1
            url = start_url+'&page={}'.format(i)
            
            resp=requests.get(url)
            soup=BeautifulSoup(resp.content, 'lxml')
            a_tag = soup.select('div table tbody tr td.time')
            if not (':' in a_tag[-1].text.strip() or yesDate == a_tag[-1].text.strip()):
                self.chk=1
            # //*[@id="bd_801402415_0"]/div/table/tbody/tr[34]/td[4]
            
            
            print(i,'page'+'-'*30)

            yield scrapy.Request(url=url, meta={"yesDate":yesDate},callback=self.parse_page)

        
    def parse_page(self, response):

        now = datetime.now() # 현재시간
        nowDate = now.strftime('%m-%d')
        nowTime = now.strftime('%H:%M')

        print('***크롤링 중 ***')

        for line in response.xpath('//*[@id="bd_801402415_0"]/div/table/tbody/tr'):
            index = line.xpath('td[1]/text()').extract()[0].strip()
            
            if line.xpath('td[4]/text()').extract():
                T = line.xpath('td[4]/text()').extract()[0].strip()
            else : T = 0
            
            if index.isdecimal() and (':' in T or response.meta["yesDate"] == T):
                
                url = 'https://theqoo.net'+line.xpath('td[3]/a/@href').extract()[0]
                title = line.xpath('td[3]/a[1]/span/text()').extract()[0].strip()
                reply = line.xpath('td[3]/a[2]/text()').extract()[0].strip()
                views = line.xpath('td[5]/text()').extract()[0].strip()
                if '만' in views:
                    views=int(views[:-1].replace('.',''))*1000 # 단위 조정
                

                item = IssuecrawlItem()

                item['index'] = index
                item['date'] = nowDate
                item['time'] = nowTime
                item['title'] = title
                item['reply'] = reply
                item['views'] = views


                yield item
                # yield scrapy.Request(url=url, meta={'Index':index,'Date':nowDate, 'Time':nowTime, 'Title':title, 'Reply':reply, 'Views':views}, callback=self.parse_reply)#,2227,1018,1001
    



    def parse_reply(self, response):
        item = IssuecrawlItem()

        item['index'] = response.meta['Index']
        item['date'] = response.meta['Date']
        item['time'] = response.meta['Time']
        item['title'] = response.meta['Title']
        item['reply'] = response.meta['Reply']
        item['views'] = response.meta['Views']

        yield item
