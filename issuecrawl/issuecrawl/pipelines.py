# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import csv
import os
from datetime import datetime

class IssuecrawlPipeline:
    def __init__(self):
        date = datetime.today().strftime("%m%d")
        if date+'_issue.csv' not in os.listdir(os.getcwd()): # scrapy 실행하는 dir의 위치에 issue.csv가 있는지 확인 
            self.csvwriter = csv.writer(open(date+'_issue.csv','w', encoding='utf-8')) 
            self.csvwriter.writerow(['date', 'time', 'index', 'title', 'reply', 'views'])
        else:
            self.csvwriter = csv.writer(open(date+'_issue.csv','a', encoding='utf-8')) 
    def process_item(self, item, spider):
        row=[]
        row.append(item['date'])
        row.append(item['time'])
        row.append(item['index'])
        row.append(item['title'])
        row.append(item['views'])
        row.append(item['reply'])

        self.csvwriter.writerow(row)

        return item