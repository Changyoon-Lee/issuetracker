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
        
        res_path = os.path.join(os.getcwd(),'data')
        print(res_path)
        file_name = datetime.today().strftime("%m%d") +'_issue.csv'
        file_path = os.path.join(res_path, file_name) 
        if not os.path.isdir(res_path):
            os.makedirs(res_path)
        if not os.path.isfile(file_path): # scrapy 실행하는 dir의 위치에 issue.csv가 있는지 확인 
            self.csvwriter = csv.writer(open(file_path,'w', encoding='utf-8')) 
            self.csvwriter.writerow(['date', 'time', 'index', 'title', 'reply', 'views'])
        else:
            self.csvwriter = csv.writer(open(file_path ,'a', encoding='utf-8')) 
    def process_item(self, item, spider):
        row=[]
        row.append(item['date'])
        row.append(item['time'])
        row.append(item['index'])
        row.append(item['title'])
        row.append(item['reply'])
        row.append(item['views'])


        self.csvwriter.writerow(row)

        return item
